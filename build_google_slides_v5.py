#!/usr/bin/env python3
"""
Build the SEO Week 2026 v5 presentation in Google Slides.
Sets PNG slide backgrounds from GitHub raw URLs (slides_v5/).

Requires:
  pip install google-auth google-auth-oauthlib google-api-python-client

Usage:
  python3 build_google_slides_v5.py
  python3 build_google_slides_v5.py --dark   # use dark About slide
"""

import os
import pickle
import argparse

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/presentations"]
CREDS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

REPO = "https://raw.githubusercontent.com/cyberandy/infinite-context/main"

# ── Slide order (matches generate_slides_v5.py) ──
SLIDES_WHITE = [
    "slide_01_title",
    "slide_02_about",
    "slide_03_weight",
    "slide_04_journey",
    "slide_05_shifts",
    "slide_06_paradox",
    "slide_07_turboquant",
    "slide_08_rankings",
    "slide_09_realignment",
    "slide_10_landscape",
    "slide_11_explores",
    "slide_12_advantage",
    "slide_13_discovery",
    "slide_14_gap",
    "slide_15_ondevice",
    "slide_16_training",
    "slide_17_floor",
    "slide_18_moat",
    "slide_19_connected",
    "slide_20_thesis",
]

SLIDES_DARK_ABOUT = list(SLIDES_WHITE)
SLIDES_DARK_ABOUT[1] = "slide_02_about_dark"

EMU_PER_PX = 9525
SLIDE_W = 1920 * EMU_PER_PX
SLIDE_H = 1080 * EMU_PER_PX


def get_credentials():
    """Authenticate with Google OAuth2."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
    return creds


def main():
    parser = argparse.ArgumentParser(
        description="Build v5 'Structure Is the Moat' deck in Google Slides"
    )
    parser.add_argument("--dark", action="store_true",
                        help="Use dark variant for the About slide")
    args = parser.parse_args()

    slides_list = SLIDES_DARK_ABOUT if args.dark else SLIDES_WHITE
    variant = "dark" if args.dark else "white"
    n = len(slides_list)

    creds = get_credentials()
    service = build("slides", "v1", credentials=creds)

    # 1. Create presentation
    print(f"Creating presentation ({variant} About variant, {n} slides)...")
    res = service.presentations().create(
        body={"title": f"Structure Is the Moat — v5 ({variant})"}
    ).execute()
    pres_id = res["presentationId"]

    # 2. Add blank slides (first slide already exists)
    requests = []
    for i in range(1, n):
        slide_id = f"slide_{i:02d}"
        requests.append({
            "createSlide": {
                "objectId": slide_id,
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }
        })

    if requests:
        print(f"  Adding {len(requests)} blank slides...")
        service.presentations().batchUpdate(
            presentationId=pres_id, body={"requests": requests}
        ).execute()

    # 3. Refetch slide IDs
    pres = service.presentations().get(presentationId=pres_id).execute()
    all_slides = pres["slides"]
    print(f"  ✓ Total slides: {len(all_slides)}")

    # 4. Set background images from GitHub
    for idx, slide_name in enumerate(slides_list):
        slide_obj = all_slides[idx]
        page_id = slide_obj["objectId"]
        png_url = f"{REPO}/slides_v5/{slide_name}.png"
        print(f"  [{idx+1:02d}/{n}] {slide_name}...", end=" ", flush=True)

        requests = [{
            "updatePageProperties": {
                "objectId": page_id,
                "pageProperties": {
                    "pageBackgroundFill": {
                        "stretchedPictureFill": {"contentUrl": png_url}
                    }
                },
                "fields": "pageBackgroundFill",
            }
        }]

        try:
            service.presentations().batchUpdate(
                presentationId=pres_id, body={"requests": requests}
            ).execute()
            print("✓")
        except Exception as e:
            print(f"FAILED")
            print(f"  Error: {e}")
            continue

    url = f"https://docs.google.com/presentation/d/{pres_id}/edit"
    print(f"\n✓ Presentation ready: {url}")
    return url


if __name__ == "__main__":
    main()

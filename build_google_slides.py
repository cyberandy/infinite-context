#!/usr/bin/env python3
"""
Build the SEO Week 2026 presentation in Google Slides.
Sets PNG backgrounds from GitHub raw URLs + adds curated GIF overlays.
"""

import os
import pickle
from pathlib import Path
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/presentations"]
CREDS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

import subprocess
REPO = f"https://raw.githubusercontent.com/cyberandy/infinite-context/main"

# ── Slide order (matches generate_slides_v2_bold.py) ──────────────
SLIDES = [
    "01_title", "02_origin", "03_numbers", "04_more_context", "05_journey",
    "06_three_shifts", "07_two_responses", "08_memory_layer", "09_experiment",
    "10_takeaway_1", "11_compression", "12_turboquant", "13_silent_failure",
    "14_zero_bias", "15_landscape", "16_visibility", "17_environment",
    "18_rlm", "19_how_it_works", "20_rlm_on_kg", "21_explores", "22_benchmark",
    "23_separation", "24_capability", "25_comparison", "26_behavioral",
    "27_evolution", "28_new_workflow", "29_audit", "30_conclusion",
    "31_thesis", "32_cta"
]

# ── Curated GIF overlays (only the ones that earn their pixels) ──
GIF_MAP = {
    "03_numbers": "10b_context_timeline",
    "04_more_context": "02b_more_context",
    "05_journey": "03_two_columns",
    "06_three_shifts": "04_three_shifts",
    "11_compression": "05_compression_reveal",
    "12_turboquant": "06_turboquant_counter",
    "13_silent_failure": "24_ghost_counter",
    "19_how_it_works": "11_pipeline_steps",
    "20_rlm_on_kg": "12_graph_nodes",
    "21_explores": "27_explore_verify_cite",
    "25_comparison": "15b_graphrag_faceoff",
    "26_behavioral": "17_distillation_pipeline",
    "28_new_workflow": "26_consistency_bars",
    "29_audit": "20_floor_set",
    "31_thesis": "30_closing_cta",
}

EMU_PER_PX = 9525  # EMUs per pixel
SLIDE_W = 1920 * EMU_PER_PX
SLIDE_H = 1080 * EMU_PER_PX
GIF_W = 800 * EMU_PER_PX
GIF_H = 600 * EMU_PER_PX


def main():
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

    service = build("slides", "v1", credentials=creds)

    # 1. Start fresh with a new presentation
    print("Creating presentation...")
    res = service.presentations().create(body={"title": "Structure Is the Moat — Keynote v2"}).execute()
    pres_id = res["presentationId"]

    # 2. Add blank slides for the rest of the outline
    requests = []
    for i in range(1, len(SLIDES)):
        slide_id = f"slide_{i:02d}"
        requests.append({
            "createSlide": {
                "objectId": slide_id,
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }
        })

    if requests:
        print(f"  Adding {len(requests)} slides...")
        service.presentations().batchUpdate(presentationId=pres_id, body={"requests": requests}).execute()

    # 3. Get all slide IDs (refetch)
    pres = service.presentations().get(presentationId=pres_id).execute()
    all_slides = pres["slides"]
    print(f"  ✓ Total slides: {len(all_slides)}")

    # 4. Set backgrounds + GIF overlays
    requests = []
    for idx, slide_name in enumerate(SLIDES):
        slide_obj = all_slides[idx]
        page_id = slide_obj["objectId"]
        png_url = f"{REPO}/slides_v2/{slide_name}.png"
        print(f"  ({idx+1}/{len(SLIDES)}) Mapping {slide_name}...")

        # Background PNG
        requests.append({
            "updatePageProperties": {
                "objectId": page_id,
                "pageProperties": {
                    "pageBackgroundFill": {
                        "stretchedPictureFill": {"contentUrl": png_url}
                    }
                },
                "fields": "pageBackgroundFill",
            }
        })

        # Opt-in GIF Overlay
        if slide_name in GIF_MAP:
            gif_name = GIF_MAP[slide_name]
            gif_url = f"{REPO}/content_animations_v2/{gif_name}.gif"
            requests.append({
                "createImage": {
                    "objectId": f"gif_{idx:02d}",
                    "url": gif_url,
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"width": {"magnitude": GIF_W, "unit": "EMU"}, "height": {"magnitude": GIF_H, "unit": "EMU"}},
                        "transform": {"scaleX": 1, "scaleY": 1, "translateX": (SLIDE_W - GIF_W)//2, "translateY": (SLIDE_H - GIF_H)//2, "unit": "EMU"}
                    }
                }
            })

    # Submit in batches
    batch_size = 50
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        print(f"  Applying batch {i//batch_size + 1}...")
        service.presentations().batchUpdate(presentationId=pres_id, body={"requests": batch}).execute()

    print(f"\n✓ Presentation Ready: https://docs.google.com/presentation/d/{pres_id}/edit")


if __name__ == "__main__":
    main()

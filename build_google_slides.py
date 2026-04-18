#!/usr/bin/env python3
"""
Build the SEO Week 2026 presentation in Google Slides.
Sets PNG backgrounds from GitHub raw URLs + adds curated GIF overlays.
"""

import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/presentations"]
CREDS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

import subprocess
commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
REPO = f"https://raw.githubusercontent.com/cyberandy/infinite-context/{commit_hash}"

# ── Slide order (matches slides_v2/) ──────────────────
SLIDES = [
    "01_title", "02_weight_problem", "03_query_to_journey", "04_three_shifts",
    "04b_memory_layer",
    "05_compression_paradox", "06_turboquant", "07_silent_ranking", "08_zero_bias",
    "09_quant_landscape", "10_turbo_demo",
    "10b_context_timeline", "10c_librarian",
    "11_navigator", "12_rlm_demo",
    "13_conditional_advantage", "14_separation", "15_model_gap",
    "15b_graphrag",
    "17_distillation",
    "18_slm_edge", "19_connected_data", "20_floor_set", "21_moat_graph",
    "22_seo_playbook_chapter", "23_visibility_shift", "24_ghost_citations",
    "25_gpt_reads_differently", "26_consistency_not_crawling", "27_explore_verify_cite",
    "28_autoResearch", "29_well_connected", "30_closing",
]

# ── Curated GIF overlays (only the ones that earn their pixels) ──
GIF_MAP = {
    "02_weight_problem": "02_context_chaos",
    "03_query_to_journey": "03_two_columns",
    "04_three_shifts": "04_three_shifts",
    "05_compression_paradox": "05_compression_reveal",
    "06_turboquant": "06_turboquant_counter",
    "10b_context_timeline": "10b_context_timeline",
    "11_navigator": "11_pipeline_steps",
    "12_rlm_demo": "12_graph_nodes",
    "15b_graphrag": "15b_graphrag_faceoff",
    "17_distillation": "17_distillation_pipeline",
    "20_floor_set": "20_checklist",
    "21_moat_graph": "21_moat_graph",
    "24_ghost_citations": "24_ghost_counter",
    "26_consistency_not_crawling": "26_consistency_bars",
    "27_explore_verify_cite": "27_explore_verify_cite",
    "30_closing": "30_closing_cta",
}

EMU_PER_PX = 9525  # EMUs per pixel
SLIDE_W = 1920 * EMU_PER_PX
SLIDE_H = 1080 * EMU_PER_PX
GIF_W = 800 * EMU_PER_PX
GIF_H = 600 * EMU_PER_PX


def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return creds


def main():
    print("Authenticating...")
    creds = authenticate()
    service = build("slides", "v1", credentials=creds)

    # 1. Create presentation
    print("Creating presentation...")
    pres = service.presentations().create(
        body={
            "title": "Structure Is the Moat — SEO Week 2026",
            "pageSize": {
                "width": {"magnitude": SLIDE_W, "unit": "EMU"},
                "height": {"magnitude": SLIDE_H, "unit": "EMU"},
            },
        }
    ).execute()
    pres_id = pres["presentationId"]
    print(f"  ✓ Created: https://docs.google.com/presentation/d/{pres_id}")

    # The new presentation has 1 blank slide — we'll use it for slide 01
    # and add 28 more
    existing = pres["slides"]
    first_slide_id = existing[0]["objectId"]

    # 2. Build batch requests
    requests = []

    # Create 28 additional blank slides (we already have 1)
    for i in range(1, len(SLIDES)):
        slide_id = f"slide_{i:02d}"
        requests.append({
            "createSlide": {
                "objectId": slide_id,
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }
        })

    # Submit slide creation
    if requests:
        print(f"  Adding {len(requests)} slides...")
        service.presentations().batchUpdate(
            presentationId=pres_id, body={"requests": requests}
        ).execute()

    # 3. Re-fetch to get all slide IDs
    pres = service.presentations().get(presentationId=pres_id).execute()
    all_slides = pres["slides"]
    print(f"  ✓ Total slides: {len(all_slides)}")

    # 4. Set backgrounds + add GIF overlays
    requests = []
    for idx, slide_name in enumerate(SLIDES):
        slide_obj = all_slides[idx]
        page_id = slide_obj["objectId"]
        png_url = f"{REPO}/slides_v2/{slide_name}.png"

        # Set background
        requests.append({
            "updatePageProperties": {
                "objectId": page_id,
                "pageProperties": {
                    "pageBackgroundFill": {
                        "stretchedPictureFill": {
                            "contentUrl": png_url,
                        }
                    }
                },
                "fields": "pageBackgroundFill",
            }
        })

        # Add GIF overlay if curated
        if slide_name in GIF_MAP:
            gif_name = GIF_MAP[slide_name]
            gif_url = f"{REPO}/content_animations_v2/{gif_name}.gif"
            img_id = f"gif_{idx:02d}"

            # Center the GIF on the slide
            left = (SLIDE_W - GIF_W) // 2
            top = (SLIDE_H - GIF_H) // 2

            requests.append({
                "createImage": {
                    "objectId": img_id,
                    "url": gif_url,
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {
                            "width": {"magnitude": GIF_W, "unit": "EMU"},
                            "height": {"magnitude": GIF_H, "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": left,
                            "translateY": top,
                            "unit": "EMU",
                        },
                    },
                }
            })

    # Submit in batches (API limit ~500 per batch)
    batch_size = 50
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        print(f"  Applying requests {i+1}–{i+len(batch)} of {len(requests)}...")
        service.presentations().batchUpdate(
            presentationId=pres_id, body={"requests": batch}
        ).execute()

    print(f"\n✓ Done! Open your presentation:")
    print(f"  https://docs.google.com/presentation/d/{pres_id}/edit")


if __name__ == "__main__":
    main()

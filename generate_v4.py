#!/usr/bin/env python3
"""
Generate V4.1 presentation videos — motion-only prompts (no text rendering).

Uses Veo 3.1 on Vertex AI to animate existing slide PNGs with restrained,
grid-disciplined motion. Prompts describe ONLY motion behavior; the source
image provides all text and layout.

Usage:
    python generate_v4.py [--start-from N] [--only N] [--check]
"""

import argparse
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai import types

# Load environment variables
load_dotenv()


# ── Swiss Style preamble (prepended to every animation prompt) ──
# Focuses on motion style and anti-hallucination guardrails.
SWISS_PREAMBLE = (
    "Animate this presentation slide with very subtle, restrained motion. "
    "Locked-off frontal camera, no rotation, no camera movement. "
    "DO NOT add, remove, or modify any text or labels on the slide. "
    "DO NOT generate any new text characters. "
    "Keep the existing slide content exactly as shown in the image. "
    "White background, clean editorial feel, Swiss modernist design. "
)

# ── 20 slides: (source_filename, motion_prompt) ──
# Prompts describe ONLY what should move, never what text to create.
SLIDES = [
    # ── Ch 1: Infinite Context ──
    ("01_ch1_title.png",
     "The large red wedge draws in smoothly from the bottom right, anchoring the composition. "
     "The title text '01 INFINITE CONTEXT' remains sharp and static on the black background. "
     "Subtle parallax between the large number and the title. "
     "Elegant, minimal, Swiss-style reveal."),

    ("02_context.png",
     "The slide content fades in gently. The 'visible' blue section in the context window "
     "bar pulses with a steady, clinical rhythm. The line between the brain icon and "
     "the bar draws in precisely. Clean, restrained, scientific feel."),

    ("03_quadratic.png",
     "The bar chart grows smoothly from the bottom: the short blue bar settles first, "
     "followed by the dramatic growth of the red bar. Network diagram nodes "
     "on the right pulse with subtle activity. Restrained data visualization."),

    ("04_race.png",
     "The blue staircase chart animates step by step, reflecting the growth of "
     "context windows from 2K to 10M+. Each step appears with a precise, "
     "modular slide-in. Clean, editorial layout with active whitespace."),

    # ── Ch 2: Architecture ──
    ("05_ch2_title.png",
     "The wide red wedge slides across the center horizontally, dividing the "
     "large '02' from the 'ARCHITECTURE' title. The blue triangle in the bottom "
     "right glows subtly. Minimal, elegant chapter reveal with Swiss grid discipline."),

    ("06_stretching.png",
     "Three rows of architectural techniques reveal sequentially from top to bottom. "
     "Text appears with a crisp, no-bounce fade and slide-in. "
     "Thin horizontal hairline dividers draw across the grid. Precise and functional."),

    ("07_ceiling.png",
     "The performance curve draws smoothly from left to right. It plateaus accurately "
     "before dropping at the 'Context Rot' mark. The red indicator wedge pulses "
     "once to highlight the drop. Analytical and deliberate."),

    ("08_tworoutes.png",
     "The vertical dividing line draws down the center. The left column (bigger brain) "
     "and right column (smarter memory) fade in with balanced symmetry. "
     "Clean, asymmetric Swiss composition remains perfectly steady."),

    # ── Ch 3: Memory ──
    ("09_ch3_title.png",
     "The red wedge pulses with a steady, clinical light. The large '03' and "
     "'MEMORY' title remain static. Subtle parallax adds depth without breaking "
     "the grid. Minimalist and cinematic chapter intro."),

    ("10_virtual.png",
     "The memory hierarchy bars fill in with staggered timing: Main Context, "
     "then Recall Storage, then Archival Vector DB. Labels appear precisely "
     "above each bar. Systematic, modular animation style."),

    ("11_rag.png",
     "Flow diagram arrows draw in sequence from the question mark to the database "
     "and finally to the LLM brain. Each icon settles with a subtle, sharp "
     "reveal. Clean, technical schematic animation."),

    ("12_rlm.png",
     "Two-column juxtaposition: the left 'speed reader' side fades in muted, "
     "the right 'librarian' side enters with a sharp, vivid reveal. "
     "The blue arrow between them draws last. Confident, editorial pacing."),

    # ── Ch 4: Recursion ──
    ("13_ch4_title.png",
     "The red lightning-wedge accent pulses with energy. The large '04' and "
     "'RECURSION' title are locked and sharp. Elegant slow zoom into the "
     "entire modular composition. Dramatic yet restrained."),

    ("14_howrlm.png",
     "The recursive loop animates: the arrow from 'writes code' to 'External REPL' "
     "draws first, followed by the return arrow 'results return' below it. "
     "Arrows move with precise, non-curved motion. Clean technical flow."),

    ("15_paper.png",
     "The circular 'RLM-on-KG' diagram draws clockwise with a steady pen-stroke "
     "motion, revealing Seed, Expand, Verify, Collect, and Re-rank. "
     "The '9 tools' center label fades in last. Balanced and clear."),

    ("16_results.png",
     "The F1 scores reveal with a sharp fade-in. A thin blue box draws around "
     "the '56% win rate' statistic to highlight the key result. "
     "Minimum decoration, maximum data clarity. Confident reveal."),

    # ── Ch 5: The SEO Playbook ──
    ("17_ch5_title.png",
     "The red wedge and blue star accent pulse together in a slow, synchronized "
     "rhythm. The '05' and 'THE SEO PLAYBOOK' title remain sharp. "
     "Swiss International Style at its most cinematic."),

    ("18_oldnew.png",
     "The top 'crawling' section fades into a desaturated gray, then a striking "
     "red line draws through it. The bottom 'Exploring' section slides in "
     "from the left with bold, vivid blue accents. Decisive transformation."),

    ("19_optimize.png",
     "The five priorities reveal one by one from top to bottom. Blue checkboxes "
     "appear as bullet markers with a sharp, clinical flash. "
     "Text is perfectly aligned to the modular grid. Systematic and clear."),

    ("20_cta.png",
     "The final headline fades in with a confident, centered presence. "
     "Subtle parallax makes the core message feel alive. "
     "A thin red rule draws across the bottom as a final period. Decisive closing."),
]

SLIDES_DIR = Path("slides_v3_16x9")
VIDEOS_DIR = Path("videos_v4")


def check_setup() -> bool:
    """Verify prerequisites."""
    print("=== Pre-flight checks ===")
    ok = True
    for fname, _ in SLIDES:
        p = SLIDES_DIR / fname
        if p.exists():
            print(f"  ✓ {fname} ({p.stat().st_size // 1024} KB)")
        else:
            print(f"  ✗ MISSING: {fname}")
            ok = False

    try:
        api_key = os.getenv("GEMINI_KEY")
        if api_key:
            genai.Client(api_key=api_key)
            print("  ✓ Google AI Studio client OK (using GEMINI_KEY)")
        else:
            project_id = os.getenv("PROJECT_NUMBER") or os.getenv("PROJECT_NAME", "videogeneration-484813").split('/')[-1]
            location = os.getenv("GCP_LOCATION", "us-central1")
            genai.Client(vertexai=True, project=project_id, location=location)
            print(f"  ✓ Vertex AI client OK (Project: {project_id})")
    except Exception as e:
        print(f"  ✗ Client error: {e}")
        ok = False

    if os.system("ffmpeg -version > /dev/null 2>&1") == 0:
        print("  ✓ ffmpeg OK")
    else:
        print("  ✗ ffmpeg missing")
        ok = False

    return ok


def generate_video(
    client: genai.Client,
    slide_path: Path,
    prompt: str,
    output_path: Path,
    slide_num: int,
    total: int,
) -> bool:
    """Generate one video via Veo 3.1."""
    full_prompt = SWISS_PREAMBLE + prompt
    print(f"\n--- Slide {slide_num}/{total}: {slide_path.name} ---")
    print(f"  Prompt ({len(full_prompt)} chars): {prompt[:100]}...")

    with open(slide_path, "rb") as f:
        image_bytes = f.read()

    image = types.Image(image_bytes=image_bytes, mime_type="image/png")

    try:
        print("  Submitting to Veo 3.1...")
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=full_prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9",
                resolution="720p",
                duration_seconds=8,
                person_generation="allow_adult",
            ),
        )

        poll = 0
        while not operation.done:
            poll += 1
            print(f"  Polling... ({poll})")
            time.sleep(15)
            operation = client.operations.get(operation)

        gv = operation.response.generated_videos
        if not gv or len(gv) == 0:
            print("  ✗ No generated_videos in response")
            return False

        video = gv[0].video
        saved = False

        # Method 1: Direct video_bytes
        if getattr(video, "video_bytes", None):
            with open(output_path, "wb") as f:
                f.write(video.video_bytes)
            saved = True
            print("  Downloaded via video_bytes")

        # Method 2: SDK save
        if not saved:
            try:
                video.save(str(output_path))
                if output_path.exists() and output_path.stat().st_size > 0:
                    saved = True
                    print("  Downloaded via video.save()")
            except Exception as e:
                print(f"  video.save() failed: {e}")

        # Method 3: GCS URI
        if not saved and getattr(video, "uri", None) and video.uri.startswith("gs://"):
            os.system(f"gsutil cp '{video.uri}' '{output_path}'")
            if output_path.exists():
                saved = True
                print("  Downloaded via gsutil")

        if saved:
            print(f"  ✓ Saved ({output_path.stat().st_size // 1024} KB)")
            return True
        else:
            print("  ✗ All download methods failed")
            return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def concatenate(video_dir: Path, output: Path, total: int) -> bool:
    """Concatenate slide videos into final presentation."""
    print("\n=== Concatenating ===")
    concat_file = video_dir / "concat_list.txt"
    with open(concat_file, "w") as f:
        for i in range(1, total + 1):
            f.write(f"file 'slide_{i:02d}.mp4'\n")

    cmd = f"ffmpeg -y -f concat -safe 0 -i {concat_file} -c copy {output}"
    result = os.system(cmd)
    if result == 0 and output.exists():
        mb = output.stat().st_size / (1024 * 1024)
        print(f"  ✓ {output} ({mb:.1f} MB)")
        return True
    print(f"  ✗ Concatenation failed (exit {result})")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate V4.1 Swiss Style presentation with Veo 3.1 (motion-only prompts)"
    )
    parser.add_argument("--check", action="store_true", help="Pre-flight only")
    parser.add_argument("--start-from", type=int, default=1, help="Start from slide N")
    parser.add_argument("--only", type=int, default=0, help="Generate only slide N")
    parser.add_argument("--no-concat", action="store_true", help="Skip concatenation")
    args = parser.parse_args()

    if args.check:
        sys.exit(0 if check_setup() else 1)

    VIDEOS_DIR.mkdir(exist_ok=True)

    api_key = os.getenv("GEMINI_KEY")
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        project_id = os.getenv("PROJECT_NUMBER") or os.getenv("PROJECT_NAME", "videogeneration-484813").split('/')[-1]
        location = os.getenv("GCP_LOCATION", "us-central1")
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )

    total = len(SLIDES)
    success = 0

    for i, (slide_file, prompt) in enumerate(SLIDES, 1):
        if args.only and i != args.only:
            continue
        if i < args.start_from:
            continue

        slide_path = SLIDES_DIR / slide_file
        output_path = VIDEOS_DIR / f"slide_{i:02d}.mp4"

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"\n  Slide {i} exists, skipping.")
            success += 1
            continue

        if generate_video(client, slide_path, prompt, output_path, i, total):
            success += 1
        else:
            print(f"\n  ⚠ Slide {i} failed. Retry with --start-from {i}")

    print(f"\n=== Generated {success}/{total} ===")

    if not args.no_concat:
        all_exist = all(
            (VIDEOS_DIR / f"slide_{i:02d}.mp4").exists() for i in range(1, total + 1)
        )
        if all_exist:
            concatenate(VIDEOS_DIR, Path("presentation_v4.mp4"), total)
        else:
            missing = [
                i for i in range(1, total + 1)
                if not (VIDEOS_DIR / f"slide_{i:02d}.mp4").exists()
            ]
            print(f"  Missing: {missing}")


if __name__ == "__main__":
    main()

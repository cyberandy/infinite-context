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

from google import genai
from google.genai import types


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
     "Gentle slow zoom into the slide from slightly wider framing. "
     "The large title text remains sharp and static. "
     "A thin red horizontal line draws in from the left edge. "
     "Subtle parallax between the large number and the title. "
     "Elegant, minimal reveal."),

    ("02_context.png",
     "The slide content fades in gently from transparent to fully visible. "
     "The horizontal bar diagram fills in with a smooth left-to-right "
     "animation, the highlighted section appearing first. "
     "Very subtle micro-parallax. Clean, restrained."),

    ("03_quadratic.png",
     "The bar chart elements animate: bars grow upward smoothly from "
     "the baseline. The short bar appears first, then the tall bar grows "
     "dramatically taller. Network diagram nodes gently pulse once. "
     "Minimal, analytical, data-visualization feel."),

    ("04_race.png",
     "The staircase chart draws in step by step from left to right, "
     "each step appearing in sequence. The final tallest step gains "
     "a subtle glow or highlight. Smooth, clean timing. "
     "Restrained, editorial chart animation."),

    # ── Ch 2: Architecture ──
    ("05_ch2_title.png",
     "Gentle slow zoom into the slide. "
     "A thin red horizontal line draws in from the left edge. "
     "Subtle parallax between the large number and the title below it. "
     "Minimal, elegant chapter reveal. Same feel as opening slide."),

    ("06_stretching.png",
     "Three rows of content appear one by one with subtle slide-in "
     "from the left, staggered timing. Each row settles precisely "
     "on the grid. Thin hairline separators draw in. "
     "Clean sequential reveal, no bounce."),

    ("07_ceiling.png",
     "The line chart curve draws smoothly from left to right. "
     "The curve plateaus, then bends downward. "
     "A red indicator point appears at the inflection. "
     "Minimal, analytical data animation. Locked-off camera."),

    ("08_tworoutes.png",
     "Two-column layout reveals sequentially: left column content "
     "fades in first, then the vertical dividing line draws downward, "
     "then right column fades in. Balanced, deliberate timing. "
     "Clean separation, Swiss grid discipline."),

    # ── Ch 3: Memory ──
    ("09_ch3_title.png",
     "Gentle slow zoom into the slide. "
     "A thin red horizontal line draws in from the left edge. "
     "Subtle parallax between the large number and the title. "
     "Minimal, elegant chapter reveal."),

    ("10_virtual.png",
     "Three horizontal bars slide in from the left with staggered "
     "timing, each one slightly longer than the previous. "
     "They lock precisely onto the grid. "
     "Clean, modular, systematic animation."),

    ("11_rag.png",
     "Flow diagram arrows draw in from left to right in sequence. "
     "Each element in the chain appears after the arrow reaches it. "
     "Smooth, logical left-to-right reveal. "
     "Clean, minimal, analytical."),

    ("12_rlm.png",
     "Two-column comparison reveals: left side slides in from left, "
     "pause, then right side slides in from right. "
     "Arrow between them draws last. "
     "Clean Swiss grid structure, deliberate pacing."),

    # ── Ch 4: Recursion ──
    ("13_ch4_title.png",
     "Gentle slow zoom into the slide. "
     "A thin red horizontal line draws in from the left edge. "
     "Subtle parallax between the large number and the title. "
     "Minimal, elegant chapter reveal."),

    ("14_howrlm.png",
     "Flow diagram animates: left box appears first, then an arrow "
     "draws rightward to the second box. A return arrow draws below "
     "going leftward. Smooth sequential reveal of the flow. "
     "Clean, technical, restrained."),

    ("15_paper.png",
     "The circular flow diagram draws clockwise, each step appearing "
     "in sequence around the circle. The center label fades in last. "
     "Smooth, continuous rotational drawing motion. "
     "Analytical, clean."),

    ("16_results.png",
     "Large data numbers fade in with subtle scale-up animation. "
     "Then a bordered box draws its outline around the key statistic. "
     "Clean reveal hierarchy: headline, data, then callout box. "
     "Minimal, confident, editorial."),

    # ── Ch 5: The SEO Playbook ──
    ("17_ch5_title.png",
     "Gentle slow zoom into the slide. "
     "A thin red horizontal line draws in from the left edge. "
     "Subtle parallax between the large number and the title. "
     "Minimal, elegant chapter reveal."),

    ("18_oldnew.png",
     "Top section fades in first, appearing muted and desaturated. "
     "A strikethrough line draws across it. Then the bottom section "
     "slides in from left, appearing bold and vivid. "
     "Clean before-and-after juxtaposition."),

    ("19_optimize.png",
     "Five list items appear one by one from top to bottom, each "
     "sliding in from the left with clean stagger. Small red squares "
     "appear as bullet markers just before each line settles. "
     "Systematic, precise, grid-aligned."),

    ("20_cta.png",
     "The large headline fades in with a subtle float-up. "
     "Body text fades in softer after a brief pause. "
     "A thin red horizontal rule draws from left to right at the bottom. "
     "Confident, final, decisive closing slide."),
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
        genai.Client(vertexai=True, project="videogeneration-484813", location="us-central1")
        print("  ✓ Vertex AI client OK")
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

    client = genai.Client(
        vertexai=True,
        project="videogeneration-484813",
        location="us-central1",
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

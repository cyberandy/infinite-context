#!/usr/bin/env python3
"""
Generate V4 presentation videos in strict Swiss International Typographic Style.

Uses Veo 3.1 on Vertex AI to animate existing slide PNGs with restrained,
grid-disciplined motion prompts.

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
SWISS_PREAMBLE = (
    "A 16:9 presentation slide in strict Swiss International Typographic Style. "
    "White background, modular grid, asymmetric flush-left layout. "
    "Neo-grotesk sans-serif typography similar to Helvetica. "
    "Black text, cool gray secondary, single vivid red accent only when "
    "functionally needed. No centered text, no decorative elements, no icons, "
    "no gradients, no shadows. Print-poster editorial clarity. "
    "Locked-off frontal camera, very subtle fade-in and micro-parallax motion only. "
    "Museum-grade modernist design system. ENGLISH TEXT ONLY. "
)

# ── 20 slides: (source_filename, animation_prompt_suffix) ──
SLIDES = [
    # ── Ch 1: Infinite Context ──
    ("01_ch1_title.png",
     "Oversized flush-left chapter number '01' in light gray at top-left. "
     "Title 'Infinite Context' flush-left in black, bold, very large, below the number. "
     "A single thin red horizontal rule draws in slowly from the left edge. "
     "Tiny label 'Andrea Volpini · WordLift' bottom-left in light gray. "
     "Elements fade in sequentially on the modular grid. Restrained, elegant."),

    ("02_context.png",
     "Flush-left headline 'What Is Context?' in bold black at top-left. "
     "Below on the grid: a clean horizontal bar diagram. A narrow black rectangle "
     "labeled 'visible' occupies the left portion of a longer gray bar labeled "
     "'context window'. Tiny caption 'The working memory of a language model.' "
     "flush-left in gray at bottom-left. The black bar fills in with gentle "
     "linear animation from left to right."),

    ("03_quadratic.png",
     "Flush-left headline 'The Quadratic Wall' in bold black at top-left. "
     "Minimal bar chart on the grid: one short black bar labeled 'N tokens', "
     "one tall red bar labeled '2N tokens = 4x cost'. Thin gray grid lines. "
     "Flush-left caption 'Doubling context quadruples the cost.' in small gray text. "
     "Clean chart-drawing animation, bars grow upward from baseline."),

    ("04_race.png",
     "Flush-left headline 'The Context Race' in bold black at top-left. "
     "Staircase step chart with thin black lines ascending right: "
     "2020: 2K, 2022: 32K, 2023: 128K, 2024: 2M, 2026: 10M+. "
     "The final 10M+ step highlighted with solid red fill. "
     "Caption 'But is more context window enough?' flush-left in gray. "
     "Stairs draw in step by step, left to right."),

    # ── Ch 2: Architecture ──
    ("05_ch2_title.png",
     "Oversized flush-left chapter number '02' in light gray at top-left. "
     "Title 'Architecture' flush-left in black, bold, very large. "
     "A single thin red horizontal rule draws in from the left edge. "
     "Same grid system as chapter 1. Elements fade in sequentially."),

    ("06_stretching.png",
     "Flush-left headline 'Stretching the Window' in bold black at top-left. "
     "Three clean text rows flush-left, separated by thin gray hairlines: "
     "'Compressive Memory — Infini-attention', "
     "'State Space Models — Mamba · SAMBA', "
     "'RoPE Scaling — LongRoPE2'. "
     "No icons. Caption 'Three ways to rewire the brain for more input.' "
     "Rows slide in one by one from left with subtle stagger."),

    ("07_ceiling.png",
     "Flush-left headline 'The Ceiling' in bold black at top-left. "
     "Clean line chart with thin black axes: accuracy curve plateaus then "
     "curves downward. A single red dot marks the inflection point with tiny "
     "red label 'Context Rot'. Caption 'More input does not mean better "
     "understanding.' flush-left in gray. Line draws smoothly left to right."),

    ("08_tworoutes.png",
     "Flush-left headline 'Two Routes' in bold black at top-left. "
     "Two-column layout with a thin vertical black divider line. "
     "Left column: 'Architectural' in bold black, 'Bigger brain' in gray below. "
     "Right column: 'Philosophical' in bold black, 'Smarter memory' in gray below. "
     "Caption 'Neither solved it alone.' flush-left in bold. "
     "Left column fades in, then right column fades in."),

    # ── Ch 3: Memory ──
    ("09_ch3_title.png",
     "Oversized flush-left chapter number '03' in light gray at top-left. "
     "Title 'Memory' flush-left in black, bold, very large. "
     "A single thin red horizontal rule draws in from the left edge. "
     "Same strict grid system. Elements fade in sequentially."),

    ("10_virtual.png",
     "Flush-left headline 'Virtual Memory for LLMs' in bold black at top-left. "
     "Three clean horizontal bars stacked flush-left with different widths: "
     "small black bar 'Main Context (RAM)', medium gray bar 'Recall Storage (Cache)', "
     "large light-gray bar 'Archival (Vector DB)'. "
     "Red label 'Letta / MemGPT' flush-left. "
     "Caption 'Small fast window, unbounded system memory.' "
     "Bars slide in from left, staggered timing."),

    ("11_rag.png",
     "Flush-left headline 'Give It a Search Bar' in bold black at top-left, "
     "spanning two lines. Clean horizontal flow diagram with thin black arrows: "
     "'Query' then arrow then 'Database' then arrow then 'LLM'. "
     "Red label 'Retrieval-Augmented Generation' flush-left below diagram. "
     "Caption 'Fetch only what is relevant.' Flow draws left to right."),

    ("12_rlm.png",
     "Flush-left headline 'Enter Recursive Language Models' in bold black, "
     "spanning two lines at top-left. Two-column comparison below: "
     "left flush 'Standard LLM' bold with 'Speed reader' in gray, "
     "right 'RLM' bold with 'Librarian' in red. Thin black dividing rule between. "
     "Caption 'Context as an environment to explore, not a buffer to fill.' "
     "Elements slide in left then right."),

    # ── Ch 4: Recursion ──
    ("13_ch4_title.png",
     "Oversized flush-left chapter number '04' in light gray at top-left. "
     "Title 'Recursion' flush-left in black, bold, very large. "
     "A single thin red horizontal rule draws in from the left edge. "
     "Same grid system. Elements fade in sequentially."),

    ("14_howrlm.png",
     "Flush-left headline 'How RLMs Work' in bold black at top-left. "
     "Clean flow diagram on the grid: rectangular box 'LLM' left, "
     "thin black arrow labeled 'writes code' pointing right to rectangular box "
     "'External REPL'. Return arrow below labeled 'Results'. "
     "Red method labels 'search() · partition() · peek()' inside REPL box. "
     "Caption 'The model explores programmatically, not by memorizing.' "
     "Arrows draw in sequence, left to right then return."),

    ("15_paper.png",
     "Flush-left oversized headline 'RLM-on-KG' in bold black at top-left. "
     "Red subtitle 'Autonomous navigator over RDF knowledge graph' flush-left. "
     "Clean circular flow diagram below: Seed then Expand then Verify then "
     "Collect then Re-rank, connected by thin black arrows. "
     "Center label '9 tools' in gray. "
     "Caption 'Entity-first exploration over structured data.' "
     "Circle draws clockwise with smooth animation."),

    ("16_results.png",
     "Flush-left headline 'Results' in bold black at top-left. "
     "Large flush-left data display: 'F1: 45.8' in large bold black, "
     "'F1: 45.6' in large gray, separated by a thin vertical black rule. "
     "Below: red-outlined box containing '56 percent win rate when evidence "
     "scattered across 11+ chunks'. "
     "Caption 'RLMs win when structure matters most.' in bold. "
     "Numbers fade in, then stat box draws its red border."),

    # ── Ch 5: The SEO Playbook ──
    ("17_ch5_title.png",
     "Oversized flush-left chapter number '05' in light gray at top-left. "
     "Title 'The SEO Playbook' flush-left in black, bold, very large. "
     "A single thin red horizontal rule draws in from the left edge. "
     "Same grid system. Elements fade in sequentially."),

    ("18_oldnew.png",
     "Flush-left headline 'From Crawl-Index-Rank to Explore-Verify-Cite' "
     "in bold black at top-left, spanning two lines. "
     "Old pipeline in gray with strikethrough: 'Crawl → Index → Rank', "
     "small gray label 'The old pipeline' below. "
     "New pipeline in bold black: 'Explore → Verify → Cite' with red arrow "
     "accents, small label 'The new paradigm' below. "
     "Caption 'AI agents navigate structured data.' flush-left. "
     "Old text fades in then gets crossed out, new text slides in from left."),

    ("19_optimize.png",
     "Flush-left headline 'What to Optimize' in bold black at top-left. "
     "Five flush-left text items separated by thin gray hairlines, each "
     "preceded by a small solid red square: "
     "'Stable URIs', 'Mention Links', 'Provenance Anchors', "
     "'Entity Pages', 'Crawlable Endpoints'. "
     "Caption 'Make your content navigable, not just embeddable.' "
     "Items slide in one by one from left with clean stagger."),

    ("20_cta.png",
     "Flush-left oversized headline 'Structure Is the New Moat' in bold black, "
     "positioned upper-left on the grid. Body text in gray flush-left below: "
     "'Connected data compounds in value under scaffolding. Schema.org, "
     "Knowledge Graphs, entity markup — these are the surfaces agents explore.' "
     "A thin red horizontal rule separates the credit line below: "
     "'Andrea Volpini · WordLift' in black and "
     "'github.com/wordlift/rlm-on-kg' in small gray, both flush-left. "
     "Gentle fade-in for text, then rule draws from left."),
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
        description="Generate V4 Swiss Style presentation with Veo 3.1"
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

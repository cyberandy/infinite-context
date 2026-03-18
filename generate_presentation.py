#!/usr/bin/env python3
"""
Generate a video presentation from slide images using Veo 3.1.

V2: 27 slides across 8 chapters, style progression:
Swiss Minimalism → Bauhaus → Russian Futurism.

Usage:
    python generate_presentation.py [--check] [--start-from N] [--only N]

Requires:
    - google-genai SDK
    - gcloud auth application-default login (ADC)
    - ffmpeg (for concatenation)
"""

import argparse
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types


# --- 27 slides: slide filename -> animation prompt ---
CHAPTERS = [
    # ── Ch 1: What Is Context? (Swiss Minimalism) ──
    {
        "slide": "01a_context.png",
        "prompt": (
            "Slow elegant zoom into a clean white presentation slide. "
            "A context window bar gradually fills with teal tokens from left to right. "
            "Swiss minimalist design, Helvetica typography, subtle parallax. "
            "Professional academic tone. No people."
        ),
    },
    {
        "slide": "01b_bottleneck.png",
        "prompt": (
            "Camera gently pans over a minimalist diagram of the quadratic bottleneck. "
            "Token connections animate as thin lines, the cost bar grows dramatically. "
            "'4x cost' text pulses in red-orange. Clean grid background. No people."
        ),
    },
    {
        "slide": "01c_twocamps.png",
        "prompt": (
            "Split-screen reveal: left column 'Architectural' fades in first, then "
            "right column 'Philosophical'. Neural network and system design icons "
            "animate subtly. Clean Swiss grid, teal accents. No people."
        ),
    },
    # ── Ch 2: The Architectural Route (Swiss Minimalism) ──
    {
        "slide": "02a_gated.png",
        "prompt": (
            "Gentle animation of two data streams flowing toward a central gate valve. "
            "Local Attention stream glows teal, Compressed Memory stream fades from "
            "detailed to abstract. Gate opens and merges them. Clean white background. "
            "No people."
        ),
    },
    {
        "slide": "02b_ssm.png",
        "prompt": (
            "Tokens flow left to right through a continuous state bar. Green checkmarks "
            "appear on kept tokens, gray X marks on forgotten ones. Smooth flowing "
            "animation. Clean minimalist design. No people."
        ),
    },
    {
        "slide": "02c_rope.png",
        "prompt": (
            "A spring stretches smoothly from left (8K) to right (1M+). Warning icon "
            "appears near the end labeled 'Context Rot'. Teal and red-orange colors. "
            "Clean Swiss design. No people."
        ),
    },
    {
        "slide": "02d_timeline.png",
        "prompt": (
            "Ascending staircase chart animates step by step: 2K, 32K, 128K, 2M, "
            "then the massive 10M+ step rises dramatically with a teal glow. "
            "Question appears: 'But is more context window enough?' No people."
        ),
    },
    # ── Ch 3: The Philosophical Route (Swiss → Bauhaus) ──
    {
        "slide": "03a_virtual.png",
        "prompt": (
            "LLM chip icon connects to three storage layers that slide in one by one. "
            "Main Context (small green), Recall Storage (blue), Archival (large gray). "
            "Data arrows pulse between them. Subtle geometric accents appear. No people."
        ),
    },
    {
        "slide": "03b_rag.png",
        "prompt": (
            "Encyclopedia gets crossed out with dramatic X, then search bar appears. "
            "A chunk of data pulls from database to LLM. Bauhaus geometric elements "
            "emerge in corners. Dynamic, revealing animation. No people."
        ),
    },
    {
        "slide": "03c_enough.png",
        "prompt": (
            "A question mark made of two halves rotates slowly — neural network meets "
            "system diagram. Bauhaus colored blocks build up around edges. "
            "'Enter Recursive Language Models' text appears in red. No people."
        ),
    },
    # ── Ch 4: Recursive Language Models (Bauhaus) ──
    {
        "slide": "04a_paradigm.png",
        "prompt": (
            "Bold Bauhaus-style animation. Left side: chaotic stack of books and pages "
            "flying apart, overwhelming text fragments, labeled 'Standard LLM'. Right side: "
            "calm organized card catalog with neatly arranged drawers, labeled 'RLM'. "
            "Primary color geometric shapes drift. Caption animates: 'From speed reader "
            "to librarian.' Constructivist visual metaphor. No people."
        ),
    },
    {
        "slide": "04b_howrlm.png",
        "prompt": (
            "LLM brain icon writes code arrows that shoot into External REPL box. "
            "Functions 'search(), partition(), peek()' appear one by one. Results "
            "flow back. Bauhaus geometric framing. Energetic. No people."
        ),
    },
    {
        "slide": "04c_recursion.png",
        "prompt": (
            "Root LLM node pulses red, then sends arrows down to three blue Sub-LLM "
            "nodes. Each analyzes a chunk, then sends clean results back up. Shield "
            "'No Context Rot' glows. Bauhaus colors. No people."
        ),
    },
    {
        "slide": "04d_inference.png",
        "prompt": (
            "Camera pans from left (massive expensive building with dollar signs, X'd out) "
            "to right (compact model with tools: hammer, magnifying glass, clock). "
            "Arrow sweeps: 'More thinking, not more parameters.' Bauhaus style. No people."
        ),
    },
    # ── Ch 5: Scaffolding (Bauhaus) ──
    {
        "slide": "05a_whatscaff.png",
        "prompt": (
            "Three interlocking gears animate: yellow Tools, blue Memory, red Reasoning "
            "Loops. They combine into a larger AI System. Building and modularity theme. "
            "Bauhaus primary colors. No people."
        ),
    },
    {
        "slide": "05b_search.png",
        "prompt": (
            "An LLM at center controls a search loop. Arrows rotate through "
            "Query → Retrieve → Evaluate → Refine cycle. Each step highlights "
            "in sequence. Bauhaus colors, energetic. No people."
        ),
    },
    {
        "slide": "05c_compound.png",
        "prompt": (
            "Three columns grow upward like compound interest: yellow Structured Data, "
            "blue Entity Handles, red Tool APIs. Upward arrow shows compounding value. "
            "Growth animation. Bauhaus constructivist style. No people."
        ),
    },
    # ── Ch 6: From Indexes to Tools (Bauhaus → Russian Futurism) ──
    {
        "slide": "06a_oldworld.png",
        "prompt": (
            "Gray desaturated slide with fading 'Crawl → Index → Rank' pipeline. "
            "A dramatic red diagonal wedge sweeps in from bottom-right, disrupting "
            "the old world. Transition from Bauhaus to Constructivism. No people."
        ),
    },
    {
        "slide": "06b_newworld.png",
        "prompt": (
            "Bold black and red composition. 'Explore → Verify → Cite' text "
            "slashes across the frame. Constructivist arrows and wedge shapes "
            "create dynamic energy. Dramatic reveal. No people."
        ),
    },
    {
        "slide": "06c_seos.png",
        "prompt": (
            "Three rows animate in — Schema.org Markup, Knowledge Graphs, Entity "
            "Endpoints — each with an arrow pointing to an agent robot icon. "
            "Dark background, red and teal accents. Russian Constructivist energy. No people."
        ),
    },
    # ── Ch 7: RLM-on-KG (Russian Futurism) ──
    {
        "slide": "07a_paper.png",
        "prompt": (
            "Knowledge graph network pulses with orange light at center. 9 tool icons "
            "appear in a semicircle around it. Bold 'RLM-on-KG' title dominates. "
            "Red and orange constructivist wedges. Dark background. No people."
        ),
    },
    {
        "slide": "07b_loop.png",
        "prompt": (
            "Circular retrieval loop animates: Seed → Expand → Verify → Collect → Re-rank. "
            "Each step lights up in sequence, rotating through the cycle. Center text: "
            "'Each stage = GEO optimization target.' Dark background, red/orange. No people."
        ),
    },
    {
        "slide": "07c_results.png",
        "prompt": (
            "Stats animate in dramatically: 'F1: 45.8 vs 45.6' in white, then "
            "'56% win rate at 11+ scattered chunks' in orange. Win-tie-loss bar "
            "fills in from left. Constructivist angles. Dark background. No people."
        ),
    },
    {
        "slide": "07d_insight.png",
        "prompt": (
            "Large quote fades in: 'Separate discovery from ranking.' Then below: "
            "'Let the LLM explore. Let the vectors decide.' Red diagonal accents "
            "frame the text. Knowledge graph fades in background. Dramatic. No people."
        ),
    },
    # ── Ch 8: Structure Is the New Moat (Russian Futurism) ──
    {
        "slide": "08a_diagnostics.png",
        "prompt": (
            "Four diagnostic boxes animate in with orange/red constructivist shapes: "
            "Coverage, Connectivity, Provenance, Queryability. Bold diagonal lines "
            "streak behind. Dark background. No people."
        ),
    },
    {
        "slide": "08b_optimize.png",
        "prompt": (
            "Checklist items reveal one by one with red checkmarks: Stable URIs, "
            "Mention Links, Provenance Anchors, Entity Pages, Crawlable Endpoints. "
            "Each check appears with a satisfying animation. Dark background. No people."
        ),
    },
    {
        "slide": "08c_cta.png",
        "prompt": (
            "Maximum impact finale. Red diagonal wedge sweeps dramatically. Massive "
            "white letters: 'STRUCTURE IS THE NEW MOAT'. Red star glows. Camera slowly "
            "pulls back. Credits: Andrea Volpini, WordLift. Decisive ending. No people."
        ),
    },
]


def check_setup(slides_dir: Path) -> bool:
    """Verify all prerequisites are met."""
    print("=== Pre-flight checks ===")
    all_good = True
    for ch in CHAPTERS:
        slide_path = slides_dir / ch["slide"]
        if slide_path.exists():
            print(f"  ✓ {ch['slide']} ({slide_path.stat().st_size // 1024} KB)")
        else:
            print(f"  ✗ MISSING: {ch['slide']}")
            all_good = False

    try:
        client = genai.Client(
            vertexai=True,
            project="videogeneration-484813",
            location="us-central1",
        )
        print("  ✓ google-genai client initialized (Vertex AI)")
    except Exception as e:
        print(f"  ✗ google-genai client error: {e}")
        all_good = False

    if os.system("ffmpeg -version > /dev/null 2>&1") == 0:
        print("  ✓ ffmpeg available")
    else:
        print("  ✗ ffmpeg not found")
        all_good = False

    return all_good


def generate_video_for_slide(
    client: genai.Client,
    slide_path: Path,
    prompt: str,
    output_path: Path,
    slide_num: int,
) -> bool:
    """Generate a video from a slide image using Veo 3.1."""
    print(f"\n--- Slide {slide_num}/{len(CHAPTERS)}: {slide_path.name} ---")
    print(f"  Prompt: {prompt[:80]}...")

    with open(slide_path, "rb") as f:
        image_bytes = f.read()

    image = types.Image(image_bytes=image_bytes, mime_type="image/png")

    try:
        print("  Submitting to Veo 3.1...")
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9",
                resolution="720p",
                duration_seconds=8,
                person_generation="dont_allow",
            ),
        )

        poll_count = 0
        while not operation.done:
            poll_count += 1
            print(f"  Waiting... (poll #{poll_count})")
            time.sleep(15)
            operation = client.operations.get(operation)

        # Download the generated video
        generated_video = operation.response.generated_videos[0]
        video = generated_video.video

        saved = False

        # Method 1: Direct video_bytes
        if getattr(video, 'video_bytes', None):
            with open(output_path, 'wb') as f:
                f.write(video.video_bytes)
            saved = True
            print("  Downloaded via video_bytes")

        # Method 2: Save method
        if not saved:
            try:
                video.save(str(output_path))
                if output_path.exists() and output_path.stat().st_size > 0:
                    saved = True
                    print("  Downloaded via video.save()")
            except Exception as e:
                print(f"  video.save() failed: {e}")

        # Method 3: GCS URI via gsutil
        if not saved and getattr(video, 'uri', None) and video.uri.startswith('gs://'):
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


def concatenate_videos(video_dir: Path, output_path: Path) -> bool:
    """Concatenate all slide videos into final presentation."""
    print("\n=== Concatenating videos ===")
    video_files = sorted(video_dir.glob("slide_*.mp4"))
    if not video_files:
        print("  ✗ No slide videos found!")
        return False

    concat_file = video_dir / "concat_list.txt"
    with open(concat_file, "w") as f:
        for vf in video_files:
            f.write(f"file '{vf.name}'\n")

    print(f"  Concatenating {len(video_files)} videos...")
    cmd = f"ffmpeg -y -f concat -safe 0 -i {concat_file} -c copy {output_path}"
    result = os.system(cmd)

    if result == 0 and output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ Final video: {output_path} ({size_mb:.1f} MB)")
        return True
    else:
        print(f"  ✗ Concatenation failed (exit code {result})")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate V2 video presentation with Veo 3.1")
    parser.add_argument("--check", action="store_true", help="Pre-flight checks only")
    parser.add_argument("--slides-dir", default="slides", help="Slide images directory")
    parser.add_argument("--output-dir", default="videos", help="Output videos directory")
    parser.add_argument("--start-from", type=int, default=1, help="Start from slide N")
    parser.add_argument("--only", type=int, default=0, help="Generate only slide N")
    parser.add_argument("--no-concat", action="store_true", help="Skip concatenation")
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.check:
        ok = check_setup(slides_dir)
        sys.exit(0 if ok else 1)

    client = genai.Client(
        vertexai=True,
        project="videogeneration-484813",
        location="us-central1",
    )

    successes = 0
    total = len(CHAPTERS)
    for i, chapter in enumerate(CHAPTERS, 1):
        if args.only and i != args.only:
            continue
        if i < args.start_from:
            print(f"  Skipping slide {i}")
            successes += 1
            continue

        slide_path = slides_dir / chapter["slide"]
        output_path = output_dir / f"slide_{i:02d}.mp4"

        if output_path.exists():
            print(f"\n  Slide {i} exists, skipping.")
            successes += 1
            continue

        if generate_video_for_slide(client, slide_path, chapter["prompt"], output_path, i):
            successes += 1
        else:
            print(f"\n  ⚠ Slide {i} failed. Retry with --start-from {i}")

    print(f"\n=== Generated {successes}/{total} slide videos ===")

    if not args.no_concat and successes == total:
        concatenate_videos(output_dir, Path("presentation_v2.mp4"))
    elif successes < total:
        print("  Skipping concatenation (not all slides generated)")


if __name__ == "__main__":
    main()

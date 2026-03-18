#!/usr/bin/env python3
"""Generate V3 presentation videos from 16:9 slides using Veo 3.1."""

import os, sys, time
from pathlib import Path
from google import genai
from google.genai import types

# Slide definitions: (filename, animation_prompt)
SLIDES = [
    ("01_ch1_title.png",
     "Dark chapter card with bold white text '01 INFINITE CONTEXT' slowly zooms in. "
     "Red wedge accent pulses subtly. Blue triangle glows. Dramatic, cinematic."),
    ("02_context.png",
     "Clean white slide. Brain icon connects to context window bar. The 'visible' "
     "blue section highlights and pulses. Text 'What Is Context?' fades in cleanly."),
    ("03_quadratic.png",
     "Network diagram nodes light up. Bar chart animates: small blue bar appears, "
     "then tall red-orange bar grows dramatically. Title and subtitle fade in."),
    ("04_race.png",
     "Staircase chart animates step by step: 2K, 32K, 128K, 2M. Final 10M+ step "
     "rises dramatically with blue glow. Question appears at bottom."),
    ("05_ch2_title.png",
     "Dark chapter card with '02 ARCHITECTURE' text. Red wedge swoops across. "
     "Blue triangle accent appears. Bold, dramatic, cinematic zoom."),
    ("06_stretching.png",
     "Three rows appear one by one: brain + Compressive Memory, wave + State Space "
     "Models, spring + RoPE Scaling. Blue labels fade in after each."),
    ("07_ceiling.png",
     "Line chart animates: accuracy line holds steady then curves downward. "
     "Warning icon appears at 'Context Rot' point. Clean, data-driven."),
    ("08_tworoutes.png",
     "Two-column split animates: left column slides in with neural network icon, "
     "right column with database. Blue dividing line draws down center."),
    ("09_ch3_title.png",
     "Dark chapter card '03 MEMORY'. Red lightning wedge accent pulses. "
     "Blue circle glows. Bold typography, cinematic."),
    ("10_virtual.png",
     "LLM chip icon appears. Three memory bars slide in: green Main Context, "
     "blue Recall Storage, gray Archival. Letta/MemGPT label fades in."),
    ("11_rag.png",
     "Encyclopedia gets crossed out. Search bar appears with magnifying glass. "
     "Arrow chain: search → database → LLM brain. RAG label in blue."),
    ("12_rlm.png",
     "Left side: chaotic books and reading figure. Arrow transforms to right side: "
     "organized card catalog. Labels appear: Standard LLM vs RLM."),
    ("13_ch4_title.png",
     "Dark chapter card '04 RECURSION'. Red lightning bolt accent. "
     "Blue square pulses with energy. Bold, dramatic."),
    ("14_howrlm.png",
     "Flow diagram animates: LLM brain sends 'writes code' arrow to External REPL "
     "box. Function names appear in blue. Results arrow returns."),
    ("15_paper.png",
     "RLM-on-KG title appears in bold. Blue subtitle fades in. Circular flow "
     "diagram draws: Seed → Expand → Verify → Collect → Re-rank. '9 tools' center."),
    ("16_results.png",
     "Stats animate in: F1 45.8 in blue, F1 45.6 in gray. Dividing line draws. "
     "Blue bordered box reveals: 56% win rate. Bold conclusion fades in."),
    ("17_ch5_title.png",
     "Dark chapter card '05 THE SEO PLAYBOOK'. Red wedge accent. Blue star glows. "
     "Bold typography, cinematic. Maximum drama."),
    ("18_oldnew.png",
     "Old pipeline fades in gray with strikethrough. New paradigm appears bold in "
     "blue: Explore → Verify → Cite. Subtitle about AI agents fades in."),
    ("19_optimize.png",
     "Checklist animates: blue check marks appear one by one. Stable URIs, Mention "
     "Links, Provenance Anchors, Entity Pages, Crawlable Endpoints. Bold conclusion."),
    ("20_cta.png",
     "Structure Is the New Moat title appears large and centered. Body text fades in. "
     "Andrea Volpini · WordLift in blue at bottom. Professional closing."),
]

SLIDES_DIR = Path("slides_v3_16x9")
VIDEOS_DIR = Path("videos_v3")


def main():
    VIDEOS_DIR.mkdir(exist_ok=True)

    start_from = 1
    if "--start-from" in sys.argv:
        start_from = int(sys.argv[sys.argv.index("--start-from") + 1])

    client = genai.Client(
        vertexai=True,
        project="videogeneration-484813",
        location="us-central1",
    )

    success = 0
    total = len(SLIDES)

    for i, (slide_file, prompt) in enumerate(SLIDES, 1):
        if i < start_from:
            continue

        slide_path = SLIDES_DIR / slide_file
        output_path = VIDEOS_DIR / f"slide_{i:02d}.mp4"

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"\n--- Slide {i}/{total}: {slide_file} --- (already exists, skipping)")
            success += 1
            continue

        print(f"\n--- Slide {i}/{total}: {slide_file} ---")
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
                    person_generation="allow_adult",
                ),
            )

            poll_count = 0
            while not operation.done:
                poll_count += 1
                print(f"  Waiting... (poll #{poll_count})")
                time.sleep(15)
                operation = client.operations.get(operation)

            gv = operation.response.generated_videos
            if gv and len(gv) > 0:
                video = gv[0].video
                if getattr(video, 'video_bytes', None):
                    with open(output_path, 'wb') as f:
                        f.write(video.video_bytes)
                    print(f"  ✓ Saved ({output_path.stat().st_size // 1024} KB)")
                    success += 1
                else:
                    print("  ✗ No video_bytes")
            else:
                print(f"  ✗ No generated_videos")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\n=== Generated {success}/{total} slide videos ===")

    # Concatenate if all done
    all_exist = all((VIDEOS_DIR / f"slide_{i:02d}.mp4").exists() for i in range(1, total + 1))
    if all_exist:
        print("\nAll videos ready! Concatenating...")
        concat_list = VIDEOS_DIR / "concat_list.txt"
        with open(concat_list, "w") as f:
            for i in range(1, total + 1):
                f.write(f"file 'slide_{i:02d}.mp4'\n")
        os.system(
            f"ffmpeg -y -f concat -safe 0 -i {concat_list} "
            f"-c copy presentation_v3.mp4"
        )
        if Path("presentation_v3.mp4").exists():
            size_mb = Path("presentation_v3.mp4").stat().st_size // (1024 * 1024)
            print(f"✓ presentation_v3.mp4 ({size_mb} MB)")
    else:
        missing = [i for i in range(1, total + 1) if not (VIDEOS_DIR / f"slide_{i:02d}.mp4").exists()]
        print(f"  Missing slides: {missing}")


if __name__ == "__main__":
    main()

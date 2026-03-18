#!/usr/bin/env python3
"""Generate voiceover narration for V3 using Gemini 2.5 Flash TTS, then merge with video."""

import os, sys, time, struct
from pathlib import Path
from google import genai
from google.genai import types

# Per-slide narration text (~6-7s spoken per slide to fit 8s clips)
NARRATION = {
    1:  "",  # Ch1 title card
    2:  "What is context? It's the working memory of a language model. "
        "Everything the model can see at once when generating an answer.",
    3:  "But self-attention has a problem. Every token compares with every other token. "
        "Double the context, and the cost quadruples. This quadratic wall kept "
        "context windows stuck at a few thousand tokens for years.",
    4:  "Then the race began. From two thousand tokens in twenty-twenty, to thirty-two K, "
        "to one twenty-eight K, to two million, and now beyond ten million. "
        "But is more context window really enough?",
    5:  "",  # Ch2 title card
    6:  "Three approaches emerged to stretch the window. Compressive memory "
        "like Infini-attention. State space models like Mamba. And RoPE scaling "
        "like LongRoPE2. Each rewires the architecture for more input.",
    7:  "But there's a ceiling. As context grows, accuracy declines. "
        "This is context rot. More input does not mean better understanding.",
    8:  "So we face two routes. Architectural — build a bigger brain. "
        "Or philosophical — design smarter memory. Neither solved it alone.",
    9:  "",  # Ch3 title card
    10: "What if we treat the LLM like a CPU? Letta, formerly MemGPT, does exactly that. "
        "A small fast context window is the RAM. A recall store is the cache. "
        "And an archival vector database is the disk.",
    11: "Or give it a search bar. Retrieval-Augmented Generation. "
        "Don't stuff the context — let the model fetch only what's relevant. "
        "This is where SEOs first entered the picture.",
    12: "But neither approach was enough alone. Enter Recursive Language Models. "
        "Instead of speed-reading everything, the RLM acts like a librarian. "
        "Context becomes an environment to explore, not a buffer to fill.",
    13: "",  # Ch4 title card
    14: "How do RLMs work? The model writes code — search, partition, peek — "
        "and sends it to an external REPL. Results come back. "
        "The model explores programmatically, not by memorizing.",
    15: "We built RLM-on-KG. An autonomous navigator over an RDF knowledge graph. "
        "Nine tools. Entity-first exploration. A retrieval loop of "
        "seed, expand, verify, collect, and re-rank.",
    16: "The results? F1 forty-five point eight versus GraphRAG's forty-five point six. "
        "Parity overall. But fifty-six percent win rate when evidence is scattered "
        "across eleven or more chunks. RLMs win when structure matters most.",
    17: "",  # Ch5 title card
    18: "The old pipeline — crawl, index, rank — is being replaced. "
        "AI agents don't rank pages. They explore structured data, "
        "verify claims, and cite sources. Explore, verify, cite.",
    19: "What should you optimize? Stable URIs. Mention links. "
        "Provenance anchors. Entity pages. Crawlable endpoints. "
        "Make your content navigable, not just embeddable.",
    20: "Structure is the new moat. Connected data compounds in value "
        "under scaffolding. Schema dot org, knowledge graphs, entity markup. "
        "These are the surfaces agents explore. Thank you.",
}

AUDIO_DIR = Path("audio_v3")
VIDEOS_DIR = Path("videos_v3")
OUTPUT_DIR = Path("videos_v3_narrated")


def save_pcm_as_wav(pcm_data, path, sample_rate=24000):
    """Save raw PCM16 data as a WAV file."""
    with open(path, 'wb') as f:
        num_bytes = len(pcm_data)
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + num_bytes))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<HHIIHH', 1, 1, sample_rate, sample_rate * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', num_bytes))
        f.write(pcm_data)


def generate_audio():
    """Generate TTS audio for each slide using Gemini 2.5 Flash TTS."""
    AUDIO_DIR.mkdir(exist_ok=True)

    client = genai.Client(
        vertexai=True,
        project="videogeneration-484813",
        location="us-central1",
    )

    for slide_num, text in sorted(NARRATION.items()):
        output = AUDIO_DIR / f"slide_{slide_num:02d}.wav"
        if output.exists() and output.stat().st_size > 1000:
            dur_s = (output.stat().st_size - 44) / (24000 * 2)
            print(f"  Slide {slide_num}: already exists ({dur_s:.1f}s), skipping")
            continue

        if not text.strip():
            # 2s silence for title cards
            print(f"  Slide {slide_num}: title card — 2s silence")
            os.system(
                f"ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 2 "
                f"-c:a pcm_s16le {output} 2>/dev/null"
            )
            continue

        print(f"  Slide {slide_num}: generating TTS ({len(text)} chars)...", end=" ", flush=True)

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Kore"  # Professional voice
                            )
                        )
                    ),
                ),
            )
            pcm_data = response.candidates[0].content.parts[0].inline_data.data
            save_pcm_as_wav(pcm_data, str(output))
            dur_s = len(pcm_data) / (24000 * 2)
            print(f"✓ {dur_s:.1f}s")
        except Exception as e:
            print(f"✗ {e}")

    print("\n=== Audio generation complete ===")


def merge_audio_video():
    """Merge audio with video clips."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    for i in range(1, 21):
        video = VIDEOS_DIR / f"slide_{i:02d}.mp4"
        audio = AUDIO_DIR / f"slide_{i:02d}.wav"
        output = OUTPUT_DIR / f"slide_{i:02d}.mp4"

        if output.exists() and output.stat().st_size > 0:
            print(f"  Slide {i}: already merged, skipping")
            continue

        if not video.exists() or not audio.exists():
            miss = "video" if not video.exists() else "audio"
            print(f"  Slide {i}: ✗ missing {miss}")
            continue

        print(f"  Slide {i}: merging...", end=" ", flush=True)

        cmd = (
            f"ffmpeg -y -i {video} -i {audio} "
            f"-c:v copy -c:a aac -b:a 128k "
            f"-filter_complex '[1:a]apad[aout]' -map 0:v -map '[aout]' "
            f"-shortest {output} 2>/dev/null"
        )
        os.system(cmd)

        if output.exists():
            print(f"✓ ({output.stat().st_size // 1024} KB)")
        else:
            print("✗ failed")


def concatenate():
    """Concatenate all narrated clips."""
    concat_list = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for i in range(1, 21):
            clip = OUTPUT_DIR / f"slide_{i:02d}.mp4"
            if clip.exists():
                f.write(f"file '{clip.resolve()}'\n")

    output = Path("presentation_v3_narrated.mp4")
    os.system(
        f"ffmpeg -y -f concat -safe 0 -i {concat_list} "
        f"-c copy {output} 2>/dev/null"
    )
    if output.exists():
        size_mb = output.stat().st_size // (1024 * 1024)
        print(f"\n✓ {output} ({size_mb} MB)")
    else:
        print("\n✗ Concatenation failed")


if __name__ == "__main__":
    print("=== Step 1: Generate TTS audio ===")
    generate_audio()

    print("\n=== Step 2: Merge audio + video ===")
    merge_audio_video()

    print("\n=== Step 3: Concatenate ===")
    concatenate()

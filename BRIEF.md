# Infinite Context — Presentation Brief

## Overview

**Title**: Infinite Context: From Context Windows to Autonomous Retrieval  
**Author**: Andrea Volpini · WordLift  
**Format**: 20 animated slides (16:9, 8 seconds each)  
**Source**: Based on the research paper *RLM-on-KG: Autonomous Retrieval over RDF Knowledge Graphs*

---

## Narrative Arc (5 Chapters, 20 Slides)

### Chapter 1 — Infinite Context (Slides 1–4)

The presentation opens with the fundamental question: *What is a context window?* It's the working memory of a language model — the text the model can "see" at once.

| Slide | Title | Key Message |
|-------|-------|-------------|
| 01 | **Infinite Context** | Chapter title card |
| 02 | **What Is Context?** | The context window is the LLM's working memory — a fixed buffer of visible tokens |
| 03 | **The Quadratic Wall** | Doubling context quadruples the cost (quadratic attention scaling) |
| 04 | **The Context Race** | Context windows grew from 2K (2020) → 32K → 128K → 2M → 10M+ (2026). But is more enough? |

### Chapter 2 — Architecture (Slides 5–8)

Engineering approaches to stretching the window — and why they hit a ceiling.

| Slide | Title | Key Message |
|-------|-------|-------------|
| 05 | **Architecture** | Chapter title card |
| 06 | **Stretching the Window** | Three techniques: Compressive Memory (Infini-attention), State Space Models (Mamba/SAMBA), RoPE Scaling (LongRoPE2) |
| 07 | **The Ceiling** | More input ≠ better understanding. Accuracy plateaus then drops — "Context Rot" |
| 08 | **Two Routes** | Architectural (bigger brain) vs. Philosophical (smarter memory). Neither solved it alone |

### Chapter 3 — Memory (Slides 9–12)

The philosophical shift: instead of cramming more into the window, give the model external memory systems.

| Slide | Title | Key Message |
|-------|-------|-------------|
| 09 | **Memory** | Chapter title card |
| 10 | **Virtual Memory for LLMs** | Letta/MemGPT: small fast window + recall cache + archival vector DB. Unbounded system memory |
| 11 | **Give It a Search Bar** | RAG: Query → Database → LLM. Fetch only what's relevant |
| 12 | **Enter Recursive Language Models** | Standard LLM = "speed reader" vs. RLM = "librarian." Context as environment to explore, not buffer to fill |

### Chapter 4 — Recursion (Slides 13–16)

The paper's core contribution: how RLMs work, and the RLM-on-KG system.

| Slide | Title | Key Message |
|-------|-------|-------------|
| 13 | **Recursion** | Chapter title card |
| 14 | **How RLMs Work** | LLM writes code → External REPL executes (search, partition, peek) → results return. Programmatic exploration, not memorization |
| 15 | **RLM-on-KG** | Autonomous navigator over RDF knowledge graphs. Circular pipeline: Seed → Expand → Verify → Collect → Re-rank (9 tools) |
| 16 | **Results** | F1: 45.8 (RLM-on-KG) vs. 45.6 (GraphRAG). 56% win rate when evidence scattered across 11+ chunks. RLMs win when structure matters most |

### Chapter 5 — The SEO Playbook (Slides 17–20)

Implications for SEO and content strategy in the age of AI agents.

| Slide | Title | Key Message |
|-------|-------|-------------|
| 17 | **The SEO Playbook** | Chapter title card |
| 18 | **From Crawl-Index-Rank to Explore-Verify-Cite** | Old pipeline (crossed out) → new paradigm. AI agents don't rank pages — they navigate structured data |
| 19 | **What to Optimize** | Five priorities: Stable URIs, Mention Links, Provenance Anchors, Entity Pages, Crawlable Endpoints. Make content navigable, not just embeddable |
| 20 | **Structure Is the New Moat** | Connected data compounds in value. Schema.org, Knowledge Graphs, entity markup — these are the surfaces agents explore |

---

## Design System

### Visual Style: Swiss International Typographic Style

The entire deck follows a strict Müller-Brockmann-inspired design system:

- **Layout**: Modular grid, asymmetric flush-left composition, active whitespace
- **Typography**: Neo-grotesk sans-serif (Helvetica-like), hierarchy through scale not decoration
- **Color**: White background, black text, cool gray secondary, vivid Swiss red accent (functional only)
- **Constraints**: No centered text, no decorative icons, no gradients, no shadows, no illustrations

### Animation Style (Veo 3.1)

Motion-only prompts — Veo animates the existing slide image, never renders new text:

- **Camera**: Locked-off, frontal, no rotation
- **Motion**: Subtle fade-ins, precise slide-ins, clean chart-drawing, gentle parallax
- **Guardrail**: "DO NOT add, remove, or modify any text"
- **Duration**: 8 seconds per slide

---

## Technical Pipeline

1. **Slide images** → 20 PNG files at 16:9 in `slides_v3_16x9/`
2. **Video generation** → Veo 3.1 on Vertex AI via `generate_v4.py` → `videos_v4/`
3. **Concatenation** → ffmpeg → `presentation_v4.mp4`
4. **GIF conversion** → 720p (`gifs_v4/`) and 480p (`gifs_v4_480p/`)
5. **PPTX** → `create_slides.py` → `infinite_context_v4.pptx` (480p GIFs, <100 MB)

---

## References

- **Paper**: [RLM-on-KG](https://github.com/wordlift/rlm-on-kg) — Autonomous retrieval over RDF knowledge graphs
- **Repository**: [cyberandy/infinite-context](https://github.com/cyberandy/infinite-context)

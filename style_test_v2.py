#!/usr/bin/env python3
"""
Style Exploration V2 — Bolder.

Design thesis:
  - Slides are OVERLAYS on animated CA rule video backgrounds
  - Text is minimal — speaker's visual anchor only
  - CA patterns are the HERO, not decoration
  - Typography is massive, positioned to live alongside the animation
  - Two modes: dark-on-CA (most slides) and full-bleed-dark (chapter titles)

Generate 5 test slides covering each visual mode:
  A) Chapter title — full-dark, enormous type, act number
  B) Statement — one phrase, giant CA as hero
  C) Diagram — ultra-minimal pipeline, CA fills frame
  D) Data stat — single number, CA as data viz metaphor
  E) Closing — thesis, converging CAs
"""

import asyncio
from pathlib import Path

OUT = Path("slides_v5_style_test_v2")

# ── WordLift + Swiss Tokens ──
T = {
    "bg_dark": "#0D0D0D",     # near-black
    "fg_white": "#FFFFFF",
    "sky": "#3452DB",
    "berry": "#D55471",
    "petal": "#A10269",
    "leaf": "#22A286",
    "moss": "#125054",
    "sand": "#C2A41D",
    "gray": "#A1A7AF",
    "W": 1920,
    "H": 1080,
    "font": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
}

# ── CA Generators ──
def rule_row(prev, rule_num):
    n = len(prev)
    row = [0] * n
    for i in range(n):
        l, c, r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (rule_num >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_grid(rule_num, rows=50, cols=100, start="center"):
    first = [0] * cols
    if start == "center":
        first[cols//2] = 1
    elif start == "right":
        first[-1] = 1
    else:  # multi-seed for chaos
        import random
        random.seed(42)
        for i in range(0, cols, 7):
            first[i] = 1
    grid = [first]
    for _ in range(rows - 1):
        grid.append(rule_row(grid[-1], rule_num))
    return grid

def grid_to_svg(grid, cell=12, color="#3452DB", opacity=0.4, x=0, y=0, glow=False):
    rects = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val:
                cx = x + c * cell
                cy = y + r * cell
                rects.append(
                    f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" '
                    f'fill="{color}" opacity="{opacity}" />'
                )
                if glow:
                    rects.append(
                        f'<rect x="{cx-1}" y="{cy-1}" width="{cell+2}" height="{cell+2}" '
                        f'fill="{color}" opacity="{opacity*0.15}" rx="2" />'
                    )
    return "\n".join(rects)


def html(body, bg="#0D0D0D", ca_svg="", extra_css=""):
    return f"""<!DOCTYPE html>
<html><head><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};
font-family:'Inter',{T['font']};overflow:hidden;position:relative;color:{T['fg_white']};}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}}
.c{{position:relative;z-index:1;width:100%;height:100%;padding:80px 100px;
display:flex;flex-direction:column;justify-content:center;}}
.act-num{{font-size:200px;font-weight:900;line-height:0.85;letter-spacing:-8px;
opacity:0.08;position:absolute;right:100px;top:60px;z-index:0;}}
.section{{font-size:15px;font-weight:700;letter-spacing:6px;text-transform:uppercase;
color:{T['sky']};}}
{extra_css}
</style></head>
<body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="glow"><feGaussianBlur stdDeviation="2" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""


# ═══════════════════════════════════════════════
# A — Chapter Title (Dark poster, enormous type)
# ═══════════════════════════════════════════════
def slide_a_chapter():
    """Full-dark chapter card. The animation behind will be the CA rule growing."""
    # Subtle Rule 30 grid as background texture
    grid = gen_grid(30, rows=80, cols=160, start="center")
    ca = grid_to_svg(grid, cell=12, color=T['sky'], opacity=0.06, x=0, y=0)

    body = f"""
    <div class="act-num" style="color:{T['sky']};">I</div>
    <div style="margin-top:auto; margin-bottom:auto;">
      <div class="section" style="margin-bottom:32px;">Act I</div>
      <div style="font-size:130px; font-weight:900; line-height:0.92; letter-spacing:-6px;
                  max-width:1000px;">
        The Context<br>Explosion
      </div>
      <div style="width:80px; height:5px; background:{T['sky']}; margin-top:48px;"></div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
# B — Statement (CA as hero, text as anchor)
# ═══════════════════════════════════════════════
def slide_b_statement():
    """The CA grid IS the slide. Text is positioned to carve space within the pattern.
    This represents the kind of slide where the animated CA grows behind the statement."""
    # Large, bold Rule 30 fills right + bottom
    grid = gen_grid(30, rows=90, cols=120, start="center")
    ca = grid_to_svg(grid, cell=14, color=T['sky'], opacity=0.45, x=400, y=-100, glow=True)
    # Second layer: berry accent grid in the corner
    grid2 = gen_grid(110, rows=30, cols=40, start="right")
    ca += grid_to_svg(grid2, cell=10, color=T['berry'], opacity=0.25, x=0, y=780)

    body = f"""
    <div class="section">Act I — The Context Explosion</div>
    <div style="font-size:88px; font-weight:900; line-height:1.0; letter-spacing:-4px;
                margin-top:48px; max-width:800px;">
      Search Used<br>to Be a<br>Query.
    </div>
    <div style="font-size:88px; font-weight:900; line-height:1.0; letter-spacing:-4px;
                color:{T['sky']}; margin-top:8px; max-width:800px;">
      Now It's a<br>Journey.
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
# C — Diagram (Ultra-minimal pipeline)
# ═══════════════════════════════════════════════
def slide_c_pipeline():
    """Pipeline diagram as the core visual. CA fills the computation space.
    The pipeline boxes are where the cinemagraph animation plays."""
    # Rule 110 as "computation in progress"
    grid = gen_grid(110, rows=70, cols=140, start="right")
    ca = grid_to_svg(grid, cell=14, color=T['sky'], opacity=0.3, x=0, y=0, glow=True)

    box = (
        "padding:20px 32px; font-size:20px; font-weight:700; letter-spacing:1px;"
        "border:2px solid rgba(255,255,255,0.3);"
    )
    active = f"background:{T['sky']}; border-color:{T['sky']};"
    arrow = f"font-size:28px; color:{T['gray']}; opacity:0.6;"

    body = f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:72px; font-weight:900; line-height:1.0; letter-spacing:-3px;
                margin-top:40px;">
      It Doesn't Search.
    </div>
    <div style="font-size:72px; font-weight:900; line-height:1.0; letter-spacing:-3px;
                color:{T['sky']};">
      It Explores.
    </div>

    <div style="margin-top:auto; margin-bottom:60px; display:flex; align-items:center; gap:16px;">
      <div style="{box}">Seed</div>
      <div style="{arrow}">→</div>
      <div style="{box}">Expand</div>
      <div style="{arrow}">→</div>
      <div style="{box} {active}">Verify</div>
      <div style="{arrow}">→</div>
      <div style="{box}">Collect</div>
      <div style="{arrow}">→</div>
      <div style="{box}">Cite</div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
# D — Data Stat (Single number, CA as data)
# ═══════════════════════════════════════════════
def slide_d_stat():
    """One massive number. The CA pattern density visually encodes 'complexity'.
    Berry accent for disruption/warning."""
    # Dense Rule 110 as complexity visual
    grid = gen_grid(110, rows=60, cols=100, start="right")
    ca = grid_to_svg(grid, cell=14, color=T['berry'], opacity=0.2, x=900, y=100, glow=True)
    # Sparse Rule 90 (Sierpinski) underneath for contrast
    grid2 = gen_grid(90, rows=40, cols=60, start="center")
    ca += grid_to_svg(grid2, cell=16, color=T['sky'], opacity=0.08, x=100, y=600)

    body = f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:36px; font-weight:400; color:{T['gray']}; margin-top:32px;
                max-width:600px;">
      When the evidence is scattered
    </div>

    <div style="margin-top:60px;">
      <div style="font-size:280px; font-weight:900; line-height:0.85; letter-spacing:-12px;
                  color:{T['sky']};">71<span style="font-size:180px;">%</span></div>
      <div style="font-size:32px; font-weight:400; margin-top:8px;">
        LLM win rate on complex reasoning
      </div>
      <div style="width:60px; height:3px; background:{T['berry']}; margin-top:24px;"></div>
      <div style="font-size:18px; color:{T['gray']}; margin-top:12px;">
        +4.55pp F1 · p &lt; 0.001 · n=519
      </div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
# E — Closing (Thesis convergence)
# ═══════════════════════════════════════════════
def slide_e_closing():
    """Final thesis. All three CA rules converge on screen — Rule 30 (chaos) fading,
    Rule 90 (structure) dominant, Rule 110 (computation) emerging.
    This is the visual metaphor: chaos → structure → intelligence."""
    # Rule 30 — fading (chaos of unstructured data)
    g30 = gen_grid(30, rows=50, cols=80, start="multi")
    ca = grid_to_svg(g30, cell=12, color=T['berry'], opacity=0.08, x=0, y=0)
    # Rule 90 — dominant (the knowledge graph / structure)
    g90 = gen_grid(90, rows=60, cols=100, start="center")
    ca += grid_to_svg(g90, cell=14, color=T['sky'], opacity=0.35, x=600, y=100, glow=True)
    # Rule 110 — emerging (computation / intelligence)
    g110 = gen_grid(110, rows=40, cols=60, start="right")
    ca += grid_to_svg(g110, cell=12, color=T['leaf'], opacity=0.15, x=1400, y=600)

    body = f"""
    <div style="margin-top:auto; margin-bottom:auto; max-width:1100px;">
      <div style="font-size:64px; font-weight:900; line-height:1.15; letter-spacing:-3px;">
        The Moat Is Not<br>the Model.
      </div>
      <div style="font-size:64px; font-weight:900; line-height:1.15; letter-spacing:-3px;
                  color:{T['sky']}; margin-top:8px;">
        The Moat Is<br>the Graph.
      </div>
      <div style="width:80px; height:4px; background:{T['sky']}; margin-top:48px;"></div>
      <div style="font-size:24px; color:{T['gray']}; margin-top:24px; line-height:1.6;">
        Structure your knowledge. Connect your entities.<br>
        Train your navigators on your graph.
      </div>
      <div style="font-size:18px; color:{T['gray']}; opacity:0.5; margin-top:48px;">
        Andrea Volpini · WordLift · SEO Week 2026
      </div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
TESTS = [
    ("a_chapter.png", slide_a_chapter),
    ("b_statement.png", slide_b_statement),
    ("c_pipeline.png", slide_c_pipeline),
    ("d_stat.png", slide_d_stat),
    ("e_closing.png", slide_e_closing),
]


async def render():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": T["W"], "height": T["H"]},
            device_scale_factor=1,
        )
        for fname, gen in TESTS:
            print(f"  Rendering {fname}...", end=" ", flush=True)
            await page.set_content(gen(), wait_until="networkidle")
            path = OUT / fname
            await page.screenshot(path=str(path), type="png")
            print(f"✓ ({path.stat().st_size // 1024} KB)")
        await browser.close()
    print(f"\n✓ Style V2 tests saved to {OUT}/")


if __name__ == "__main__":
    asyncio.run(render())

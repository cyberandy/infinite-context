#!/usr/bin/env python3
"""
Style exploration: 3 test slides to establish the visual language
before committing to all 19.

V3 lessons: dark bg, massive type, bold geometry, MINIMAL text.
V5 additions: WordLift branding (sky blue), implicit CA patterns, Müller-Brockmann grid.

Generate 3 slides:
  A) Title card — dark, poster-style
  B) Content slide — diagram-driven, minimal text
  C) Data slide — single stat, graphic emphasis
"""

import asyncio
from pathlib import Path

OUT = Path("slides_v5_style_test")

# ── WordLift + Swiss Tokens ──
T = {
    "bg_dark": "#191919",     # neutral-900
    "bg_white": "#FFFFFF",
    "fg_white": "#FFFFFF",
    "fg_dark": "#191919",
    "sky": "#3452DB",         # primary brand
    "berry": "#D55471",       # disruption
    "petal": "#A10269",       # secondary
    "leaf": "#22A286",        # success
    "gray": "#A1A7AF",        # neutral-500
    "gray_light": "#F6F6F7",  # neutral-100
    "W": 1920,
    "H": 1080,
    "font": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
}

# ── CA Generators ──
def rule30_row(prev):
    n = len(prev)
    row = [0] * n
    for i in range(n):
        l, c, r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (30 >> ((l<<2)|(c<<1)|r)) & 1
    return row

def rule110_row(prev):
    n = len(prev)
    row = [0] * n
    for i in range(n):
        l, c, r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (110 >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_grid(rule_fn, rows=30, cols=80, start="center"):
    first = [0] * cols
    if start == "center":
        first[cols//2] = 1
    else:
        first[-1] = 1
    grid = [first]
    for _ in range(rows - 1):
        grid.append(rule_fn(grid[-1]))
    return grid

def grid_to_svg(grid, cell=12, color="#3452DB", opacity=0.25, x=0, y=0):
    rects = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val:
                rects.append(
                    f'<rect x="{x+c*cell}" y="{y+r*cell}" '
                    f'width="{cell}" height="{cell}" '
                    f'fill="{color}" opacity="{opacity}" />'
                )
    return "\n".join(rects)


def html(body, bg="#191919", ca_svg=""):
    return f"""<!DOCTYPE html>
<html><head><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};
font-family:{T['font']};overflow:hidden;position:relative;}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}}
.c{{position:relative;z-index:1;width:100%;height:100%;padding:80px 100px;
display:flex;flex-direction:column;}}
</style></head>
<body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""


# ═══════════════════════════════════════════════
# STYLE A — Title Card (Dark, poster-weight)
# ═══════════════════════════════════════════════
def style_a_title():
    grid = gen_grid(rule30_row, rows=45, cols=90)
    ca = grid_to_svg(grid, cell=14, color=T['sky'], opacity=0.20, x=700, y=0)
    # Bold diagonal wedge
    ca += f'<polygon points="1300,0 1920,0 1920,1080 900,1080" fill="{T["sky"]}" opacity="0.15" />'

    body = f"""
    <div style="margin-top:auto; margin-bottom:auto;">
      <div style="font-size:18px; font-weight:700; letter-spacing:6px; text-transform:uppercase;
                  color:{T['sky']}; margin-bottom:40px;">SEO Week 2026</div>
      <div style="font-size:120px; font-weight:800; line-height:0.95; letter-spacing:-4px;
                  color:{T['fg_white']};">Structure<br>Is the<br>Moat</div>
      <div style="width:120px; height:6px; background:{T['sky']}; margin-top:48px;"></div>
      <div style="font-size:22px; color:{T['gray']}; margin-top:24px;">Andrea Volpini · WordLift</div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
# STYLE B — Content slide (Diagram-driven)
# One graphic concept, one phrase, you speak the rest
# ═══════════════════════════════════════════════
def style_b_diagram():
    # Rule 110 as the "computation" visual for the RLM pipeline
    grid = gen_grid(rule110_row, rows=50, cols=100, start="right")
    ca = grid_to_svg(grid, cell=11, color=T['sky'], opacity=0.35, x=960, y=0)

    # pipeline boxes as the diagram
    box_style = (
        "display:inline-block; padding:16px 28px; font-size:22px; font-weight:700; "
        "letter-spacing:1px; margin-right:8px;"
    )
    body = f"""
    <div style="font-size:16px; font-weight:700; letter-spacing:5px; text-transform:uppercase;
                color:{T['sky']};">Act III — The Navigator</div>
    <div style="font-size:80px; font-weight:800; line-height:1.0; letter-spacing:-3px;
                color:{T['fg_white']}; margin-top:32px; max-width:900px;">
      It Doesn't<br>Search.<br>
      <span style="color:{T['sky']};">It Explores.</span>
    </div>

    <div style="margin-top:auto; margin-bottom:80px; display:flex; align-items:center; gap:12px;">
      <div style="{box_style} background:{T['fg_white']}; color:{T['bg_dark']};">Seed</div>
      <div style="color:{T['gray']}; font-size:24px;">→</div>
      <div style="{box_style} background:{T['fg_white']}; color:{T['bg_dark']};">Expand</div>
      <div style="color:{T['gray']}; font-size:24px;">→</div>
      <div style="{box_style} background:{T['sky']}; color:{T['fg_white']};">Verify</div>
      <div style="color:{T['gray']}; font-size:24px;">→</div>
      <div style="{box_style} background:{T['fg_white']}; color:{T['bg_dark']};">Collect</div>
      <div style="color:{T['gray']}; font-size:24px;">→</div>
      <div style="{box_style} background:{T['fg_white']}; color:{T['bg_dark']};">Cite</div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
# STYLE C — Data slide (Single stat, graphic emphasis)
# ═══════════════════════════════════════════════
def style_c_stat():
    grid = gen_grid(rule110_row, rows=35, cols=70, start="right")
    ca = grid_to_svg(grid, cell=12, color=T['berry'], opacity=0.15, x=1100, y=200)

    body = f"""
    <div style="font-size:16px; font-weight:700; letter-spacing:5px; text-transform:uppercase;
                color:{T['sky']};">Act III — The Navigator</div>
    <div style="font-size:48px; font-weight:400; color:{T['gray']}; margin-top:40px;">
      When the evidence is scattered
    </div>

    <div style="margin-top:auto; margin-bottom:auto;">
      <div style="font-size:220px; font-weight:800; line-height:0.9; letter-spacing:-8px;
                  color:{T['sky']};">71%</div>
      <div style="font-size:36px; font-weight:400; color:{T['fg_white']}; margin-top:16px;">
        LLM win rate on complex reasoning
      </div>
      <div style="width:80px; height:4px; background:{T['berry']}; margin-top:32px;"></div>
      <div style="font-size:22px; color:{T['gray']}; margin-top:16px;">
        +4.55pp F1 over heuristic · p &lt; 0.001 · n=519
      </div>
    </div>
    """
    return html(body, T['bg_dark'], ca)


# ═══════════════════════════════════════════════
TESTS = [
    ("style_a_title.png", style_a_title),
    ("style_b_diagram.png", style_b_diagram),
    ("style_c_stat.png", style_c_stat),
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
    print(f"\n✓ Style tests saved to {OUT}/")


if __name__ == "__main__":
    asyncio.run(render())

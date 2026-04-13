#!/usr/bin/env python3
"""
Style V3 — Dark/Light rhythm. 6 slides showing both modes.
Light slides for emphasis moments (key stats, pivots, closing thesis).
"""

import asyncio
from pathlib import Path

OUT = Path("slides_v5_style_test_v3")

T = {
    "dark": "#0D0D0D",
    "white": "#FFFFFF",
    "sky": "#3452DB",
    "berry": "#D55471",
    "leaf": "#22A286",
    "gray": "#A1A7AF",
    "gray_light": "#F6F6F7",
    "neutral900": "#191919",
    "W": 1920, "H": 1080,
    "font": "'Helvetica Neue','Helvetica','Arial',sans-serif",
}

def rule_row(prev, rule_num):
    n = len(prev)
    row = [0]*n
    for i in range(n):
        l,c,r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (rule_num >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_grid(rule, rows, cols, start="center"):
    first = [0]*cols
    if start=="center": first[cols//2]=1
    elif start=="right": first[-1]=1
    else:
        import random; random.seed(42)
        for i in range(0,cols,5): first[i]=1
    grid=[first]
    for _ in range(rows-1): grid.append(rule_row(grid[-1],rule))
    return grid

def svg_grid(grid, vis, cell, color, opacity, x, y, glow=False):
    rects=[]
    for r in range(min(vis,len(grid))):
        for c,val in enumerate(grid[r]):
            if val:
                cx,cy=x+c*cell,y+r*cell
                if glow:
                    rects.append(f'<rect x="{cx-1}" y="{cy-1}" width="{cell+2}" height="{cell+2}" fill="{color}" opacity="{opacity*0.15}" rx="1"/>')
                rects.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" fill="{color}" opacity="{opacity}"/>')
    return "\n".join(rects)

def html(body, bg, fg, ca_svg=""):
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};
font-family:{T['font']};overflow:hidden;position:relative;color:{fg};}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}}
.c{{position:relative;z-index:1;width:100%;height:100%;padding:80px 100px;
display:flex;flex-direction:column;justify-content:center;}}
.section{{font-size:15px;font-weight:700;letter-spacing:6px;text-transform:uppercase;
color:{T['sky']};margin-bottom:32px;}}
</style></head><body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""


# ═══════════ DARK SLIDES ═══════════

def slide_dark_title():
    grid = gen_grid(30, rows=100, cols=140, start="center")
    ca = svg_grid(grid, 75, cell=14, color=T['sky'], opacity=0.35, x=500, y=0, glow=True)
    body = f"""
    <div class="section">SEO Week 2026</div>
    <div style="font-size:120px;font-weight:900;line-height:0.92;letter-spacing:-5px;">
      Structure<br>Is the<br>Moat</div>
    <div style="width:80px;height:5px;background:{T['sky']};margin-top:48px;"></div>
    <div style="font-size:20px;color:{T['gray']};margin-top:24px;">Andrea Volpini · WordLift</div>
    """
    return html(body, T['dark'], T['white'], ca)

def slide_dark_navigator():
    grid = gen_grid(110, rows=80, cols=150, start="right")
    ca = svg_grid(grid, 60, cell=14, color=T['sky'], opacity=0.3, x=0, y=0, glow=True)
    box = "padding:16px 28px;font-size:18px;font-weight:700;border:2px solid rgba(255,255,255,0.3);"
    body = f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:76px;font-weight:900;line-height:1.0;letter-spacing:-3px;">
      It Doesn't Search.</div>
    <div style="font-size:76px;font-weight:900;line-height:1.0;letter-spacing:-3px;
                color:{T['sky']};">It Explores.</div>
    <div style="margin-top:auto;margin-bottom:80px;display:flex;align-items:center;gap:16px;">
      <div style="{box}">Seed</div><div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="{box}">Expand</div><div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="{box} background:{T['sky']};border-color:{T['sky']};">Verify</div>
      <div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="{box}">Collect</div><div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="{box}">Cite</div>
    </div>
    """
    return html(body, T['dark'], T['white'], ca)

def slide_dark_chapter():
    grid = gen_grid(90, rows=60, cols=100, start="center")
    ca = svg_grid(grid, 60, cell=10, color=T['sky'], opacity=0.06, x=T['W']//2-50*10, y=200)
    body = f"""
    <div class="section" style="margin-bottom:40px;">Act II</div>
    <div style="font-size:130px;font-weight:900;line-height:0.92;letter-spacing:-6px;max-width:1000px;">
      The<br>Compression<br>Solution</div>
    <div style="width:80px;height:5px;background:{T['sky']};margin-top:48px;"></div>
    """
    return html(body, T['dark'], T['white'], ca)

# ═══════════ LIGHT SLIDES (emphasis / punctuation) ═══════════

def slide_light_stat():
    """LIGHT — Big stat for emphasis."""
    grid = gen_grid(110, rows=55, cols=90, start="right")
    ca = svg_grid(grid, 55, cell=12, color=T['sky'], opacity=0.10, x=T['W']-90*12, y=100)
    body = f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:36px;font-weight:400;color:{T['gray']};margin-top:20px;">
      When the evidence is scattered</div>
    <div style="margin-top:60px;">
      <div style="font-size:300px;font-weight:900;line-height:0.82;letter-spacing:-14px;
                  color:{T['sky']};">71<span style="font-size:190px;">%</span></div>
      <div style="font-size:32px;font-weight:400;color:{T['neutral900']};margin-top:12px;">
        LLM win rate on complex reasoning</div>
      <div style="width:60px;height:4px;background:{T['berry']};margin-top:28px;"></div>
      <div style="font-size:18px;color:{T['gray']};margin-top:14px;">
        +4.55pp F1 over heuristic · p &lt; 0.001 · n=519</div>
    </div>
    """
    return html(body, T['white'], T['neutral900'], ca)

def slide_light_pivot():
    """LIGHT — Emphasis pivot moment. 'The Moat Is the Graph' reveal."""
    grid = gen_grid(90, rows=70, cols=120, start="center")
    ca = svg_grid(grid, 70, cell=12, color=T['sky'], opacity=0.12, x=T['W']//2-60*12, y=50)
    body = f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div style="font-size:80px;font-weight:900;line-height:1.08;letter-spacing:-4px;
                  color:{T['neutral900']};">
        The Moat Is Not<br>the Model.</div>
      <div style="font-size:80px;font-weight:900;line-height:1.08;letter-spacing:-4px;
                  color:{T['sky']};margin-top:12px;">
        The Moat Is<br>the Graph.</div>
      <div style="width:100px;height:5px;background:{T['sky']};margin-top:56px;"></div>
    </div>
    """
    return html(body, T['white'], T['neutral900'], ca)

def slide_light_turboquant():
    """LIGHT — TurboQuant results. Clean data emphasis."""
    grid = gen_grid(90, rows=40, cols=60, start="center")
    ca = svg_grid(grid, 40, cell=10, color=T['sky'], opacity=0.06, x=100, y=650)
    body = f"""
    <div class="section">Act II — The Compression Solution</div>
    <div style="font-size:64px;font-weight:900;line-height:1.0;letter-spacing:-3px;
                color:{T['neutral900']};">TurboQuant</div>
    <div style="display:flex;gap:60px;margin-top:64px;align-items:flex-end;">
      <div>
        <div style="font-size:120px;font-weight:900;line-height:0.9;color:{T['sky']};">4.5×</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">smaller KV cache</div>
      </div>
      <div>
        <div style="font-size:120px;font-weight:900;line-height:0.9;color:{T['sky']};">8×</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">faster attention</div>
      </div>
      <div>
        <div style="font-size:120px;font-weight:900;line-height:0.9;color:{T['neutral900']};">0</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">retrieval degradation</div>
      </div>
    </div>
    <div style="width:60px;height:3px;background:{T['berry']};margin-top:48px;"></div>
    <div style="font-size:20px;color:{T['gray']};margin-top:16px;">
      First algorithm with unbiased inner products, zero codebook, GPU-native, data-oblivious.</div>
    """
    return html(body, T['white'], T['neutral900'], ca)


SLIDES = [
    ("01_dark_title.png", slide_dark_title),
    ("02_dark_chapter.png", slide_dark_chapter),
    ("03_dark_navigator.png", slide_dark_navigator),
    ("04_light_stat.png", slide_light_stat),
    ("05_light_turboquant.png", slide_light_turboquant),
    ("06_light_pivot.png", slide_light_pivot),
]

async def render():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width":T["W"],"height":T["H"]}, device_scale_factor=1)
        for fname, gen in SLIDES:
            print(f"  {fname}...", end=" ", flush=True)
            await page.set_content(gen(), wait_until="networkidle")
            path = OUT / fname
            await page.screenshot(path=str(path), type="png")
            print(f"✓ ({path.stat().st_size//1024} KB)")
        await browser.close()
    print(f"\n✓ Saved to {OUT}/")

if __name__ == "__main__":
    asyncio.run(render())

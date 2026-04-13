#!/usr/bin/env python3
"""
Generate FULL-RES (1920x1080) cinemagraph GIFs + composite slide previews.
Each animation: 80 frames, ~4s loop at 20fps.
Also produces a composite PNG showing the slide text + CA pattern together.
"""

import asyncio
from pathlib import Path
from PIL import Image
import io

OUT = Path("cinemagraphs_1080p")

T = {
    "bg": "#0D0D0D",
    "sky": "#3452DB",
    "berry": "#D55471",
    "leaf": "#22A286",
    "white": "#FFFFFF",
    "gray": "#A1A7AF",
    "W": 1920,
    "H": 1080,
    "font": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
}

TOTAL_FRAMES = 80
DELAY_MS = 50

def rule_row(prev, rule_num):
    n = len(prev)
    row = [0] * n
    for i in range(n):
        l, c, r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (rule_num >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_grid(rule_num, rows, cols, start="center"):
    first = [0] * cols
    if start == "center": first[cols//2] = 1
    elif start == "right": first[-1] = 1
    else:
        import random; random.seed(42)
        for i in range(0, cols, 5): first[i] = 1
    grid = [first]
    for _ in range(rows - 1):
        grid.append(rule_row(grid[-1], rule_num))
    return grid

def svg_grid(grid, vis_rows, cell, color, opacity, x, y, glow=False):
    rects = []
    for r in range(min(vis_rows, len(grid))):
        for c, val in enumerate(grid[r]):
            if val:
                cx, cy = x + c*cell, y + r*cell
                if glow:
                    rects.append(
                        f'<rect x="{cx-1}" y="{cy-1}" width="{cell+2}" height="{cell+2}" '
                        f'fill="{color}" opacity="{opacity*0.18}" rx="1"/>')
                rects.append(
                    f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" '
                    f'fill="{color}" opacity="{opacity}"/>')
    return "\n".join(rects)


def frame_html(svg, text_overlay="", bg="#0D0D0D"):
    return f"""<!DOCTYPE html><html><head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};overflow:hidden;
font-family:'Inter',sans-serif;position:relative;color:{T['white']};}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;}}
.text{{position:absolute;top:0;left:0;width:100%;height:100%;z-index:1;
padding:80px 100px;display:flex;flex-direction:column;justify-content:center;}}
.section{{font-size:15px;font-weight:700;letter-spacing:6px;text-transform:uppercase;
color:{T['sky']};margin-bottom:32px;}}
</style></head><body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
{f'<div class="text">{text_overlay}</div>' if text_overlay else ''}
</body></html>"""


async def render_anim(page, name, make_frame, desc, text_overlay=""):
    """Render frames → GIF."""
    print(f"\n  [{name}] {desc}")
    frames = []
    for i in range(TOTAL_FRAMES):
        svg = make_frame(i)
        await page.set_content(frame_html(svg, text_overlay), wait_until="domcontentloaded")
        buf = await page.screenshot(type="png")
        img = Image.open(io.BytesIO(buf)).convert("RGB")
        frames.append(img)
        if (i+1) % 20 == 0:
            print(f"    frame {i+1}/{TOTAL_FRAMES}")

    # Save GIF
    path = OUT / f"{name}.gif"
    frames[0].save(str(path), save_all=True, append_images=frames[1:],
                   duration=DELAY_MS, loop=0, optimize=False)
    kb = path.stat().st_size // 1024
    print(f"    ✓ {path} ({kb} KB)")

    # Save composite PNG (frame at 75%)
    comp = OUT / f"{name}_composite.png"
    frames[int(TOTAL_FRAMES * 0.75)].save(str(comp))
    print(f"    ✓ {comp}")


# ═══════════════════════════════════════════════
# ANIMATIONS WITH TEXT OVERLAYS
# ═══════════════════════════════════════════════

def make_anim_title():
    """Title slide: Rule 30 grows behind 'Structure Is the Moat'."""
    grid = gen_grid(30, rows=100, cols=140, start="center")
    text = f"""
    <div class="section">SEO Week 2026</div>
    <div style="font-size:120px;font-weight:900;line-height:0.92;letter-spacing:-5px;">
      Structure<br>Is the<br>Moat</div>
    <div style="width:80px;height:5px;background:{T['sky']};margin-top:48px;"></div>
    <div style="font-size:20px;color:{T['gray']};margin-top:24px;">Andrea Volpini · WordLift</div>
    """
    def frame(i):
        p = i / TOTAL_FRAMES
        rows = int(p * 100) + 1
        return svg_grid(grid, rows, cell=14, color=T['sky'], opacity=0.35,
                       x=500, y=0, glow=True)
    return frame, text


def make_anim_statement():
    """Statement slide: Rule 30 chaos fills the right side."""
    grid = gen_grid(30, rows=90, cols=120, start="center")
    g110 = gen_grid(110, rows=30, cols=40, start="right")
    text = f"""
    <div class="section">Act I — The Context Explosion</div>
    <div style="font-size:88px;font-weight:900;line-height:1.0;letter-spacing:-4px;
                max-width:800px;">
      Search Used<br>to Be a<br>Query.</div>
    <div style="font-size:88px;font-weight:900;line-height:1.0;letter-spacing:-4px;
                color:{T['sky']};max-width:800px;margin-top:8px;">
      Now It's a<br>Journey.</div>
    """
    def frame(i):
        p = i / TOTAL_FRAMES
        svg = svg_grid(grid, int(p*90)+1, cell=14, color=T['sky'], opacity=0.4,
                       x=500, y=-50, glow=True)
        # Berry accent emerges in bottom-left
        berry_rows = max(1, int(max(0, p-0.5)*30/0.5))
        svg += svg_grid(g110, berry_rows, cell=10, color=T['berry'], opacity=0.25,
                       x=0, y=800)
        return svg
    return frame, text


def make_anim_navigator():
    """Navigator slide: Rule 110 computation cascades from top-right."""
    grid = gen_grid(110, rows=80, cols=150, start="right")
    text = f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:76px;font-weight:900;line-height:1.0;letter-spacing:-3px;">
      It Doesn't Search.</div>
    <div style="font-size:76px;font-weight:900;line-height:1.0;letter-spacing:-3px;
                color:{T['sky']};">It Explores.</div>
    <div style="margin-top:auto;margin-bottom:80px;display:flex;align-items:center;gap:16px;">
      <div style="padding:16px 28px;font-size:18px;font-weight:700;border:2px solid rgba(255,255,255,0.3);">Seed</div>
      <div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="padding:16px 28px;font-size:18px;font-weight:700;border:2px solid rgba(255,255,255,0.3);">Expand</div>
      <div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="padding:16px 28px;font-size:18px;font-weight:700;background:{T['sky']};border:2px solid {T['sky']};">Verify</div>
      <div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="padding:16px 28px;font-size:18px;font-weight:700;border:2px solid rgba(255,255,255,0.3);">Collect</div>
      <div style="color:{T['gray']};font-size:24px;">→</div>
      <div style="padding:16px 28px;font-size:18px;font-weight:700;border:2px solid rgba(255,255,255,0.3);">Cite</div>
    </div>
    """
    def frame(i):
        p = i / TOTAL_FRAMES
        rows = int(p * 80) + 1
        return svg_grid(grid, rows, cell=14, color=T['sky'], opacity=0.3,
                       x=0, y=0, glow=True)
    return frame, text


def make_anim_stat():
    """Data stat: Berry Rule 110 + sky Rule 90 underlayer."""
    g110 = gen_grid(110, rows=60, cols=100, start="right")
    g90 = gen_grid(90, rows=45, cols=70, start="center")
    text = f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:36px;font-weight:400;color:{T['gray']};margin-top:20px;">
      When the evidence is scattered</div>
    <div style="margin-top:60px;">
      <div style="font-size:280px;font-weight:900;line-height:0.85;letter-spacing:-12px;
                  color:{T['sky']};">71<span style="font-size:180px;">%</span></div>
      <div style="font-size:32px;font-weight:400;margin-top:8px;">
        LLM win rate on complex reasoning</div>
      <div style="width:60px;height:3px;background:{T['berry']};margin-top:24px;"></div>
      <div style="font-size:18px;color:{T['gray']};margin-top:12px;">
        +4.55pp F1 · p &lt; 0.001 · n=519</div>
    </div>
    """
    def frame(i):
        p = i / TOTAL_FRAMES
        svg = svg_grid(g90, int(p*45)+1, cell=10, color=T['sky'], opacity=0.08,
                       x=100, y=550)
        svg += svg_grid(g110, int(p*60)+1, cell=14, color=T['berry'], opacity=0.2,
                       x=T['W']-100*14, y=100, glow=True)
        return svg
    return frame, text


def make_anim_closing():
    """Closing: all 3 rules converge. Berry fades, sky dominates, leaf emerges."""
    g30 = gen_grid(30, rows=55, cols=80, start="multi")
    g90 = gen_grid(90, rows=65, cols=120, start="center")
    g110 = gen_grid(110, rows=45, cols=60, start="right")
    text = f"""
    <div style="margin-top:auto;margin-bottom:auto;max-width:1100px;">
      <div style="font-size:68px;font-weight:900;line-height:1.12;letter-spacing:-3px;">
        The Moat Is Not<br>the Model.</div>
      <div style="font-size:68px;font-weight:900;line-height:1.12;letter-spacing:-3px;
                  color:{T['sky']};margin-top:8px;">
        The Moat Is<br>the Graph.</div>
      <div style="width:80px;height:4px;background:{T['sky']};margin-top:48px;"></div>
      <div style="font-size:24px;color:{T['gray']};margin-top:24px;line-height:1.6;">
        Structure your knowledge. Connect your entities.<br>
        Train your navigators on your graph.</div>
      <div style="font-size:18px;color:{T['gray']};opacity:0.5;margin-top:40px;">
        Andrea Volpini · WordLift · SEO Week 2026</div>
    </div>
    """
    def frame(i):
        p = i / TOTAL_FRAMES
        svg = ""
        # Berry chaos fades out
        chaos_op = max(0, 0.25 * (1 - p * 1.8))
        if chaos_op > 0.01:
            svg += svg_grid(g30, 55, cell=8, color=T['berry'], opacity=chaos_op, x=0, y=0)
        # Sky structure grows
        sky_op = min(0.35, p * 0.45)
        svg += svg_grid(g90, int(p*65)+1, cell=12, color=T['sky'], opacity=sky_op,
                       x=T['W']//2 - 60*12, y=50, glow=True)
        # Leaf computation emerges late
        leaf_op = max(0, min(0.25, (p - 0.4) * 0.5))
        leaf_rows = max(1, int(max(0, p-0.4) * 45 / 0.6))
        if leaf_op > 0.01:
            svg += svg_grid(g110, leaf_rows, cell=10, color=T['leaf'], opacity=leaf_op,
                           x=T['W']-60*10, y=T['H']-45*10)
        return svg
    return frame, text


ANIMS = [
    ("01_title", make_anim_title, "Title — Rule 30 grows behind headline"),
    ("03_statement", make_anim_statement, "Statement — chaos fills, berry accent late"),
    ("10_navigator", make_anim_navigator, "Navigator — Rule 110 computation cascade"),
    ("11_stat", make_anim_stat, "Data — 71% with berry/sky underlayers"),
    ("19_closing", make_anim_closing, "Closing — three rules converge"),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ANIMS)} composite cinemagraphs at 1920×1080 ({TOTAL_FRAMES} frames)...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": T["W"], "height": T["H"]},
            device_scale_factor=1,
        )
        for name, make_fn, desc in ANIMS:
            frame_fn, text = make_fn()
            await render_anim(page, name, frame_fn, desc, text)
        await browser.close()

    print(f"\n✓ All composites saved to {OUT}/")


if __name__ == "__main__":
    asyncio.run(main())

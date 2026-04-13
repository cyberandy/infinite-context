#!/usr/bin/env python3
"""
Generate animated CA cinemagraph GIFs for each slide.
CSS animations rendered frame-by-frame via Playwright → assembled into GIFs with Pillow.

Each GIF: 854x480 (16:9), 60 frames, ~3s loop.
"""

import asyncio
from pathlib import Path
from PIL import Image
import io

OUT = Path("cinemagraphs")

T = {
    "bg": "#0D0D0D",
    "sky": "#3452DB",
    "berry": "#D55471",
    "leaf": "#22A286",
    "W": 854,
    "H": 480,
}

TOTAL_FRAMES = 60
FRAME_DELAY_MS = 50  # 20fps

# ── CA engine ──
def rule_row(prev, rule_num):
    n = len(prev)
    row = [0] * n
    for i in range(n):
        l, c, r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (rule_num >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_full_grid(rule_num, rows, cols, start="center"):
    first = [0] * cols
    if start == "center":
        first[cols//2] = 1
    elif start == "right":
        first[-1] = 1
    else:
        import random; random.seed(42)
        for i in range(0, cols, 5): first[i] = 1
    grid = [first]
    for _ in range(rows - 1):
        grid.append(rule_row(grid[-1], rule_num))
    return grid


def grid_svg(grid, visible_rows, cell, color, opacity, x, y, glow=False):
    """Render only `visible_rows` rows of the grid."""
    rects = []
    for r in range(min(visible_rows, len(grid))):
        for c, val in enumerate(grid[r]):
            if val:
                cx, cy = x + c*cell, y + r*cell
                if glow:
                    rects.append(
                        f'<rect x="{cx-1}" y="{cy-1}" width="{cell+2}" height="{cell+2}" '
                        f'fill="{color}" opacity="{opacity*0.2}" rx="1"/>'
                    )
                rects.append(
                    f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" '
                    f'fill="{color}" opacity="{opacity}"/>'
                )
    return "\n".join(rects)


def frame_html(ca_svg, bg="#0D0D0D"):
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};overflow:hidden;}}
</style></head><body>
<svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg>
</body></html>"""


async def render_gif(page, name, frame_generator, description):
    """Render frames and assemble into GIF."""
    print(f"  [{name}] {description}", flush=True)
    frames = []
    for i in range(TOTAL_FRAMES):
        svg_content = frame_generator(i)
        await page.set_content(frame_html(svg_content), wait_until="domcontentloaded")
        buf = await page.screenshot(type="png")
        img = Image.open(io.BytesIO(buf)).convert("RGB")
        frames.append(img)
        if (i+1) % 15 == 0:
            print(f"    frame {i+1}/{TOTAL_FRAMES}", flush=True)

    path = OUT / f"{name}.gif"
    frames[0].save(
        str(path), save_all=True, append_images=frames[1:],
        duration=FRAME_DELAY_MS, loop=0, optimize=True,
    )
    print(f"    ✓ {path} ({path.stat().st_size // 1024} KB)")


# ═══════════════════════════════════════════════
# ANIMATION DEFINITIONS
# ═══════════════════════════════════════════════

def anim_rule30_grow():
    """Rule 30: chaos grows from center, row by row."""
    grid = gen_full_grid(30, rows=80, cols=110, start="center")
    def frame(i):
        # Grow from 0 to 80 rows across 60 frames, then loop zone
        progress = i / TOTAL_FRAMES
        visible = int(progress * 80) + 1
        return grid_svg(grid, visible, cell=8, color=T['sky'], opacity=0.5,
                       x=0, y=0, glow=True)
    return frame

def anim_rule30_sweep():
    """Rule 30: diagonal sweep reveal — chaos emerging from the corner."""
    grid = gen_full_grid(30, rows=70, cols=120, start="center")
    def frame(i):
        progress = i / TOTAL_FRAMES
        # Reveal rows with a sweep — each row delayed slightly
        rects = []
        cell = 8
        for r in range(len(grid)):
            row_delay = r / len(grid) * 0.5  # stagger
            row_progress = max(0, min(1, (progress - row_delay) / 0.5))
            visible_cols = int(row_progress * len(grid[r]))
            for c in range(visible_cols):
                if grid[r][c]:
                    cx, cy = c*cell, r*cell
                    rects.append(
                        f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" '
                        f'fill="{T["sky"]}" opacity="0.45"/>'
                    )
        return "\n".join(rects)
    return frame

def anim_rule90_sierpinski():
    """Rule 90: Sierpinski triangle emerges symmetrically."""
    grid = gen_full_grid(90, rows=60, cols=110, start="center")
    def frame(i):
        progress = i / TOTAL_FRAMES
        visible = int(progress * 60) + 1
        return grid_svg(grid, visible, cell=8, color=T['sky'], opacity=0.45,
                       x=T['W']//2 - 55*8, y=0, glow=True)
    return frame

def anim_rule110_compute():
    """Rule 110: computation waves from the right edge."""
    grid = gen_full_grid(110, rows=65, cols=110, start="right")
    def frame(i):
        progress = i / TOTAL_FRAMES
        visible = int(progress * 65) + 1
        return grid_svg(grid, visible, cell=8, color=T['sky'], opacity=0.4,
                       x=T['W'] - 110*8, y=0, glow=True)
    return frame

def anim_rule110_berry():
    """Rule 110 in berry — disruption/warning accent."""
    grid = gen_full_grid(110, rows=55, cols=90, start="right")
    def frame(i):
        progress = i / TOTAL_FRAMES
        visible = int(progress * 55) + 1
        return grid_svg(grid, visible, cell=8, color=T['berry'], opacity=0.35,
                       x=T['W'] - 90*8, y=50, glow=True)
    return frame

def anim_convergence():
    """All 3 rules converging — chaos fades, structure dominates, computation emerges."""
    g30 = gen_full_grid(30, rows=50, cols=70, start="multi")
    g90 = gen_full_grid(90, rows=55, cols=100, start="center")
    g110 = gen_full_grid(110, rows=40, cols=50, start="right")
    def frame(i):
        progress = i / TOTAL_FRAMES
        # Rule 30 fades OUT
        chaos_opacity = max(0, 0.3 * (1 - progress * 1.5))
        # Rule 90 fades IN and grows
        struct_opacity = min(0.4, progress * 0.5)
        struct_rows = int(progress * 55) + 1
        # Rule 110 emerges late
        compute_opacity = max(0, min(0.3, (progress - 0.4) * 0.6))
        compute_rows = max(1, int(max(0, progress - 0.4) * 40 / 0.6))

        svg = ""
        if chaos_opacity > 0.01:
            svg += grid_svg(g30, 50, cell=7, color=T['berry'], opacity=chaos_opacity,
                           x=0, y=0)
        svg += grid_svg(g90, struct_rows, cell=9, color=T['sky'], opacity=struct_opacity,
                       x=T['W']//2 - 50*9, y=20, glow=True)
        if compute_opacity > 0.01:
            svg += grid_svg(g110, compute_rows, cell=8, color=T['leaf'], opacity=compute_opacity,
                           x=T['W'] - 50*8, y=T['H'] - 40*8)
        return svg
    return frame


# ═══════════════════════════════════════════════
ANIMATIONS = [
    ("ca_rule30_grow", anim_rule30_grow, "Rule 30 — chaos grows from center"),
    ("ca_rule30_sweep", anim_rule30_sweep, "Rule 30 — diagonal sweep reveal"),
    ("ca_rule90_sierpinski", anim_rule90_sierpinski, "Rule 90 — Sierpinski emerges"),
    ("ca_rule110_compute", anim_rule110_compute, "Rule 110 — computation from right"),
    ("ca_rule110_berry", anim_rule110_berry, "Rule 110 berry — disruption accent"),
    ("ca_convergence", anim_convergence, "Three rules converge — chaos→structure→intelligence"),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ANIMATIONS)} cinemagraph GIFs ({TOTAL_FRAMES} frames each)...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": T["W"], "height": T["H"]},
            device_scale_factor=1,
        )
        for name, gen_fn, desc in ANIMATIONS:
            await render_gif(page, name, gen_fn(), desc)
        await browser.close()

    print(f"\n✓ All cinemagraphs saved to {OUT}/")


if __name__ == "__main__":
    asyncio.run(main())

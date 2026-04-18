#!/usr/bin/env python3
"""
Generate an animated GIF for the "This is context" slide background.
Narrow light aperture breathing + Rule 30 cascade from top-right.
"""
import asyncio
from pathlib import Path

OUT = Path("content_animations_v2")

# Rule 30 grid generator (matching the deck's design system)
def rule_row(prev, rule_num):
    n = len(prev); row = [0]*n
    for i in range(n):
        l, c, r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (rule_num >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_grid(rule, rows, cols, start="center"):
    first = [0]*cols
    if start == "center": first[cols//2] = 1
    elif start == "right": first[-1] = 1
    grid = [first]
    for _ in range(rows - 1):
        grid.append(rule_row(grid[-1], rule))
    return grid

def svg_ca_rects(grid, vis, cell, color, opacity, x, y):
    rects = []
    for r in range(min(vis, len(grid))):
        for c, val in enumerate(grid[r]):
            if val:
                cx, cy = x + c*cell, y + r*cell
                rects.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" fill="{color}" opacity="{opacity}"/>')
    return "\n".join(rects)

# Generate Rule 30 grid for the background cascade
G30 = gen_grid(30, 80, 100, "center")
ca_svg = svg_ca_rects(G30, 50, 6, "#3452DB", 0.03, 600, -10)

HTML = f"""<!DOCTYPE html><html><head><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:800px; height:600px; background:#0D0D0D; overflow:hidden; position:relative; }}

/* The breathing light aperture */
.aperture {{
  position: absolute;
  left: 260px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 280px;
  background: linear-gradient(180deg, transparent 0%, rgba(52,82,219,0.3) 15%, rgba(200,210,255,0.95) 50%, rgba(52,82,219,0.3) 85%, transparent 100%);
  border-radius: 2px;
  animation: breathe 4s ease-in-out infinite;
  box-shadow:
    0 0 30px 8px rgba(52,82,219,0.15),
    0 0 60px 15px rgba(52,82,219,0.08),
    0 0 100px 30px rgba(52,82,219,0.04);
}}

@keyframes breathe {{
  0%   {{ opacity: 0.6; height: 240px; box-shadow: 0 0 20px 5px rgba(52,82,219,0.10), 0 0 40px 10px rgba(52,82,219,0.05); }}
  50%  {{ opacity: 1.0; height: 300px; box-shadow: 0 0 40px 12px rgba(52,82,219,0.20), 0 0 80px 20px rgba(52,82,219,0.10), 0 0 120px 40px rgba(52,82,219,0.05); }}
  100% {{ opacity: 0.6; height: 240px; box-shadow: 0 0 20px 5px rgba(52,82,219,0.10), 0 0 40px 10px rgba(52,82,219,0.05); }}
}}

/* Soft ambient glow behind the slit */
.glow {{
  position: absolute;
  left: 220px;
  top: 50%;
  transform: translateY(-50%);
  width: 80px;
  height: 400px;
  background: radial-gradient(ellipse at center, rgba(52,82,219,0.06) 0%, transparent 70%);
  animation: glowPulse 4s ease-in-out infinite;
  filter: blur(20px);
}}

@keyframes glowPulse {{
  0%   {{ opacity: 0.4; }}
  50%  {{ opacity: 0.8; }}
  100% {{ opacity: 0.4; }}
}}

/* CA pattern layer — subtle cascade */
.ca-layer {{
  position: absolute;
  top: 0; right: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  animation: caReveal 6s ease-out forwards;
}}
@keyframes caReveal {{
  0%   {{ opacity: 0; }}
  100% {{ opacity: 1; }}
}}

/* Film grain overlay */
.grain {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  pointer-events: none;
}}
</style></head>
<body>
  <div class="glow"></div>
  <div class="aperture"></div>
  <div class="ca-layer">
    <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
      {ca_svg}
    </svg>
  </div>
  <div class="grain"></div>
</body></html>"""


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    import io

    OUT.mkdir(exist_ok=True)
    name = "context_window_breathing"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 800, "height": 600}, device_scale_factor=2)
        await page.set_content(HTML, wait_until="domcontentloaded")

        # Capture 50 frames over 5 seconds (one full breath cycle + CA reveal)
        frames = []
        for i in range(50):
            await asyncio.sleep(0.1)
            frame_bytes = await page.screenshot(type="png")
            frames.append(Image.open(io.BytesIO(frame_bytes)).convert("RGBA"))

        # Save preview
        preview_path = OUT / f"{name}_preview.png"
        frames[-1].save(str(preview_path))
        print(f"  Preview: {preview_path}")

        # Build GIF
        gif_path = OUT / f"{name}.gif"
        frames[0].save(
            str(gif_path), save_all=True, append_images=frames[1:],
            duration=100, loop=0, optimize=True)
        print(f"  GIF: {gif_path} ({gif_path.stat().st_size // 1024} KB)")

        await page.close()
        await browser.close()

    print(f"\n✓ Done → {OUT}/{name}.gif")


if __name__ == "__main__":
    asyncio.run(main())

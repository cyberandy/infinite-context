#!/usr/bin/env python3
"""
Generate a standalone TurboQuant 3-stage pipeline GIF.
White background, 800×600, suitable for Google Slides overlay.
"""

import asyncio
from pathlib import Path

OUT = Path("content_animations_v2")

T = {
    "dark": "#0D0D0D", "white": "#FFFFFF", "sky": "#3452DB",
    "berry": "#D55471", "leaf": "#22A286", "sand": "#C2A41D",
    "gray": "#A1A7AF", "W": 800, "H": 600,
    "font": "'Helvetica Neue','Helvetica','Arial',sans-serif",
}

HTML_BODY = """
<style>
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-25px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes arrowPulse {
  0%%   { opacity: 0; }
  50%%  { opacity: 1; }
  100%% { opacity: 1; }
}
.stage {
  padding: 22px 28px;
  border-radius: 4px;
  opacity: 0;
  animation: slideDown 0.6s ease-out forwards;
}
.arrow {
  text-align: center;
  font-size: 22px;
  color: %(gray)s;
  opacity: 0;
}
.stat-block { opacity: 0; animation: fadeIn 0.5s ease-out forwards; }
</style>

<div style="display:flex; gap:32px; padding:40px 48px; font-family:%(font)s; height:100%%;">

  <!-- LEFT: 3-stage pipeline -->
  <div style="flex:1.1; display:flex; flex-direction:column; justify-content:center; gap:10px;">

    <div class="stage" style="background:rgba(0,0,0,0.04); border-left:6px solid %(dark)s; animation-delay:0.2s;">
      <div style="font-size:11px; font-weight:700; color:%(gray)s; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">Stage 1</div>
      <div style="font-size:22px; font-weight:900; color:%(dark)s;">PolarQuant</div>
      <div style="font-size:14px; color:%(gray)s; margin-top:2px;">Norm + Angle Decomposition</div>
    </div>

    <div class="arrow" style="animation: arrowPulse 0.4s ease-out 0.7s forwards;">↓</div>

    <div class="stage" style="background:rgba(52,82,219,0.06); border-left:6px solid %(sky)s; animation-delay:0.9s;">
      <div style="font-size:11px; font-weight:700; color:%(sky)s; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">Stage 2</div>
      <div style="font-size:22px; font-weight:900; color:%(dark)s;">QJL Transform</div>
      <div style="font-size:14px; color:%(gray)s; margin-top:2px;">Zero-bias Realignment</div>
    </div>

    <div class="arrow" style="animation: arrowPulse 0.4s ease-out 1.4s forwards;">↓</div>

    <div class="stage" style="background:rgba(194,164,29,0.06); border-left:6px solid %(sand)s; animation-delay:1.6s;">
      <div style="font-size:11px; font-weight:700; color:%(sand)s; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">Stage 3</div>
      <div style="font-size:22px; font-weight:900; color:%(dark)s;">GPU-Native Kernel</div>
      <div style="font-size:14px; color:%(gray)s; margin-top:2px;">Hardware-Aware Search</div>
    </div>

  </div>

  <!-- RIGHT: Results -->
  <div style="flex:0.7; display:flex; flex-direction:column; justify-content:center; gap:32px; padding-left:28px; border-left:1px solid #e5e5e5;">

    <div class="stat-block" style="animation-delay:2.2s;">
      <div style="font-size:64px; font-weight:900; line-height:0.9; color:%(sky)s; letter-spacing:-3px;">4.5×</div>
      <div style="font-size:15px; color:%(gray)s; margin-top:6px; font-weight:700;">Smaller KV Cache</div>
    </div>

    <div class="stat-block" style="animation-delay:2.5s;">
      <div style="font-size:64px; font-weight:900; line-height:0.9; color:%(sky)s; letter-spacing:-3px;">8×</div>
      <div style="font-size:15px; color:%(gray)s; margin-top:6px; font-weight:700;">Faster Attention</div>
    </div>

    <div class="stat-block" style="animation-delay:2.8s;">
      <div style="font-size:64px; font-weight:900; line-height:0.9; color:%(dark)s; letter-spacing:-3px;">0</div>
      <div style="font-size:15px; color:%(gray)s; margin-top:6px; font-weight:700;">Recall Degradation</div>
    </div>

  </div>

</div>
"""


async def main():
    from playwright.async_api import async_playwright

    OUT.mkdir(exist_ok=True)
    name = "06_turboquant_3stage"

    # Template substitution
    html = HTML_BODY
    for k, v in T.items():
        html = html.replace(f"%({k})s", str(v))

    full_html = f"""<!DOCTYPE html><html><head><style>
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{width:{T['W']}px;height:{T['H']}px;background:{T['white']};color:{T['dark']};
          font-family:{T['font']};overflow:hidden;}}
    </style></head><body>{html}</body></html>"""

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": T["W"], "height": T["H"]}, device_scale_factor=2)
        await page.set_content(full_html, wait_until="domcontentloaded")

        # Capture 40 frames over 4 seconds
        frames = []
        for i in range(40):
            await asyncio.sleep(0.1)
            frame_bytes = await page.screenshot(type="png")
            frames.append(frame_bytes)

        # Save last frame as preview
        preview_path = OUT / f"{name}_preview.png"
        with open(preview_path, "wb") as f:
            f.write(frames[-1])
        print(f"  Preview: {preview_path}")

        # Build GIF
        from PIL import Image
        import io
        pil_frames = []
        for fb in frames:
            img = Image.open(io.BytesIO(fb))
            pil_frames.append(img.convert("RGBA"))

        gif_path = OUT / f"{name}.gif"
        pil_frames[0].save(
            str(gif_path), save_all=True, append_images=pil_frames[1:],
            duration=100, loop=0, optimize=True)
        print(f"  GIF: {gif_path} ({gif_path.stat().st_size//1024} KB)")

        await page.close()
        await browser.close()

    print(f"\n✓ Done → {OUT}/{name}.gif")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
import asyncio
from pathlib import Path
from PIL import Image
import io

OUT = Path("content_animations_v2")
T = {
    "dark": "#0D0D0D", "white": "#FFFFFF", "sky": "#3452DB",
    "berry": "#D55471", "leaf": "#22A286", "sand": "#C2A41D",
    "gray": "#A1A7AF", "W": 800, "H": 600,
    "font": "'Helvetica Neue','Helvetica','Arial',sans-serif",
}

def get_html():
    template = """
    <style>
    @keyframes count45{0%%{content:'0.0×'}25%%{content:'1.2×'}50%%{content:'2.8×'}75%%{content:'3.9×'}100%%{content:'4.5×'}}
    @keyframes count8{0%%{content:'0×'}25%%{content:'2×'}50%%{content:'4×'}75%%{content:'6×'}100%%{content:'8×'}}
    @keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    .stat{font-size:120px;font-weight:900;line-height:0.9;letter-spacing:-6px;color:%(sky)s;}
    .stat::after{animation-duration:1.5s;animation-fill-mode:forwards;animation-timing-function:steps(4);}
    .s1::after{content:'4.5×';animation-name:count45;}
    .s2::after{content:'8×';animation-name:count8;animation-delay:0.5s;}
    .s3{animation:fadeIn 0.8s ease-out 1.2s forwards;opacity:0;color:%(white)s;}
    </style>
    <div style="display:flex;gap:60px;padding:60px;font-family:%(font)s;background:%(dark)s;height:100%%;align-items:center;">
      <div><div class="stat s1"></div><div style="font-size:18px;color:%(gray)s;margin-top:8px;">smaller</div></div>
      <div><div class="stat s2"></div><div style="font-size:18px;color:%(gray)s;margin-top:8px;">faster</div></div>
      <div><div class="stat s3" style="font-size:120px;font-weight:900;line-height:0.9;letter-spacing:-6px;">0</div>
        <div style="font-size:18px;color:%(gray)s;margin-top:8px;">degradation</div></div>
    </div>"""
    html = template
    for k, v in T.items():
        html = html.replace(f"%%({k})s", str(v))
    # Double check remaining %% if any
    html = html.replace("%%", "%")
    return f"<!DOCTYPE html><html><head><style>body{{margin:0;padding:0;overflow:hidden;}}</style></head><body>{html}</body></html>"

async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": T["W"], "height": T["H"]})
        await page.set_content(get_html())
        
        frames = []
        for i in range(30):
            await asyncio.sleep(0.1)
            frames.append(await page.screenshot(type="png"))
        
        pil_frames = [Image.open(io.BytesIO(f)).convert("RGBA") for f in frames]
        gif_path = OUT / "06_turboquant_counter_dark.gif"
        pil_frames[0].save(str(gif_path), save_all=True, append_images=pil_frames[1:], duration=100, loop=0)
        print(f"Generated: {gif_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

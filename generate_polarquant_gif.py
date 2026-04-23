#!/usr/bin/env python3
"""
PolarQuant animated GIF.
High-fidelity visual match for the Cartesian → Sphere transformation.
"""

import asyncio, random
from pathlib import Path
from PIL import Image
import io

OUT = Path("content_animations_v2")
W, H = 840, 600

# Colors
DK = "#080808"
WH = "#FFFFFF"
GR = "#A1A7AF"
GRD = "#333333"
SKY = "#3452DB"
SKY_L = "#7C99FF" # Brighter blue for glow UI
FN = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

# ── Generate 32 random 3D dots inside the cube ──
random.seed(42)
dots_svg = ""
for i in range(35):
    u = random.uniform(0.15, 0.85)
    v = random.uniform(0.15, 0.85)
    w_depth = random.uniform(0.15, 0.85)
    
    # Projection parameters
    # Origin (back-left-bottom): 90, 180
    px = 90 + u * 150 - w_depth * 50
    py = 180 - v * 150 + w_depth * 50
    
    size = 2.5 + w_depth * 2  # Larger if closer (front is w_depth=1)
    opacity = 0.5 + w_depth * 0.5
    delay = (i * 0.05) % 2.0
    
    dots_svg += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{size:.1f}" fill="{SKY_L}" opacity="0" filter="url(#glow)" style="animation:dotAppear 0.5s ease-out {delay:.1f}s forwards, floatDot 3s ease-in-out {delay}s infinite alternate;"/>\n'

# Coordinate for the 'w' dot
w_u, w_v, w_w = 0.6, 0.6, 0.8
w_px = 90 + w_u * 150 - w_w * 50
w_py = 180 - w_v * 150 + w_w * 50

HTML = f"""<!DOCTYPE html><html><head>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; background:{DK}; font-family:{FN}; overflow:hidden; color:{WH}; background-image: radial-gradient(circle at 50% 50%, #151515 0%, {DK} 100%); }}

@keyframes fadeUp {{ from {{ opacity:0; transform:translateY(20px); }} to {{ opacity:1; transform:translateY(0); }} }}
@keyframes fadeIn {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
@keyframes dotAppear {{ from {{ opacity:0; transform:scale(0); }} to {{ opacity:1; transform:scale(1); }} }}
@keyframes floatDot {{ 0% {{ transform:translateY(0px); }} 100% {{ transform:translateY(-3px); }} }}
@keyframes drawArrow {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
@keyframes drawLine {{ from {{ stroke-dashoffset: 200; }} to {{ stroke-dashoffset: 0; }} }}

.layout {{ display:flex; justify-content:space-between; width:100%; height:100%; padding:30px 40px; }}

/* Panels */
.panel {{ display:flex; flex-direction:column; opacity:0; animation:fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }}
.left {{ flex:0 0 300px; animation-delay: 0.1s; }}
.mid {{ flex:0 0 160px; align-items:center; justify-content:center; padding-top:60px; }}
.right {{ flex:0 0 300px; animation-delay: 0.5s; }}

/* Typography */
.st {{ font-size:14px; font-weight:700; letter-spacing:1px; color:{WH}; margin-bottom:6px; }}
.ss {{ font-size:13px; color:{GR}; margin-bottom:20px; font-weight:300; }}
.cap-f {{ font-size:14px; color:{GR}; margin-top:20px; text-align:center; opacity:0; animation:fadeIn 0.6s ease-out 1.2s forwards; }}
.cap-f b {{ color:{WH}; font-weight:600; }}
.cap-d {{ font-size:13px; color:{GR}; text-align:center; margin-top:6px; opacity:0; animation:fadeIn 0.6s ease-out 1.4s forwards; line-height:1.4; }}
.bold-blue {{ color:{SKY_L}; font-weight:600; }}

/* Middle Text */
.mid-title {{ font-size:13px; color:{WH}; text-align:center; margin-top:16px; opacity:0; animation:fadeIn 0.5s ease-out 1.5s forwards; line-height:1.5; }}
.mid-formula {{ font-size:14px; color:{SKY_L}; font-style:italic; margin-top:14px; opacity:0; animation:fadeIn 0.5s ease-out 1.7s forwards; text-align:center; }}
.mid-note {{ font-size:11px; color:{GR}; text-align:center; margin-top:3px; opacity:0; animation:fadeIn 0.5s ease-out 1.9s forwards; }}

/* SVG Styles */
.line-dim {{ stroke: rgba(255,255,255,0.15); stroke-width: 1.2px; }}
.line-dimmer {{ stroke: rgba(255,255,255,0.06); stroke-width: 1px; }}
.line-axis {{ stroke: rgba(255,255,255,0.4); stroke-width: 1.5px; }}
.text-axis {{ fill: {GR}; font-size: 13px; font-style: italic; font-weight: 500; }}
.label-val {{ fill: {SKY_L}; font-size: 16px; font-style: italic; }}

</style>
</head><body>
<div class="layout">

  <!-- 1. CARTESIAN -->
  <div class="panel left">
    <div class="st">1. CARTESIAN COORDINATES</div>
    <div class="ss">Weights in ℝⁿ</div>
    <svg width="280" height="320" viewBox="0 0 280 320" style="margin:0 auto; overflow:visible;">
      <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Back face -->
      <polygon points="90,30 240,30 240,180 90,180" fill="none" class="line-dimmer"/>
      <!-- Front face -->
      <polygon points="40,80 190,80 190,230 40,230" fill="none" class="line-dim"/>
      <!-- Edges -->
      <line x1="90" y1="30" x2="40" y2="80" class="line-dimmer"/>
      <line x1="240" y1="30" x2="190" y2="80" class="line-dimmer"/>
      <line x1="240" y1="180" x2="190" y2="230" class="line-dimmer"/>
      <line x1="90" y1="180" x2="40" y2="230" class="line-dimmer"/>

      <!-- Axes originating from (90,180) -->
      <!-- x1 (front-left) -->
      <line x1="90" y1="180" x2="20" y2="250" class="line-axis"/>
      <polygon points="20,250 16,244 26,246" fill="rgba(255,255,255,0.4)"/>
      <text x="0" y="265" class="text-axis">x₁</text>

      <!-- x2 (right) -->
      <line x1="90" y1="180" x2="260" y2="180" class="line-axis"/>
      <polygon points="260,180 252,176 252,184" fill="rgba(255,255,255,0.4)"/>
      <text x="268" y="184" class="text-axis">x₂</text>

      <!-- x3 (up) -->
      <line x1="90" y1="180" x2="90" y2="10" class="line-axis"/>
      <polygon points="90,10 86,18 94,18" fill="rgba(255,255,255,0.4)"/>
      <text x="70" y="18" class="text-axis">x₃</text>

      <!-- Scattered dots -->
      {dots_svg}

      <!-- Center 'w' dot & dashed line -->
      <line x1="90" y1="180" x2="{w_px}" y2="{w_py}" stroke="{WH}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0"
            style="animation:fadeIn 0.5s ease-out 1.2s forwards;"/>
      <circle cx="{w_px}" cy="{w_py}" r="5" fill="{WH}" filter="url(#glow)" opacity="0"
              style="animation:dotAppear 0.4s ease-out 1.4s forwards;"/>
      <text x="{w_px + 10}" y="{w_py - 5}" fill="{WH}" font-size="20" font-weight="700" opacity="0"
            style="animation:fadeIn 0.5s ease-out 1.4s forwards;">w</text>
    </svg>
    <div class="cap-f"><b>w</b> = [x₁, x₂, x₃, …, xₙ]</div>
    <div class="cap-d">High-dimensional weight vector<br>in Cartesian space</div>
  </div>

  <!-- ARROW & MID INFO -->
  <div class="panel mid">
    <svg width="100" height="24">
      <line x1="10" y1="12" x2="80" y2="12" stroke="{GR}" stroke-width="2.5" stroke-dasharray="100" stroke-dashoffset="100" stroke-linecap="round"
            style="animation: drawArrow 0.6s ease-out 1.4s forwards;"/>
      <polygon points="82,12 72,6 74,12 72,18" fill="{GR}" opacity="0" style="animation: fadeIn 0.2s ease-out 1.9s forwards;"/>
    </svg>
    <div class="mid-title">Transform to<br><span class="bold-blue">Polar Coordinates</span></div>
    
    <div class="mid-formula">r = ‖w‖₂</div>
    <div class="mid-note">(radius / magnitude)</div>
    
    <div class="mid-formula" style="margin-top:10px;">θ = w / ‖w‖₂</div>
    <div class="mid-note">(direction on unit sphere)</div>
  </div>

  <!-- 2. SPHERE -->
  <div class="panel right">
    <div class="st">2. POLAR COORDINATES ON A SPHERE</div>
    <div class="ss">(r, θ) ∈ ℝ⁺ × Sⁿ⁻¹</div>
    
    <svg width="300" height="320" viewBox="0 0 300 320" style="margin:0 auto; overflow:visible;">
      <defs>
        <radialGradient id="sphereGrad" cx="30%" cy="30%" r="60%">
          <stop offset="0%" stop-color="{SKY}" stop-opacity="0.18"/>
          <stop offset="100%" stop-color="{SKY}" stop-opacity="0"/>
        </radialGradient>
      </defs>
      
      <!-- Base Sphere -->
      <circle cx="150" cy="160" r="130" fill="url(#sphereGrad)" stroke="{SKY_L}" stroke-width="1.5" opacity="0.4"/>
      
      <!-- Wireframe Latitudes -->
      <ellipse cx="150" cy="160" rx="130" ry="36" fill="none" class="line-dim" stroke-dasharray="4,4"/>
      <ellipse cx="150" cy="110" rx="120" ry="30" fill="none" class="line-dimmer" stroke-dasharray="4,4"/>
      <ellipse cx="150" cy="210" rx="120" ry="30" fill="none" class="line-dimmer" stroke-dasharray="4,4"/>
      <ellipse cx="150" cy="65" rx="88" ry="20" fill="none" class="line-dimmer" stroke-dasharray="4,4"/>
      <ellipse cx="150" cy="255" rx="88" ry="20" fill="none" class="line-dimmer" stroke-dasharray="4,4"/>
      
      <!-- Wireframe Longitudes -->
      <ellipse cx="150" cy="160" rx="36" ry="130" fill="none" class="line-dim" stroke-dasharray="4,4"/>
      <ellipse cx="150" cy="160" rx="88" ry="130" fill="none" class="line-dim" stroke-dasharray="4,4"/>
      
      <!-- xn axis -->
      <line x1="150" y1="30" x2="150" y2="290" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
      <polygon points="150,20 146,28 154,28" fill="{GR}"/>
      <text x="160" y="28" class="text-axis">xₙ</text>

      <!-- Center point -->
      <circle cx="150" cy="160" r="3" fill="rgba(255,255,255,0.4)"/>
      
      <!-- Vector r -->
      <line x1="150" y1="160" x2="250" y2="85" stroke="{SKY_L}" stroke-width="2.5" stroke-linecap="round"
            stroke-dasharray="200" stroke-dashoffset="200" style="animation: drawLine 0.7s ease-out 2.2s forwards;"/>
            
      <!-- θ Endpoint glow dot -->
      <circle cx="250" cy="85" r="7" fill="{WH}" filter="url(#glow)" opacity="0"
              style="animation:dotAppear 0.4s ease-out 2.8s forwards;"/>
              
      <text x="260" y="75" fill="{WH}" font-size="20" font-weight="700" opacity="0"
            style="animation:fadeIn 0.5s ease-out 3.0s forwards;">θ</text>
            
      <text x="175" y="145" class="label-val" opacity="0"
            style="animation:fadeIn 0.5s ease-out 2.6s forwards;">r = ‖w‖₂</text>
            
      <text x="210" y="260" fill="{SKY_L}" font-size="12" font-style="italic" opacity="0"
            style="animation:fadeIn 0.5s ease-out 2.0s forwards;">→ Unit Sphere Sⁿ⁻¹</text>
    </svg>
    <div class="cap-f" style="margin-top:10px;"><b style="color:{SKY_L}">r</b> captures <b>magnitude</b> (how far)</div>
    <div class="cap-d"><b style="color:{SKY_L}">θ</b> captures <b>direction</b> (where)</div>
  </div>

</div>
</body></html>"""

async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    name = "polarquant_diagram"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await page.set_content(HTML, wait_until="networkidle")
        frames = []
        for i in range(50):
            await asyncio.sleep(0.1)
            frames.append(await page.screenshot(type="png"))
            
        preview_path = OUT / f"{name}_preview.png"
        with open(preview_path, "wb") as f:
            f.write(frames[-1])
            
        pil_frames = [Image.open(io.BytesIO(fb)).convert("RGBA") for fb in frames]
        gif_path = OUT / f"{name}.gif"
        pil_frames[0].save(str(gif_path), save_all=True, append_images=pil_frames[1:],
                           duration=100, loop=0, optimize=True)
        print(f"✓ GIF generated: {gif_path.stat().st_size // 1024} KB")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

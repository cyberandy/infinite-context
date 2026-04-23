#!/usr/bin/env python3
"""
TurboQuant threshold diagram — animated GIF.
3 panels: Value between levels → Learned threshold → Unbiased expectation.
Dark background, matching PolarQuant style.
"""

import asyncio
from pathlib import Path
from PIL import Image
import io

OUT = Path("content_animations_v2")
W, H = 840, 480

DK = "#080808"
WH = "#FFFFFF"
GR = "#A1A7AF"
GRD = "#333333"
SKY = "#3452DB"
SKY_L = "#7C99FF"
BERRY = "#C44569"
FN = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

HTML = f"""<!DOCTYPE html><html><head>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; background:{DK}; font-size:13px;
  background-image: radial-gradient(circle at 50% 50%, #151515 0%, {DK} 100%);
  font-family:{FN}; overflow:hidden; color:{WH};
}}

@keyframes fadeUp {{
  from {{ opacity:0; transform:translateY(16px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes fadeIn {{
  from {{ opacity:0; }}
  to   {{ opacity:1; }}
}}
@keyframes drawLine {{
  from {{ stroke-dashoffset: 200; }}
  to   {{ stroke-dashoffset: 0; }}
}}
@keyframes drawArrow {{
  from {{ stroke-dashoffset: 40; }}
  to   {{ stroke-dashoffset: 0; }}
}}
@keyframes pulseGlow {{
  0%, 100% {{ opacity:0.6; }}
  50%      {{ opacity:1; }}
}}
@keyframes expandBrace {{
  from {{ transform: scaleX(0); }}
  to   {{ transform: scaleX(1); }}
}}

.layout {{ display:flex; gap:12px; width:100%; height:100%; padding:24px 24px; }}

/* Panel */
.panel {{
  flex:1; display:flex; flex-direction:column;
  opacity:0; animation: fadeUp 0.7s cubic-bezier(0.2,0.8,0.2,1) forwards;
}}
.p1 {{ animation-delay:0.2s; }}
.p2 {{ animation-delay:1.4s; }}
.p3 {{ animation-delay:2.6s; }}

/* Arrows between panels */
.panel-arrow {{
  flex:0 0 24px; display:flex; align-items:center; justify-content:center;
  padding-top:60px;
  opacity:0; animation: fadeIn 0.3s ease-out forwards;
}}
.pa1 {{ animation-delay:1.1s; }}
.pa2 {{ animation-delay:2.3s; }}

/* Typography */
.p-num {{
  font-size:14px; font-weight:700; color:{SKY_L};
  margin-bottom:4px;
}}
.p-title {{
  font-size:15px; font-weight:700; color:{WH};
  margin-bottom:6px; line-height:1.3;
}}
.p-desc {{
  font-size:11px; color:{GR}; line-height:1.4;
  margin-bottom:12px;
}}
.p-desc i {{ color:{SKY_L}; font-style:italic; }}

/* Bottom takeaway boxes */
.takeaway {{
  margin-top:auto; padding:12px 16px;
  border:1px solid rgba(255,255,255,0.12);
  border-radius:6px; background:rgba(255,255,255,0.03);
  font-size:12px; color:{GR}; line-height:1.4;
  opacity:0; animation: fadeIn 0.5s ease-out forwards;
}}
.t1 {{ animation-delay:0.9s; }}
.t2 {{ animation-delay:2.1s; }}
.t3 {{ animation-delay:3.3s; }}
.takeaway b {{ color:{WH}; font-weight:600; }}
.takeaway .drift {{ color:{BERRY}; font-weight:600; }}
.takeaway .learn {{ color:{SKY_L}; font-weight:600; }}

/* SVG shared styles */
.nl {{ stroke:{GR}; stroke-width:2; stroke-linecap:round; }}
.dot-big {{ fill:{GR}; }}
.dot-w {{ fill:{SKY_L}; filter:url(#glow); }}
.dot-tau {{ fill:{SKY_L}; filter:url(#glow); }}
.label {{ fill:{GR}; font-size:14px; font-style:italic; font-family:{FN}; }}
.label-w {{ fill:{SKY_L}; font-size:16px; font-weight:700; font-family:{FN}; }}
.label-tau {{ fill:{SKY_L}; font-size:16px; font-weight:700; font-family:{FN}; }}
.brace {{ stroke:{GR}; stroke-width:1; fill:none; stroke-dasharray:3,3; }}
.brace-label {{ fill:{GR}; font-size:11px; font-family:{FN}; }}

/* Formula styles */
.formula {{
  font-size:16px; color:{WH}; text-align:center;
  line-height:1.7; margin-top:6px;
  opacity:0; animation:fadeIn 0.6s ease-out 3.0s forwards;
}}
.formula .var {{ color:{SKY_L}; font-style:italic; }}
.formula .eq {{ color:{GR}; }}
</style>
</head><body>
<div class="layout">

  <!-- ═══ PANEL 1: Value between two levels ═══ -->
  <div class="panel p1">
    <div class="p-num">1.</div>
    <div class="p-title">Value between two levels</div>
    <div class="p-desc">A weight <i>w</i> lies between<br>two quantization levels.</div>

    <svg width="230" height="160" viewBox="0 0 230 160" style="margin:0 auto;">
      <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>

      <!-- Number line -->
      <line x1="20" y1="70" x2="210" y2="70" class="nl"
            stroke-dasharray="200" stroke-dashoffset="200"
            style="animation:drawLine 0.5s ease-out 0.4s forwards;"/>

      <!-- lk dot + label -->
      <circle cx="40" cy="70" r="5" class="dot-big" opacity="0"
              style="animation:fadeIn 0.3s ease-out 0.6s forwards;"/>
      <text x="30" y="100" class="label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 0.7s forwards;">l<tspan baseline-shift="sub" font-size="10">k</tspan></text>

      <!-- lk+1 dot + label -->
      <circle cx="190" cy="70" r="5" class="dot-big" opacity="0"
              style="animation:fadeIn 0.3s ease-out 0.6s forwards;"/>
      <text x="172" y="100" class="label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 0.7s forwards;">l<tspan baseline-shift="sub" font-size="10">k+1</tspan></text>

      <!-- w dot + label -->
      <circle cx="120" cy="70" r="6" class="dot-w" opacity="0"
              style="animation:fadeIn 0.4s ease-out 0.8s forwards;"/>
      <text x="112" y="52" class="label-w" opacity="0"
            style="animation:fadeIn 0.4s ease-out 0.9s forwards;">w</text>

      <!-- Dashed braces: round down -->
      <path d="M 115,80 Q 80,95 45,80" class="brace" opacity="0"
            style="animation:fadeIn 0.4s ease-out 1.0s forwards;"/>
      <text x="48" y="120" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 1.1s forwards;">round down</text>
      <text x="55" y="135" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 1.1s forwards;">to l<tspan baseline-shift="sub" font-size="9">k</tspan></text>

      <!-- Dashed braces: round up -->
      <path d="M 125,80 Q 155,95 185,80" class="brace" opacity="0"
            style="animation:fadeIn 0.4s ease-out 1.0s forwards;"/>
      <text x="145" y="120" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 1.1s forwards;">round up</text>
      <text x="142" y="135" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 1.1s forwards;">to l<tspan baseline-shift="sub" font-size="9">k+1</tspan></text>
    </svg>

    <div class="takeaway t1">
      Normal quantization<br>→ systematic <span class="drift">drift</span>
    </div>
  </div>

  <!-- Arrow 1→2 -->
  <div class="panel-arrow pa1">
    <svg width="20" height="20" viewBox="0 0 20 20">
      <line x1="2" y1="10" x2="12" y2="10" stroke="{GR}" stroke-width="2"
            stroke-dasharray="40" stroke-dashoffset="40"
            style="animation:drawArrow 0.3s ease-out 1.2s forwards;"/>
      <polygon points="14,5 20,10 14,15" fill="{GR}" opacity="0"
               style="animation:fadeIn 0.2s ease-out 1.4s forwards;"/>
    </svg>
  </div>

  <!-- ═══ PANEL 2: TurboQuant learns τ ═══ -->
  <div class="panel p2">
    <div class="p-num">2.</div>
    <div class="p-title">TurboQuant learns a threshold</div>
    <div class="p-desc">Instead of a fixed midpoint, we learn<br>a threshold <i>τ</i> that shifts the boundary.</div>

    <svg width="230" height="160" viewBox="0 0 230 160" style="margin:0 auto;">
      <!-- Number line -->
      <line x1="20" y1="70" x2="210" y2="70" class="nl"
            stroke-dasharray="200" stroke-dashoffset="200"
            style="animation:drawLine 0.5s ease-out 1.6s forwards;"/>

      <!-- lk dot + label -->
      <circle cx="40" cy="70" r="5" class="dot-big" opacity="0"
              style="animation:fadeIn 0.3s ease-out 1.8s forwards;"/>
      <text x="30" y="100" class="label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 1.9s forwards;">l<tspan baseline-shift="sub" font-size="10">k</tspan></text>

      <!-- lk+1 dot + label -->
      <circle cx="190" cy="70" r="5" class="dot-big" opacity="0"
              style="animation:fadeIn 0.3s ease-out 1.8s forwards;"/>
      <text x="172" y="100" class="label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 1.9s forwards;">l<tspan baseline-shift="sub" font-size="10">k+1</tspan></text>

      <!-- τ marker: downward triangle above line at ~40% position (x=100) -->
      <text x="93" y="38" class="label-tau" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.0s forwards;">τ</text>
      <polygon points="100,50 96,58 104,58" fill="{SKY_L}" filter="url(#glow)" opacity="0"
               style="animation:fadeIn 0.4s ease-out 2.0s forwards;"/>

      <!-- w dot on line at ~65% position (x=140) -->
      <circle cx="140" cy="70" r="5" class="dot-w" opacity="0"
              style="animation:fadeIn 0.4s ease-out 2.0s forwards;"/>
      <text x="132" y="55" class="label-w" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.1s forwards;">w</text>

      <defs>
        <marker id="arrowL" markerWidth="8" markerHeight="6" refX="1" refY="3" orient="auto">
          <polygon points="8,0 0,3 8,6" fill="{GR}"/></marker>
        <marker id="arrowR" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0,0 8,3 0,6" fill="{GR}"/></marker>
      </defs>

      <!-- Double-headed arrow: lk ↔ τ (left segment) -->
      <line x1="48" y1="82" x2="93" y2="82" stroke="{GR}" stroke-width="1.5"
            marker-start="url(#arrowL)" marker-end="url(#arrowR)" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.2s forwards;"/>

      <!-- Double-headed arrow: τ ↔ lk+1 (right segment) -->
      <line x1="107" y1="82" x2="183" y2="82" stroke="{GR}" stroke-width="1.5"
            marker-start="url(#arrowL)" marker-end="url(#arrowR)" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.2s forwards;"/>

      <!-- Labels below left segment -->
      <text x="42" y="112" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 2.3s forwards;">round down</text>
      <text x="42" y="127" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 2.3s forwards;">(if w &lt; τ)</text>

      <!-- Labels below right segment -->
      <text x="125" y="112" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 2.3s forwards;">round up</text>
      <text x="122" y="127" class="brace-label" opacity="0"
            style="animation:fadeIn 0.3s ease-out 2.3s forwards;">(if w ≥ τ)</text>
    </svg>

    <div class="takeaway t2">
      <span class="learn">TurboQuant learns</span> where<br>rounding should happen
    </div>
  </div>

  <!-- Arrow 2→3 -->
  <div class="panel-arrow pa2">
    <svg width="20" height="20" viewBox="0 0 20 20">
      <line x1="2" y1="10" x2="12" y2="10" stroke="{GR}" stroke-width="2"
            stroke-dasharray="40" stroke-dashoffset="40"
            style="animation:drawArrow 0.3s ease-out 2.4s forwards;"/>
      <polygon points="14,5 20,10 14,15" fill="{GR}" opacity="0"
               style="animation:fadeIn 0.2s ease-out 2.6s forwards;"/>
    </svg>
  </div>

  <!-- ═══ PANEL 3: Unbiased in expectation ═══ -->
  <div class="panel p3">
    <div class="p-num">3.</div>
    <div class="p-title">Unbiased in expectation</div>
    <div class="p-desc">We choose <i>τ</i> so that the expected<br>compressed value equals the original.</div>

    <svg width="230" height="80" viewBox="0 0 230 80" style="margin:0 auto;">
      <!-- Probability labels -->
      <text x="30" y="25" fill="{GR}" font-size="12" font-family="{FN}" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.8s forwards;">
        Round to l<tspan baseline-shift="sub" font-size="9">k</tspan></text>
      <text x="30" y="42" fill="{GR}" font-size="12" font-family="{FN}" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.9s forwards;">
        with prob. <tspan fill="{SKY_L}" font-style="italic">p</tspan></text>

      <text x="140" y="25" fill="{GR}" font-size="12" font-family="{FN}" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.8s forwards;">
        Round to l<tspan baseline-shift="sub" font-size="9">k+1</tspan></text>
      <text x="140" y="42" fill="{GR}" font-size="12" font-family="{FN}" opacity="0"
            style="animation:fadeIn 0.4s ease-out 2.9s forwards;">
        with prob. <tspan fill="{SKY_L}" font-style="italic">1 − p</tspan></text>
    </svg>

    <div class="formula">
      𝔼[ŵ] <span class="eq">=</span> <span class="var">p</span> · l<sub>k</sub> <span class="eq">+</span> (1 − <span class="var">p</span>) · l<sub>k+1</sub>
    </div>
    <div class="formula" style="animation-delay:3.3s; font-size:22px; margin-top:4px;">
      <span class="eq">=</span> <span class="var" style="font-size:24px; font-weight:700;">w</span>
    </div>

    <div class="takeaway t3">
      Expected compressed weight<br><b>= original weight</b>
    </div>
  </div>

</div>
</body></html>"""


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    name = "turboquant_threshold"
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
        print(f"✓ GIF: {gif_path} ({gif_path.stat().st_size // 1024} KB)")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

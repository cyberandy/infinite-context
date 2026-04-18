#!/usr/bin/env python3
"""
Batch generate GIF animations for uncovered high-value slides.
05, 10b, 15b, 21, 27, 30
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import io
from PIL import Image

OUT = Path("content_animations_v2")
OUT.mkdir(exist_ok=True)

T = {
    "dark": "#0D0D0D", "white": "#FFFFFF", "sky": "#3452DB",
    "berry": "#D55471", "leaf": "#22A286", "sand": "#C2A41D",
    "gray": "#A1A7AF", "W": 800, "H": 600,
    "font": "'Helvetica Neue','Helvetica','Arial',sans-serif",
}

ANIMS = [

    # ── 05 THE COMPRESSION PARADOX (chapter opener) ────────
    ("05_compression_reveal", "dark", """
    <style>
    @keyframes zoomTitle{from{opacity:0;transform:scale(0.85)}to{opacity:1;transform:scale(1)}}
    @keyframes lineSlide{from{width:0}to{width:100px}}
    @keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="padding:80px;font-family:%(font)s;color:white;height:100%%;display:flex;flex-direction:column;justify-content:center;">
      <div style="font-size:14px;font-weight:700;color:%(sky)s;letter-spacing:5px;text-transform:uppercase;margin-bottom:24px;
           animation:fadeUp 0.6s ease-out forwards;">Act II</div>
      <div style="font-size:72px;font-weight:900;line-height:1.05;letter-spacing:-3px;
           animation:zoomTitle 1s ease-out forwards;">The<br>Compression<br>Paradox</div>
      <div style="height:5px;background:%(sky)s;margin-top:32px;animation:lineSlide 0.8s ease-out 1.2s forwards;width:0;"></div>
      <div style="font-size:18px;color:%(gray)s;margin-top:24px;max-width:500px;
           animation:fadeUp 0.7s ease-out 1.6s forwards;opacity:0;">
        High compression · Zero overhead · Geometric accuracy<br>
        <span style="color:%(berry)s;">Get it wrong and similarity scores are silently biased.</span></div>
    </div>"""),

    # ── 10b CONTEXT TIMELINE (bar chart 512→∞) ─────────────
    ("10b_context_timeline", "dark", """
    <style>
    @keyframes barGrow{from{height:0}to{height:var(--h)}}
    @keyframes fadeLabel{from{opacity:0}to{opacity:1}}
    .col{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;flex:1;}
    .bar{border-radius:3px 3px 0 0;animation:barGrow 1s ease-out forwards;height:0;}
    .yr{font-size:16px;color:%(gray)s;margin-bottom:6px;animation:fadeLabel 0.5s ease-out forwards;opacity:0;}
    .tok{font-size:13px;color:%(gray)s;margin-top:6px;animation:fadeLabel 0.5s ease-out forwards;opacity:0;}
    </style>
    <div style="padding:40px 50px;font-family:%(font)s;color:white;height:100%%;display:flex;flex-direction:column;">
      <div style="font-size:16px;font-weight:700;color:%(sky)s;letter-spacing:4px;text-transform:uppercase;margin-bottom:8px;">The Context Explosion</div>
      <div style="font-size:36px;font-weight:900;margin-bottom:auto;">in Numbers</div>
      <div style="display:flex;gap:20px;align-items:flex-end;height:320px;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,0.1);">
        <div class="col"><div class="yr" style="animation-delay:0.2s;">2017</div>
          <div class="bar" style="--h:30px;background:%(gray)s;opacity:0.4;width:50px;animation-delay:0.3s;"></div>
          <div class="tok" style="animation-delay:0.5s;">512 tokens</div></div>
        <div class="col"><div class="yr" style="animation-delay:0.5s;">2020</div>
          <div class="bar" style="--h:55px;background:%(gray)s;opacity:0.5;width:50px;animation-delay:0.6s;"></div>
          <div class="tok" style="animation-delay:0.8s;">4K tokens</div></div>
        <div class="col"><div class="yr" style="animation-delay:0.8s;">2023</div>
          <div class="bar" style="--h:120px;background:%(sand)s;opacity:0.6;width:50px;animation-delay:0.9s;"></div>
          <div class="tok" style="animation-delay:1.1s;">128K</div></div>
        <div class="col"><div class="yr" style="animation-delay:1.1s;">2024</div>
          <div class="bar" style="--h:200px;background:%(sky)s;opacity:0.7;width:50px;animation-delay:1.2s;"></div>
          <div class="tok" style="animation-delay:1.4s;">1M+</div></div>
        <div class="col"><div class="yr" style="animation-delay:1.4s;color:%(sky)s;font-weight:700;">2026</div>
          <div class="bar" style="--h:280px;background:%(sky)s;width:50px;animation-delay:1.5s;"></div>
          <div class="tok" style="animation-delay:1.7s;color:%(sky)s;font-weight:700;">∞ context</div></div>
      </div>
      <div style="font-size:14px;color:%(gray)s;margin-top:12px;animation:fadeLabel 0.6s ease-out 2.2s forwards;opacity:0;">
        <span style="color:white;font-weight:700;">Context windows grew 2,000,000×.</span> The question shifted from capacity to navigation.</div>
    </div>"""),

    # ── 15b GRAPHRAG HEAD-TO-HEAD ──────────────────────────
    ("15b_graphrag_faceoff", "light", """
    <style>
    @keyframes countUp45{0%%{content:'0.0'}25%%{content:'11.5'}50%%{content:'23.0'}75%%{content:'34.4'}100%%{content:'45.8'}}
    @keyframes countUp456{0%%{content:'0.0'}25%%{content:'11.4'}50%%{content:'22.8'}75%%{content:'34.2'}100%%{content:'45.6'}}
    @keyframes fadeIn{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:translateY(0)}}
    @keyframes slideBar{from{width:0}to{width:70px}}
    .score{font-size:80px;font-weight:900;line-height:0.9;letter-spacing:-4px;}
    .score::after{animation-duration:1.8s;animation-fill-mode:forwards;animation-timing-function:steps(4);}
    </style>
    <div style="padding:50px;font-family:%(font)s;color:#191919;height:100%%;">
      <div style="font-size:14px;font-weight:700;color:%(sky)s;letter-spacing:4px;text-transform:uppercase;margin-bottom:8px;">Head-to-Head</div>
      <div style="font-size:36px;font-weight:900;margin-bottom:32px;">RLM vs GraphRAG</div>
      <div style="display:flex;gap:32px;">
        <div style="flex:1;padding:32px;border-top:5px solid %(sky)s;background:rgba(52,82,219,0.03);
             animation:fadeIn 0.6s ease-out 0.3s forwards;opacity:0;">
          <div style="font-size:16px;font-weight:700;color:%(sky)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:12px;">RLM-on-KG</div>
          <div class="score" style="color:%(sky)s;"><span style="display:none;">.</span></div>
          <div class="score" style="color:%(sky)s;">45.8</div>
          <div style="font-size:16px;color:%(gray)s;margin-top:8px;">F1 Score</div></div>
        <div style="flex:1;padding:32px;border-top:5px solid %(gray)s;
             animation:fadeIn 0.6s ease-out 0.6s forwards;opacity:0;">
          <div style="font-size:16px;font-weight:700;color:%(gray)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:12px;">Microsoft GraphRAG</div>
          <div class="score" style="color:%(gray)s;">45.6</div>
          <div style="font-size:16px;color:%(gray)s;margin-top:8px;">F1 Score</div></div>
      </div>
      <div style="height:5px;background:%(berry)s;margin-top:32px;animation:slideBar 0.6s ease-out 1.4s forwards;width:0;"></div>
      <div style="font-size:15px;color:%(gray)s;margin-top:12px;animation:fadeIn 0.5s ease-out 1.8s forwards;opacity:0;">
        When evidence spans <span style="color:%(sky)s;font-weight:700;">11+ chunks</span>: RLM wins <span style="color:%(sky)s;font-weight:700;">56%%</span> of the time</div>
    </div>"""),

    # ── 21 THE MOAT IS THE GRAPH ───────────────────────────
    ("21_moat_graph", "dark", """
    <style>
    @keyframes revealLine{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:translateX(0)}}
    @keyframes pillIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    @keyframes glowPill{0%%{box-shadow:none}100%%{box-shadow:0 0 20px rgba(52,82,219,0.3)}}
    </style>
    <div style="padding:60px 80px;font-family:%(font)s;color:white;height:100%%;display:flex;flex-direction:column;justify-content:center;">
      <div style="font-size:48px;font-weight:900;line-height:1.1;
           animation:revealLine 0.7s ease-out 0.2s forwards;opacity:0;">The Moat Is Not<br>the Model.</div>
      <div style="font-size:48px;font-weight:900;line-height:1.1;color:%(sky)s;margin-top:8px;
           animation:revealLine 0.7s ease-out 0.7s forwards;opacity:0;">The Moat Is<br>the Graph.</div>
      <div style="display:flex;gap:12px;margin-top:48px;">
        <div style="padding:16px 24px;border-top:3px solid %(sky)s;background:rgba(52,82,219,0.05);
             font-size:15px;font-weight:900;animation:pillIn 0.5s ease-out 1.2s forwards;opacity:0;">Limitless Context</div>
        <div style="padding:16px 24px;border-top:3px solid %(sky)s;background:rgba(52,82,219,0.05);
             font-size:15px;font-weight:900;animation:pillIn 0.5s ease-out 1.4s forwards;opacity:0;">Billion-Scale Search</div>
        <div style="padding:16px 24px;border-top:3px solid %(sky)s;background:rgba(52,82,219,0.05);
             font-size:15px;font-weight:900;animation:pillIn 0.5s ease-out 1.6s forwards;opacity:0;">On-Device Intelligence</div>
        <div style="padding:16px 24px;border-top:3px solid %(sky)s;background:%(sky)s;
             font-size:15px;font-weight:900;animation:pillIn 0.5s ease-out 1.8s forwards,glowPill 0.5s ease-out 2.2s forwards;opacity:0;">Navigable Knowledge Graph</div>
      </div>
    </div>"""),

    # ── 27 EXPLORE → VERIFY → CITE ─────────────────────────
    ("27_explore_verify_cite", "dark", """
    <style>
    @keyframes pillarIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    @keyframes arrowFade{from{opacity:0}to{opacity:0.5}}
    </style>
    <div style="padding:50px;font-family:%(font)s;color:white;height:100%%;display:flex;flex-direction:column;">
      <div style="font-size:14px;font-weight:700;color:%(sky)s;letter-spacing:4px;text-transform:uppercase;margin-bottom:8px;">The New Paradigm</div>
      <div style="font-size:32px;font-weight:900;margin-bottom:auto;">Explore → Verify → Cite</div>
      <div style="display:flex;gap:20px;align-items:stretch;">
        <div style="flex:1;padding:28px;background:rgba(52,82,219,0.06);border-left:5px solid %(sky)s;
             animation:pillarIn 0.6s ease-out 0.3s forwards;opacity:0;">
          <div style="font-size:12px;font-weight:700;color:%(sky)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px;">Explore</div>
          <div style="font-size:17px;font-weight:900;margin-bottom:6px;">Graph Traversal</div>
          <div style="font-size:13px;color:%(gray)s;">Navigate entity relationships to find relevant knowledge</div></div>
        <div style="font-size:24px;color:%(gray)s;display:flex;align-items:center;
             animation:arrowFade 0.4s ease-out 0.8s forwards;opacity:0;">→</div>
        <div style="flex:1;padding:28px;background:rgba(34,162,134,0.06);border-left:5px solid %(leaf)s;
             animation:pillarIn 0.6s ease-out 0.9s forwards;opacity:0;">
          <div style="font-size:12px;font-weight:700;color:%(leaf)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px;">Verify</div>
          <div style="font-size:17px;font-weight:900;margin-bottom:6px;">Evidence Grounding</div>
          <div style="font-size:13px;color:%(gray)s;">Cross-reference claims against structured data</div></div>
        <div style="font-size:24px;color:%(gray)s;display:flex;align-items:center;
             animation:arrowFade 0.4s ease-out 1.4s forwards;opacity:0;">→</div>
        <div style="flex:1;padding:28px;background:rgba(194,164,29,0.06);border-left:5px solid %(sand)s;
             animation:pillarIn 0.6s ease-out 1.5s forwards;opacity:0;">
          <div style="font-size:12px;font-weight:700;color:%(sand)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px;">Cite</div>
          <div style="font-size:17px;font-weight:900;margin-bottom:6px;">Source Attribution</div>
          <div style="font-size:13px;color:%(gray)s;">Generate answers with traceable provenance</div></div>
      </div>
    </div>"""),

    # ── 30 CLOSING (call to action) ────────────────────────
    ("30_closing_cta", "dark", """
    <style>
    @keyframes lineIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    @keyframes barGrow{from{width:0}to{width:80px}}
    </style>
    <div style="padding:60px 80px;font-family:%(font)s;color:white;height:100%%;display:flex;flex-direction:column;justify-content:center;">
      <div style="font-size:32px;font-weight:900;line-height:1.2;
           animation:lineIn 0.7s ease-out 0.2s forwards;opacity:0;">Context windows will keep growing.</div>
      <div style="font-size:32px;font-weight:900;line-height:1.2;
           animation:lineIn 0.7s ease-out 0.5s forwards;opacity:0;">Models will keep getting cheaper.</div>
      <div style="font-size:32px;font-weight:900;line-height:1.2;color:%(sky)s;margin-top:20px;
           animation:lineIn 0.7s ease-out 1.0s forwards;opacity:0;">The variable that compounds</div>
      <div style="font-size:32px;font-weight:900;line-height:1.2;color:%(sky)s;
           animation:lineIn 0.7s ease-out 1.3s forwards;opacity:0;">is your data connectivity.</div>
      <div style="height:4px;background:%(sky)s;margin-top:32px;animation:barGrow 0.6s ease-out 1.8s forwards;width:0;"></div>
      <div style="font-size:22px;font-weight:700;margin-top:20px;
           animation:lineIn 0.6s ease-out 2.2s forwards;opacity:0;">Structure your knowledge now.</div>
    </div>"""),

]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for name, mode, template in ANIMS:
            html = template
            for k, v in T.items():
                html = html.replace(f"%({k})s", str(v))
            bg = T['dark'] if mode == "dark" else T['white']
            fg = T['white'] if mode == "dark" else "#191919"

            full_html = f"""<!DOCTYPE html><html><head><style>
            *{{margin:0;padding:0;box-sizing:border-box;}}
            body{{width:{T['W']}px;height:{T['H']}px;background:{bg};color:{fg};
                  font-family:{T['font']};overflow:hidden;}}
            </style></head><body>{html}</body></html>"""

            page = await browser.new_page(
                viewport={"width": T["W"], "height": T["H"]}, device_scale_factor=1)
            await page.set_content(full_html, wait_until="domcontentloaded")

            frames = []
            for i in range(40):
                await asyncio.sleep(0.1)
                frame_bytes = await page.screenshot(type="png")
                frames.append(frame_bytes)

            # Preview
            with open(OUT / f"{name}_preview.png", "wb") as f:
                f.write(frames[-1])

            # GIF
            pil_frames = [Image.open(io.BytesIO(fb)).convert("RGBA") for fb in frames]
            gif_path = OUT / f"{name}.gif"
            pil_frames[0].save(
                str(gif_path), save_all=True, append_images=pil_frames[1:],
                duration=100, loop=0, optimize=True)
            print(f"  ✓ {name}.gif ({gif_path.stat().st_size//1024} KB)")
            await page.close()

        await browser.close()
    print(f"\n✓ All 6 animations generated → {OUT}/")


if __name__ == "__main__":
    asyncio.run(main())

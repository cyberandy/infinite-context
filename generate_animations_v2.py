#!/usr/bin/env python3
"""
Content animations for the full 29-slide v2 deck.
Generates transparent-background-ready GIF overlays for Google Slides.
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


ANIMATIONS = [
    # Act I
    ("02_context_bars", "dark", """
    <style>
    @keyframes g{from{width:0%}to{width:100%}}
    .bar{height:36px;border-radius:3px;animation:g 2s ease-out forwards;margin-bottom:16px;}
    .label{font-size:16px;font-weight:700;margin-bottom:6px;}
    </style>
    <div style="padding:40px;font-family:%(font)s;color:white;">
      <div class="label" style="color:%(sky)s;">KV Cache O(n²)</div>
      <div class="bar" style="background:%(sky)s;animation-delay:0s;"></div>
      <div class="label" style="color:%(sky)s;">Vector Index</div>
      <div class="bar" style="background:%(sky)s;animation-delay:0.3s;max-width:70%%;"></div>
      <div class="label" style="color:%(sky)s;">Device Memory</div>
      <div class="bar" style="background:%(sky)s;animation-delay:0.6s;max-width:50%%;"></div>
      <div class="label" style="color:%(berry)s;">Agent Context Loss</div>
      <div class="bar" style="background:%(berry)s;animation-delay:0.9s;max-width:85%%;"></div>
    </div>"""),

    # Act II
    ("06_turboquant_counter", "light", """
    <style>
    @keyframes count45{0%%{content:'0.0×'}25%%{content:'1.2×'}50%%{content:'2.8×'}75%%{content:'3.9×'}100%%{content:'4.5×'}}
    @keyframes count8{0%%{content:'0×'}25%%{content:'2×'}50%%{content:'4×'}75%%{content:'6×'}100%%{content:'8×'}}
    @keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    .stat{font-size:120px;font-weight:900;line-height:0.9;letter-spacing:-6px;color:%(sky)s;}
    .stat::after{animation-duration:1.5s;animation-fill-mode:forwards;animation-timing-function:steps(4);}
    .s1::after{content:'4.5×';animation-name:count45;}
    .s2::after{content:'8×';animation-name:count8;animation-delay:0.5s;}
    .s3{animation:fadeIn 0.8s ease-out 1.2s forwards;opacity:0;color:%(dark)s;}
    </style>
    <div style="display:flex;gap:60px;padding:60px;font-family:%(font)s;">
      <div><div class="stat s1"></div><div style="font-size:18px;color:%(gray)s;margin-top:8px;">smaller</div></div>
      <div><div class="stat s2"></div><div style="font-size:18px;color:%(gray)s;margin-top:8px;">faster</div></div>
      <div><div class="stat s3" style="font-size:120px;font-weight:900;line-height:0.9;letter-spacing:-6px;">0</div>
        <div style="font-size:18px;color:%(gray)s;margin-top:8px;">degradation</div></div>
    </div>"""),

    # Act III — Pipeline steps
    ("11_pipeline_steps", "dark", """
    <style>
    @keyframes stepIn{from{opacity:0.15;transform:scale(0.95)}to{opacity:1;transform:scale(1)}}
    .step{padding:16px 32px;font-size:18px;font-weight:700;border:2px solid rgba(255,255,255,0.25);
          opacity:0.15;animation:stepIn 0.4s ease-out forwards;font-family:%(font)s;color:white;}
    .arrow{color:%(gray)s;font-size:24px;opacity:0.15;animation:stepIn 0.3s ease-out forwards;}
    </style>
    <div style="display:flex;align-items:center;gap:12px;padding:40px;">
      <div class="step" style="animation-delay:0s;">Seed</div>
      <div class="arrow" style="animation-delay:0.3s;">→</div>
      <div class="step" style="animation-delay:0.5s;">Expand</div>
      <div class="arrow" style="animation-delay:0.8s;">→</div>
      <div class="step" style="animation-delay:1.0s;background:%(sky)s;border-color:%(sky)s;">Verify</div>
      <div class="arrow" style="animation-delay:1.3s;">→</div>
      <div class="step" style="animation-delay:1.5s;">Collect</div>
      <div class="arrow" style="animation-delay:1.8s;">→</div>
      <div class="step" style="animation-delay:2.0s;">Cite</div>
    </div>"""),

    # Act III — 71% counter
    ("13_stat_counter", "light", """
    <style>
    @keyframes countUp{0%%{content:'0'}10%%{content:'8'}20%%{content:'17'}30%%{content:'29'}
    40%%{content:'38'}50%%{content:'48'}60%%{content:'55'}70%%{content:'62'}80%%{content:'67'}
    90%%{content:'70'}100%%{content:'71'}}
    .num::after{content:'71';font-size:200px;font-weight:900;line-height:0.82;letter-spacing:-10px;
    color:%(sky)s;animation:countUp 2s steps(10) forwards;}
    </style>
    <div style="padding:40px;font-family:%(font)s;">
      <div><span class="num"></span><span style="font-size:130px;font-weight:900;color:%(sky)s;">%%</span></div>
      <div style="font-size:22px;color:%(dark)s;margin-top:8px;">LLM win rate on complex reasoning</div>
    </div>"""),

    # Graph nodes for RLM demo
    ("12_graph_nodes", "dark", """
    <style>
    @keyframes nodeIn{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
    @keyframes lineIn{from{stroke-dashoffset:200}to{stroke-dashoffset:0}}
    circle{animation:nodeIn 0.5s ease-out forwards;opacity:0;}
    line{stroke-dasharray:200;animation:lineIn 0.8s ease-out forwards;}
    </style>
    <svg width="500" height="350" style="padding:20px;" xmlns="http://www.w3.org/2000/svg">
      <line x1="250" y1="80" x2="100" y2="180" stroke="%(sky)s" stroke-width="2" opacity="0.5" style="animation-delay:0.5s;"/>
      <line x1="250" y1="80" x2="400" y2="180" stroke="%(sky)s" stroke-width="2" opacity="0.5" style="animation-delay:0.7s;"/>
      <line x1="100" y1="180" x2="175" y2="280" stroke="%(sky)s" stroke-width="2" opacity="0.5" style="animation-delay:1.2s;"/>
      <line x1="400" y1="180" x2="325" y2="280" stroke="%(sky)s" stroke-width="2" opacity="0.5" style="animation-delay:1.4s;"/>
      <line x1="175" y1="280" x2="325" y2="280" stroke="%(sky)s" stroke-width="2" opacity="0.3" style="animation-delay:1.8s;"/>
      <circle cx="250" cy="80" r="30" fill="%(sky)s" style="animation-delay:0s;"/>
      <text x="250" y="85" text-anchor="middle" fill="white" font-size="13" font-weight="700" font-family="Helvetica Neue,sans-serif">Entity</text>
      <circle cx="100" cy="180" r="26" fill="%(leaf)s" style="animation-delay:0.4s;"/>
      <text x="100" y="185" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica Neue,sans-serif">Action</text>
      <circle cx="400" cy="180" r="26" fill="%(sand)s" style="animation-delay:0.6s;"/>
      <text x="400" y="185" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica Neue,sans-serif">Data</text>
      <circle cx="175" cy="280" r="24" fill="%(berry)s" style="animation-delay:1.0s;"/>
      <text x="175" y="285" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica Neue,sans-serif">Result</text>
      <circle cx="325" cy="280" r="24" fill="%(sky)s" opacity="0.7" style="animation-delay:1.6s;"/>
      <text x="325" y="285" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica Neue,sans-serif">Entity</text>
    </svg>"""),

    # Act III — Distillation pipeline
    ("17_distillation_pipeline", "dark", """
    <style>
    @keyframes slideRight{from{opacity:0;transform:translateX(-30px)}to{opacity:1;transform:translateX(0)}}
    .box{padding:18px 32px;font-size:17px;font-weight:700;animation:slideRight 0.6s ease-out forwards;opacity:0;
         font-family:%(font)s;color:white;}
    .arr{color:%(gray)s;font-size:28px;animation:slideRight 0.4s ease-out forwards;opacity:0;}
    </style>
    <div style="display:flex;align-items:center;gap:14px;padding:40px;">
      <div class="box" style="background:%(sky)s;animation-delay:0s;">Claude traces</div>
      <div class="arr" style="animation-delay:0.5s;">→</div>
      <div class="box" style="border:2px solid %(sky)s;animation-delay:0.8s;">TRL fine-tuning</div>
      <div class="arr" style="animation-delay:1.2s;">→</div>
      <div class="box" style="background:%(leaf)s;animation-delay:1.5s;">Gemma on-device</div>
    </div>"""),

    # Act IV — Checklist
    ("20_checklist", "dark", """
    <style>
    @keyframes checkIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
    .item{display:flex;align-items:center;gap:16px;margin-bottom:20px;animation:checkIn 0.5s ease-out forwards;opacity:0;
          font-family:%(font)s;color:white;}
    .circle{width:44px;height:44px;border-radius:50%%;border:3px solid;display:flex;align-items:center;
            justify-content:center;font-size:20px;font-weight:900;}
    </style>
    <div style="padding:40px;">
      <div class="item" style="animation-delay:0s;">
        <div class="circle" style="border-color:%(leaf)s;color:%(leaf)s;">✓</div>
        <div style="font-size:20px;font-weight:900;">Compression</div></div>
      <div class="item" style="animation-delay:0.4s;">
        <div class="circle" style="border-color:%(sky)s;color:%(sky)s;">✓*</div>
        <div style="font-size:20px;font-weight:900;">Navigation</div></div>
      <div class="item" style="animation-delay:0.8s;">
        <div class="circle" style="border-color:%(sand)s;color:%(sand)s;">→</div>
        <div style="font-size:20px;font-weight:900;">On-Device</div></div>
      <div class="item" style="animation-delay:1.2s;">
        <div class="circle" style="border-color:%(berry)s;color:%(berry)s;">?</div>
        <div style="font-size:20px;font-weight:900;">Data Connectivity</div></div>
    </div>"""),

    # Act V — Four pillars
    ("21_four_pillars", "dark", """
    <style>
    @keyframes pillarIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    .pillar{flex:1;padding:20px;border-top:3px solid %(sky)s;animation:pillarIn 0.6s ease-out forwards;
            opacity:0;font-family:%(font)s;color:white;}
    </style>
    <div style="display:flex;gap:12px;padding:40px;">
      <div class="pillar" style="animation-delay:0s;background:rgba(52,82,219,0.05);">
        <div style="font-size:15px;font-weight:900;">Limitless Context</div></div>
      <div class="pillar" style="animation-delay:0.3s;background:rgba(52,82,219,0.05);">
        <div style="font-size:15px;font-weight:900;">Billion-Scale Search</div></div>
      <div class="pillar" style="animation-delay:0.6s;background:rgba(52,82,219,0.05);">
        <div style="font-size:15px;font-weight:900;">On-Device Intelligence</div></div>
      <div class="pillar" style="animation-delay:0.9s;background:%(sky)s;">
        <div style="font-size:15px;font-weight:900;">Navigable KG</div></div>
    </div>"""),

    # Act V — Ghost citations counter
    ("24_ghost_counter", "light", """
    <style>
    @keyframes count7{0%%{content:'0'}20%%{content:'1'}40%%{content:'3'}60%%{content:'5'}80%%{content:'6'}100%%{content:'7'}}
    .num::after{content:'7';font-size:240px;font-weight:900;line-height:0.82;letter-spacing:-12px;
    color:%(berry)s;animation:count7 1.5s steps(5) forwards;}
    </style>
    <div style="padding:40px;font-family:%(font)s;">
      <div><span class="num"></span><span style="font-size:160px;font-weight:900;color:%(berry)s;">%%</span></div>
      <div style="font-size:28px;font-weight:700;color:%(dark)s;margin-top:12px;">Ghost Citations</div>
    </div>"""),

    # Act V — Explore/Verify/Cite panels
    ("27_explore_verify_cite", "dark", """
    <style>
    @keyframes panelIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    .panel{flex:1;padding:28px;animation:panelIn 0.6s ease-out forwards;opacity:0;font-family:%(font)s;color:white;}
    </style>
    <div style="display:flex;gap:20px;padding:40px;">
      <div class="panel" style="animation-delay:0s;border-top:4px solid %(sky)s;background:rgba(52,82,219,0.05);">
        <div style="font-size:24px;font-weight:900;color:%(sky)s;">Explore</div>
        <div style="font-size:18px;font-weight:700;margin-top:8px;">Can the agent find you?</div></div>
      <div class="panel" style="animation-delay:0.4s;border-top:4px solid %(leaf)s;background:rgba(34,162,134,0.05);">
        <div style="font-size:24px;font-weight:900;color:%(leaf)s;">Verify</div>
        <div style="font-size:18px;font-weight:700;margin-top:8px;">Can the agent confirm you?</div></div>
      <div class="panel" style="animation-delay:0.8s;border-top:4px solid %(sand)s;background:rgba(194,164,29,0.05);">
        <div style="font-size:24px;font-weight:900;color:%(sand)s;">Cite</div>
        <div style="font-size:18px;font-weight:700;margin-top:8px;">Can the agent cite you?</div></div>
    </div>"""),

    # Act V — Consistency bars
    ("26_consistency_bars", "light", """
    <style>
    @keyframes barGrow{from{width:0%%}to{width:var(--w)}}
    .bar{height:40px;border-radius:3px;animation:barGrow 1.2s ease-out forwards;margin-bottom:20px;}
    .label{font-size:15px;color:%(gray)s;margin-bottom:6px;font-family:%(font)s;}
    </style>
    <div style="padding:40px;">
      <div class="label">High volume, inconsistent</div>
      <div class="bar" style="--w:30%%;background:%(gray)s;"></div>
      <div class="label">Moderate, consistent naming</div>
      <div class="bar" style="--w:58%%;background:%(sand)s;animation-delay:0.3s;"></div>
      <div class="label">Consistent + cross-links</div>
      <div class="bar" style="--w:92%%;background:%(sky)s;animation-delay:0.6s;"></div>
    </div>"""),

    # Act V — AutoResearch panels
    ("28_autoresearch_panels", "dark", """
    <style>
    @keyframes panelIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    .panel{flex:1;padding:28px;animation:panelIn 0.6s ease-out forwards;opacity:0;font-family:%(font)s;color:white;}
    </style>
    <div style="display:flex;gap:20px;padding:40px;">
      <div class="panel" style="animation-delay:0s;border-top:4px solid %(leaf)s;background:rgba(34,162,134,0.05);">
        <div style="font-size:24px;font-weight:900;color:%(leaf)s;">Discover</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:8px;">Surface gaps. No manual curation.</div></div>
      <div class="panel" style="animation-delay:0.4s;border-top:4px solid %(sky)s;background:rgba(52,82,219,0.05);">
        <div style="font-size:24px;font-weight:900;color:%(sky)s;">Synthesize</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:8px;">Grounded, citable summaries.</div></div>
      <div class="panel" style="animation-delay:0.8s;border-top:4px solid %(sand)s;background:rgba(194,164,29,0.05);">
        <div style="font-size:24px;font-weight:900;color:%(sand)s;">Act</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:8px;">Queue remediation. Graph improves.</div></div>
    </div>"""),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ANIMATIONS)} content animations...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for name, mode, template in ANIMATIONS:
            html = template
            for k, v in T.items():
                html = html.replace(f"%({k})s", str(v))
            bg = T['dark'] if mode == "dark" else T['white']
            fg = T['white'] if mode == "dark" else T['dark']

            full_html = f"""<!DOCTYPE html><html><head><style>
            *{{margin:0;padding:0;box-sizing:border-box;}}
            body{{width:{T['W']}px;height:{T['H']}px;background:{bg};color:{fg};
                  font-family:{T['font']};overflow:hidden;}}
            </style></head><body>{html}</body></html>"""

            # GIF: capture 30 frames over 3s
            page = await browser.new_page(
                viewport={"width": T["W"], "height": T["H"]}, device_scale_factor=1)
            await page.set_content(full_html, wait_until="domcontentloaded")

            frames = []
            for i in range(30):
                await asyncio.sleep(0.1)
                frame_bytes = await page.screenshot(type="png")
                frames.append(frame_bytes)

            # Save preview (last frame)
            preview_path = OUT / f"{name}_preview.png"
            with open(preview_path, "wb") as f:
                f.write(frames[-1])

            # Save individual frames for GIF assembly
            # Use PIL if available, otherwise just save frames
            try:
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
                print(f"  {name}.gif ✓ ({gif_path.stat().st_size//1024} KB)")
            except ImportError:
                print(f"  {name}_preview.png ✓ (PIL not available for GIF)")

            await page.close()

        await browser.close()

    print(f"\n✓ All animations saved to {OUT}/")


if __name__ == "__main__":
    asyncio.run(main())

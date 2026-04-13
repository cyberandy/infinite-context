#!/usr/bin/env python3
"""
Content-focused cinemagraph GIFs for Google Slides overlay.
Each GIF animates a specific content element: counters, pipeline steps, diagrams.
Dark (#0D0D0D) background to match base slides. User layers on top in Slides.

Animation list mapped to 19-slide deck:
  01. Title text reveal
  02. Context window bars growing (4K → 128K → 1M → 10M)
  03. Quadratic cost bars (N vs 4× cost)
  04. Two routes diagram (Cram vs Navigate)
  05. [Chapter card — no animation needed]
  06. TurboQuant numbers counting (4.5× / 8× / 0)
  07. Zero-bias diagram
  08. [Chapter card — no animation needed]
  09. Pipeline steps highlighting (Seed → Expand → Verify → Collect → Cite)
  10. RLM cycle diagram rotating
  11. 71% counter
  12. Graph nodes appearing
  13. [Chapter card — no animation needed]
  14. KG pipeline diagram
  15. Playbook checklist reveal
  16. [Chapter card — no animation needed]
  17. Four pillars lighting up
  18. Thesis reveal
  19. [End card — no animation needed]
"""

import asyncio
from pathlib import Path
from PIL import Image
import io, math

OUT = Path("content_animations")

T = {
    "bg": "#0D0D0D",
    "white": "#FFFFFF",
    "sky": "#3452DB",
    "berry": "#D55471",
    "leaf": "#22A286",
    "gray": "#A1A7AF",
    "gray_light": "#F6F6F7",
    "dark": "#191919",
    "W": 960,   # Half-width overlays (user scales in Slides)
    "H": 540,
}

FRAMES = 60
DELAY = 60  # ms per frame (~16fps)


def ease_out(t):
    """Ease-out cubic."""
    return 1 - (1 - t)**3

def ease_in_out(t):
    return 3*t*t - 2*t*t*t


def frame_html(body, bg="#0D0D0D", w=960, h=540):
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{w}px;height:{h}px;background:{bg};overflow:hidden;
font-family:'Helvetica Neue','Helvetica','Arial',sans-serif;color:{T['white']};
display:flex;align-items:center;justify-content:center;}}
</style></head><body>{body}</body></html>"""


async def render_gif(page, name, gen_frame, desc, w=960, h=540, bg="#0D0D0D"):
    print(f"\n  [{name}] {desc}")
    frames = []
    for i in range(FRAMES):
        body = gen_frame(i, FRAMES)
        await page.set_content(frame_html(body, bg, w, h), wait_until="domcontentloaded")
        buf = await page.screenshot(type="png")
        img = Image.open(io.BytesIO(buf)).convert("RGB")
        frames.append(img)
        if (i+1) % 20 == 0:
            print(f"    frame {i+1}/{FRAMES}")

    path = OUT / f"{name}.gif"
    frames[0].save(str(path), save_all=True, append_images=frames[1:],
                   duration=DELAY, loop=0, optimize=False)
    print(f"    ✓ {path} ({path.stat().st_size//1024} KB)")

    # Save a preview at 75%
    frames[int(FRAMES*0.75)].save(str(OUT / f"{name}_preview.png"))


# ═══════════════════════════════════════
# ANIMATION: Context Window Bars (Slide 2)
# Bars grow showing 4K → 128K → 1M → 10M
# ═══════════════════════════════════════
def anim_context_bars(i, total):
    p = ease_out(min(1, i / (total * 0.7)))
    bars = [
        ("2020", "4K", 40, T['gray']),
        ("2023", "128K", 130, T['gray']),
        ("2024", "1M", 350, T['sky']),
        ("2025", "10M+", 750, T['sky']),
    ]
    html_parts = ['<div style="width:860px;padding:20px;">']
    for idx, (year, label, max_w, color) in enumerate(bars):
        delay = idx / len(bars)
        bar_p = ease_out(max(0, min(1, (p - delay * 0.3) / 0.7)))
        w = int(max_w * bar_p)
        opacity = min(1, bar_p * 2)
        html_parts.append(f'''
        <div style="display:flex;align-items:center;margin-bottom:24px;opacity:{opacity};">
          <div style="width:60px;font-size:16px;color:{T['gray']};font-weight:700;">{year}</div>
          <div style="height:40px;width:{w}px;background:{color};border-radius:4px;
                      transition:none;display:flex;align-items:center;padding-left:12px;">
            <span style="font-size:18px;font-weight:900;color:{T['white'] if color==T['sky'] else T['dark']};
                        opacity:{1 if bar_p>0.8 else 0};">{label}</span>
          </div>
        </div>''')
    html_parts.append('</div>')
    return "".join(html_parts)


# ═══════════════════════════════════════
# ANIMATION: Quadratic Cost (Slide 3)
# Two bars: N tokens vs 2N tokens = 4× cost
# ═══════════════════════════════════════
def anim_quadratic(i, total):
    p = ease_out(min(1, i / (total * 0.6)))
    p2 = ease_out(max(0, min(1, (i / total - 0.3) / 0.5)))

    bar1_h = int(120 * p)
    bar2_h = int(360 * p2)

    return f'''
    <div style="display:flex;align-items:flex-end;gap:80px;height:420px;padding-bottom:40px;">
      <div style="text-align:center;">
        <div style="width:120px;height:{bar1_h}px;background:{T['sky']};border-radius:6px 6px 0 0;"></div>
        <div style="font-size:16px;color:{T['gray']};margin-top:12px;font-weight:700;">N tokens</div>
      </div>
      <div style="text-align:center;">
        <div style="width:120px;height:{bar2_h}px;background:{T['berry']};border-radius:6px 6px 0 0;"></div>
        <div style="font-size:16px;color:{T['gray']};margin-top:12px;font-weight:700;">2N tokens</div>
        <div style="font-size:28px;color:{T['berry']};font-weight:900;margin-top:4px;
                    opacity:{1 if p2>0.8 else 0};">= 4× cost</div>
      </div>
    </div>'''


# ═══════════════════════════════════════
# ANIMATION: TurboQuant Numbers (Slide 6)
# Counter: 4.5× / 8× / 0
# ═══════════════════════════════════════
def anim_turboquant(i, total):
    p = i / total
    # Staggered counters
    v1 = min(4.5, 4.5 * ease_out(min(1, p / 0.4)))
    v2 = min(8.0, 8.0 * ease_out(max(0, min(1, (p - 0.15) / 0.4))))
    v3_opacity = ease_out(max(0, min(1, (p - 0.5) / 0.3)))

    return f'''
    <div style="display:flex;gap:80px;align-items:flex-end;">
      <div style="text-align:center;">
        <div style="font-size:100px;font-weight:900;color:{T['sky']};line-height:1;">{v1:.1f}×</div>
        <div style="font-size:16px;color:{T['gray']};margin-top:8px;">smaller KV cache</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:100px;font-weight:900;color:{T['sky']};line-height:1;">{int(v2)}×</div>
        <div style="font-size:16px;color:{T['gray']};margin-top:8px;">faster attention</div>
      </div>
      <div style="text-align:center;opacity:{v3_opacity};">
        <div style="font-size:100px;font-weight:900;color:{T['white']};line-height:1;">0</div>
        <div style="font-size:16px;color:{T['gray']};margin-top:8px;">retrieval degradation</div>
      </div>
    </div>'''


# ═══════════════════════════════════════
# ANIMATION: Pipeline Steps (Slide 9)
# Seed → Expand → Verify → Collect → Cite
# ═══════════════════════════════════════
def anim_pipeline(i, total):
    p = i / total
    steps = ["Seed", "Expand", "Verify", "Collect", "Cite"]
    html_parts = ['<div style="display:flex;align-items:center;gap:12px;">']
    for idx, step in enumerate(steps):
        step_start = idx / len(steps) * 0.7
        step_p = max(0, min(1, (p - step_start) / 0.25))
        is_active = step_p > 0.5
        is_current = 0.3 < step_p < 0.8

        bg = T['sky'] if is_active else "transparent"
        border = T['sky'] if is_active else "rgba(255,255,255,0.3)"
        scale = 1.08 if is_current else 1.0
        glow = f"0 0 20px {T['sky']}40" if is_current else "none"

        html_parts.append(f'''
        <div style="padding:14px 24px;font-size:17px;font-weight:700;
                    background:{bg};border:2px solid {border};border-radius:4px;
                    transform:scale({scale});box-shadow:{glow};
                    transition:none;opacity:{max(0.3, step_p)};">
          {step}
        </div>''')
        if idx < len(steps) - 1:
            arrow_op = max(0.2, step_p)
            html_parts.append(f'<div style="font-size:20px;color:{T["sky"]};opacity:{arrow_op};">→</div>')

    html_parts.append('</div>')
    return "".join(html_parts)


# ═══════════════════════════════════════
# ANIMATION: RLM Cycle (Slide 10)
# Circular: Seed → Expand → Verify → Collect → (loop)
# ═══════════════════════════════════════
def anim_rlm_cycle(i, total):
    p = i / total
    steps = ["Seed", "Expand", "Verify", "Collect"]
    n = len(steps)
    cx, cy, r = 220, 220, 150
    active_idx = int(p * n * 2) % n  # loops twice

    svg_parts = [f'<svg width="440" height="440" xmlns="http://www.w3.org/2000/svg">']
    # Circle path
    svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{T["gray"]}" stroke-width="2" opacity="0.3"/>')

    for idx, step in enumerate(steps):
        angle = (idx / n) * 2 * math.pi - math.pi / 2
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        is_active = idx == active_idx
        fill = T['sky'] if is_active else T['dark']
        stroke = T['sky'] if is_active else T['gray']
        font_color = T['white']
        glow = f'<circle cx="{x}" cy="{y}" r="42" fill="{T["sky"]}" opacity="0.15"/>' if is_active else ""
        svg_parts.append(glow)
        svg_parts.append(f'<circle cx="{x}" cy="{y}" r="36" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        svg_parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" fill="{font_color}" font-size="13" font-weight="700" font-family="Helvetica Neue,sans-serif">{step}</text>')

        # Arrow to next
        next_angle = ((idx + 1) / n) * 2 * math.pi - math.pi / 2
        ax = cx + (r - 50) * math.cos((angle + next_angle) / 2)
        ay = cy + (r - 50) * math.sin((angle + next_angle) / 2)

    svg_parts.append('</svg>')
    return f'<div style="display:flex;align-items:center;justify-content:center;">{"".join(svg_parts)}</div>'


# ═══════════════════════════════════════
# ANIMATION: 71% Counter (Slide 11)
# Big number counting up 0 → 71
# ═══════════════════════════════════════
def anim_71_counter(i, total):
    p = ease_out(min(1, i / (total * 0.6)))
    val = int(71 * p)
    # Flash effect when it lands
    landed = i > total * 0.6
    color = T['sky']
    scale = 1.05 if (total*0.58 < i < total*0.65) else 1.0

    return f'''
    <div style="text-align:center;transform:scale({scale});">
      <div style="font-size:220px;font-weight:900;color:{color};line-height:0.85;
                  letter-spacing:-10px;">
        {val}<span style="font-size:140px;">%</span>
      </div>
      <div style="font-size:24px;color:{T['white']};margin-top:16px;
                  opacity:{1 if p>0.3 else 0};">
        LLM win rate on complex reasoning
      </div>
      <div style="width:50px;height:3px;background:{T['berry']};margin:20px auto 0;
                  opacity:{1 if landed else 0};"></div>
      <div style="font-size:15px;color:{T['gray']};margin-top:12px;
                  opacity:{1 if landed else 0};">
        +4.55pp F1 · p &lt; 0.001 · n=519
      </div>
    </div>'''


# ═══════════════════════════════════════
# ANIMATION: Graph Nodes (Slide 12)
# Knowledge graph: nodes appear, edges connect
# ═══════════════════════════════════════
def anim_graph_nodes(i, total):
    p = i / total
    nodes = [
        (200, 180, "Entity A"),
        (500, 120, "Entity B"),
        (750, 200, "Entity C"),
        (350, 350, "Entity D"),
        (600, 380, "Entity E"),
        (150, 400, "Entity F"),
    ]
    edges = [(0,1),(1,2),(0,3),(3,4),(1,4),(2,4),(3,5),(0,5)]

    svg = ['<svg width="900" height="500" xmlns="http://www.w3.org/2000/svg">']

    # Edges appear first
    for idx, (a, b) in enumerate(edges):
        edge_p = max(0, min(1, (p - idx/len(edges)*0.5) / 0.3))
        if edge_p > 0:
            x1,y1,_ = nodes[a]; x2,y2,_ = nodes[b]
            # Partial line
            ex = x1 + (x2-x1)*edge_p
            ey = y1 + (y2-y1)*edge_p
            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{ex}" y2="{ey}" stroke="{T["sky"]}" stroke-width="2" opacity="0.4"/>')

    # Nodes
    for idx, (x, y, label) in enumerate(nodes):
        node_p = ease_out(max(0, min(1, (p - idx/len(nodes)*0.4) / 0.25)))
        r = int(28 * node_p)
        if node_p > 0:
            svg.append(f'<circle cx="{x}" cy="{y}" r="{r+8}" fill="{T["sky"]}" opacity="0.1"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{T["sky"]}" opacity="0.9"/>')
            if node_p > 0.7:
                svg.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="{T["white"]}" font-size="11" font-weight="700" font-family="Helvetica Neue,sans-serif">{label}</text>')

    svg.append('</svg>')
    return "".join(svg)


# ═══════════════════════════════════════
# ANIMATION: Four Pillars (Slide 17)
# Pillars light up one by one
# ═══════════════════════════════════════
def anim_four_pillars(i, total):
    p = i / total
    pillars = [
        ("Limitless Context", "TurboQuant compression"),
        ("Billion-Scale Search", "Zero-bias vector indexing"),
        ("On-Device Intelligence", "SLM navigator distillation"),
        ("Navigable Knowledge Graph", "The organizational layer"),
    ]
    html_parts = ['<div style="display:flex;gap:16px;">']
    for idx, (title, sub) in enumerate(pillars):
        start = idx / len(pillars) * 0.6
        pillar_p = ease_out(max(0, min(1, (p - start) / 0.3)))
        is_last = idx == len(pillars) - 1
        bg = T['sky'] if (is_last and pillar_p > 0.8) else T['dark']
        border_color = T['sky'] if pillar_p > 0.5 else T['gray']
        title_color = T['sky'] if (is_last and pillar_p > 0.8) else T['white']

        html_parts.append(f'''
        <div style="width:200px;padding:20px;border-top:3px solid {border_color};
                    background:{bg};opacity:{max(0.2, pillar_p)};
                    transform:translateY({int(20*(1-pillar_p))}px);">
          <div style="font-size:15px;font-weight:700;color:{title_color};margin-bottom:6px;">{title}</div>
          <div style="font-size:12px;color:{T['gray']};opacity:{pillar_p};">{sub}</div>
        </div>''')

    html_parts.append('</div>')
    return "".join(html_parts)


# ═══════════════════════════════════════
# ANIMATION: Playbook Checklist (Slide 15)
# Items reveal one by one with checkmarks
# ═══════════════════════════════════════
def anim_checklist(i, total):
    p = i / total
    items = [
        "Deploy structured data (JSON-LD)",
        "Build entity-centric content hubs",
        "Publish machine-readable FAQs",
        "Maintain a navigable knowledge graph",
        "Monitor AI citation patterns",
    ]
    html_parts = ['<div style="width:700px;">']
    for idx, item in enumerate(items):
        start = idx / len(items) * 0.7
        item_p = ease_out(max(0, min(1, (p - start) / 0.2)))
        check_opacity = 1 if item_p > 0.8 else 0
        html_parts.append(f'''
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;
                    opacity:{max(0, item_p)};transform:translateX({int(30*(1-item_p))}px);">
          <div style="width:28px;height:28px;border-radius:50%;border:2px solid {T['sky']};
                      display:flex;align-items:center;justify-content:center;
                      background:{T['sky'] if item_p>0.8 else 'transparent'};">
            <span style="color:{T['white']};font-weight:900;font-size:14px;opacity:{check_opacity};">✓</span>
          </div>
          <div style="font-size:18px;font-weight:500;">{item}</div>
        </div>''')
    html_parts.append('</div>')
    return "".join(html_parts)


# ═══════════════════════════════════════
ANIMATIONS = [
    ("02_context_bars", anim_context_bars, "Context window bars growing"),
    ("03_quadratic_cost", anim_quadratic, "Quadratic cost comparison"),
    ("06_turboquant_counter", anim_turboquant, "TurboQuant numbers counting up"),
    ("09_pipeline_steps", anim_pipeline, "Pipeline steps highlighting"),
    ("10_rlm_cycle", anim_rlm_cycle, "RLM cycle diagram"),
    ("11_stat_counter", anim_71_counter, "71% counter"),
    ("12_graph_nodes", anim_graph_nodes, "Knowledge graph nodes appearing"),
    ("15_playbook_checklist", anim_checklist, "Playbook checklist reveal"),
    ("17_four_pillars", anim_four_pillars, "Four pillars lighting up"),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ANIMATIONS)} content animations ({FRAMES} frames each)...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": T["W"], "height": T["H"]},
            device_scale_factor=2,  # 2× for crispness
        )
        for name, gen_fn, desc in ANIMATIONS:
            await render_gif(page, name, gen_fn, desc)
        await browser.close()

    print(f"\n✓ All content animations saved to {OUT}/")
    print(f"   Total: {sum(f.stat().st_size for f in OUT.glob('*.gif'))//1024} KB")


if __name__ == "__main__":
    asyncio.run(main())

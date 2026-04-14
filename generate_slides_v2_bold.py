#!/usr/bin/env python3
"""
Editorial Plan v2 — BOLD style (restored from slides_final).
Speaker-first: massive type, minimal text, lots of air.
29 slides, dark/light rhythm, CA textures.
"""

import asyncio
from pathlib import Path

OUT = Path("slides_v2")

T = {
    "dark": "#0D0D0D", "dark2": "#191919", "white": "#FFFFFF",
    "sky": "#3452DB", "berry": "#D55471", "leaf": "#22A286",
    "sand": "#C2A41D", "petal": "#A10269", "moss": "#125054",
    "gray": "#A1A7AF", "gray_light": "#F6F6F7",
    "W": 1920, "H": 1080,
    "font": "'Helvetica Neue','Helvetica','Arial',sans-serif",
}

def rule_row(prev, rule_num):
    n = len(prev); row = [0]*n
    for i in range(n):
        l,c,r = prev[(i-1)%n], prev[i], prev[(i+1)%n]
        row[i] = (rule_num >> ((l<<2)|(c<<1)|r)) & 1
    return row

def gen_grid(rule, rows, cols, start="center"):
    first = [0]*cols
    if start == "center": first[cols//2] = 1
    elif start == "right": first[-1] = 1
    elif start == "left": first[0] = 1
    else:
        import random; random.seed(42)
        for i in range(0, cols, 5): first[i] = 1
    grid = [first]
    for _ in range(rows - 1):
        grid.append(rule_row(grid[-1], rule))
    return grid

def svg_grid(grid, vis, cell, color, opacity, x, y):
    rects = []
    for r in range(min(vis, len(grid))):
        for c, val in enumerate(grid[r]):
            if val:
                cx, cy = x + c*cell, y + r*cell
                rects.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" fill="{color}" opacity="{opacity}"/>')
    return "\n".join(rects)

G30 = gen_grid(30, 100, 140, "center")
G90 = gen_grid(90, 80, 120, "center")
G110 = gen_grid(110, 90, 150, "right")
G90s = gen_grid(90, 50, 80, "center")
G110s = gen_grid(110, 60, 100, "right")

def html_slide(body, bg, fg, ca_svg=""):
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};
font-family:{T['font']};overflow:hidden;position:relative;color:{fg};}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}}
.c{{position:relative;z-index:1;width:100%;height:100%;padding:60px 70px;
display:flex;flex-direction:column;justify-content:center;}}
.section{{font-size:16px;font-weight:700;letter-spacing:5px;text-transform:uppercase;
color:{T['sky']};margin-bottom:24px;}}
.h{{font-weight:900;line-height:1.08;letter-spacing:-3px;}}
.bar{{height:5px;margin-top:32px;}}
</style></head><body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""

def dark(body, ca=""): return html_slide(body, T['dark'], T['white'], ca)
def light(body, ca=""): return html_slide(body, T['white'], T['dark2'], ca)


# ═══════════════════════════════════════════════════════════
# ACT I — THE CONTEXT EXPLOSION (1–4)
# ═══════════════════════════════════════════════════════════

def slide_01():
    ca = svg_grid(G30, 80, 14, T['sky'], 0.30, 520, 0)
    return dark(f"""
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
      <div class="section">SEO Week 2026</div>
      <div class="h" style="font-size:140px;max-width:900px;">Structure<br>Is the<br>Moat</div>
      <div class="bar" style="width:100px;background:{T['sky']};"></div>
      <div style="font-size:28px;color:{T['gray']};margin-top:28px;max-width:900px;line-height:1.5;">
        What the context explosion means for how AI<br>finds, navigates and ranks your content</div>
      <div style="font-size:22px;color:{T['gray']};opacity:0.6;margin-top:36px;">Andrea Volpini · WordLift</div>
    </div>""", ca)

def slide_02():
    ca = svg_grid(G30, 50, 10, T['sky'], 0.06, 0, 500)
    panels = [("KV Cache","Memory grows\nquadratically",T['sky']),("Vector DBs","Index bloat at\nbillion scale",T['sky']),
              ("On-Device","Models can't fit\nin your pocket",T['sky']),("AI Search\nAgents","Lose context mid-\nreasoning. Silently.",T['berry'])]
    cards = ""
    for title, desc, color in panels:
        cards += f'''<div style="flex:1;padding:36px;border-top:5px solid {color};background:rgba(255,255,255,0.03);">
          <div style="font-size:28px;font-weight:900;margin-bottom:14px;white-space:pre-line;">{title}</div>
          <div style="font-size:22px;color:{T['gray']};white-space:pre-line;">{desc}</div></div>'''
    return dark(f"""
    <div class="section">Act I — The Context Explosion</div>
    <div class="h" style="font-size:84px;margin-bottom:auto;">Why Context Has<br>a Weight Problem</div>
    <div style="display:flex;gap:24px;margin-bottom:40px;">{cards}</div>""", ca)

def slide_03():
    """FIX — Two-column, but BOLD treatment"""
    ca = svg_grid(G30, 70, 12, T['sky'], 0.15, 800, 0)
    return dark(f"""
    <div class="section">Act I — The Context Explosion</div>
    <div class="h" style="font-size:80px;margin-bottom:44px;">
      Search Was a Query.<br><span style="color:{T['sky']};">Now It's a Journey.</span></div>
    <div style="display:flex;gap:40px;">
      <div style="flex:1;padding:32px;border-top:4px solid {T['gray']};">
        <div style="font-size:16px;font-weight:700;color:{T['gray']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">The Old Model</div>
        <div style="font-size:22px;color:{T['gray']};line-height:2;">
          Stateless · Symmetric · One-shot<br>
          Keyword match + link authority<br>
          <span style="font-weight:700;color:{T['white']};font-size:26px;">The document was the unit</span></div>
      </div>
      <div style="flex:1;padding:32px;border-top:4px solid {T['sky']};">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">The Agent Model</div>
        <div style="font-size:22px;color:{T['gray']};line-height:2;">
          Stateful · Asymmetric · Multi-hop<br>
          Seeds entities → traverses graph<br>
          <span style="font-weight:700;color:{T['white']};font-size:26px;">The entity is the unit</span></div>
      </div>
    </div>
    <div style="padding:20px 28px;border-left:4px solid {T['berry']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:20px;color:{T['gray']};font-style:italic;">
        "If your entities aren't connected, you're invisible to the traversal."</div>
    </div>""", ca)

def slide_04():
    ca = svg_grid(G30, 40, 8, T['sky'], 0.04, 1200, 600)
    shifts = [("01","Retrieval → Navigation","Content competes on reachability, not relevance"),
              ("02","Documents → Entities","The unit of search is now an entity, not a page"),
              ("03","One Model → A System","Compression · Navigation · Structure working together")]
    items = ""
    for num, title, desc in shifts:
        items += f'''<div style="display:flex;gap:36px;margin-bottom:56px;align-items:flex-start;">
          <div style="font-size:80px;font-weight:900;color:{T['sky']};line-height:1;min-width:120px;">{num}</div>
          <div><div style="font-size:40px;font-weight:900;margin-bottom:10px;">{title}</div>
          <div style="font-size:26px;color:{T['gray']};">{desc}</div></div></div>'''
    return dark(f"""
    <div class="section">Act I — The Context Explosion</div>
    <div class="h" style="font-size:80px;margin-bottom:64px;">Three Shifts That Changed<br>What 'Findable' Means</div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">{items}</div>""", ca)


def slide_04b():
    """NEW — Memory Layer Evidence (+29.6%) — LIGHT"""
    ca = svg_grid(G90s, 30, 6, T['sky'], 0.04, 1400, 400)
    return light(f"""
    <div class="section">Act I — The Evidence</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      Structure Makes AI Smarter</div>
    <div style="font-size:24px;color:{T['gray']};margin-top:8px;">3-tier experiment: how structured data changes retrieval accuracy</div>
    <div style="display:flex;gap:28px;margin-top:48px;">
      <div style="flex:1;padding:36px;border-top:5px solid {T['gray']};">
        <div style="font-size:16px;font-weight:700;color:{T['gray']};letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">Layer 1</div>
        <div style="font-size:28px;font-weight:900;margin-bottom:8px;">Plain HTML</div>
        <div style="font-size:22px;color:{T['gray']};">Baseline accuracy</div>
        <div style="font-size:64px;font-weight:900;color:{T['gray']};margin-top:16px;">—</div></div>
      <div style="flex:1;padding:36px;border-top:5px solid {T['sand']};">
        <div style="font-size:16px;font-weight:700;color:{T['sand']};letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">Layer 2</div>
        <div style="font-size:28px;font-weight:900;margin-bottom:8px;">+ JSON-LD</div>
        <div style="font-size:22px;color:{T['gray']};">Modest improvement</div>
        <div style="font-size:64px;font-weight:900;color:{T['sand']};margin-top:16px;">+modest</div></div>
      <div style="flex:1;padding:36px;border-top:5px solid {T['sky']};background:rgba(52,82,219,0.03);">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">Layer 3</div>
        <div style="font-size:28px;font-weight:900;margin-bottom:8px;">Enhanced Entity Pages</div>
        <div style="font-size:22px;color:{T['gray']};">Standard RAG + Agentic RAG</div>
        <div style="font-size:80px;font-weight:900;color:{T['sky']};margin-top:16px;letter-spacing:-4px;">+29.6%</div></div>
    </div>
    <div style="padding:16px 24px;border-left:5px solid {T['berry']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:22px;color:{T['gray']};font-style:italic;">
        The same content. The same model. The only variable was structure.</div>
    </div>""", ca)


# ═══════════════════════════════════════════════════════════
# ACT II — COMPRESSION (5–10)
# ═══════════════════════════════════════════════════════════

def slide_05():
    ca = svg_grid(G90, 65, 10, T['sky'], 0.06, T['W']//2 - 60*10, 200)
    return dark(f"""
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
      <div class="section" style="margin-bottom:40px;">Act II</div>
      <div class="h" style="font-size:140px;max-width:1300px;">The<br>Compression<br>Paradox</div>
      <div class="bar" style="width:100px;background:{T['sky']};"></div>
      <div style="font-size:26px;color:{T['gray']};margin-top:28px;">
        High compression · Zero overhead · Geometric accuracy<br>
        <span style="color:{T['berry']};">Get it wrong and your similarity scores are silently biased.</span></div>
    </div>""", ca)

def slide_06():
    ca = svg_grid(G90s, 40, 8, T['sky'], 0.06, 60, 680)
    return light(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">TurboQuant</div>
    <div style="font-size:24px;color:{T['gray']};margin-top:8px;">Geometric compression without information loss</div>
    <div style="display:flex;gap:70px;margin-top:56px;align-items:flex-end;">
      <div><div style="font-size:150px;font-weight:900;line-height:0.9;color:{T['sky']};letter-spacing:-7px;">4.5×</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">smaller KV cache</div></div>
      <div><div style="font-size:150px;font-weight:900;line-height:0.9;color:{T['sky']};letter-spacing:-7px;">8×</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">faster attention</div></div>
      <div><div style="font-size:150px;font-weight:900;line-height:0.9;color:{T['dark2']};letter-spacing:-7px;">0</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">retrieval degradation</div></div>
    </div>
    <div class="bar" style="width:60px;background:{T['berry']};margin-top:40px;"></div>
    <div style="font-size:20px;color:{T['gray']};margin-top:20px;">
      PolarQuant → QJL · Data-oblivious · GPU-native · Zero codebook</div>""", ca)

def slide_07():
    ca = svg_grid(G90, 30, 8, T['berry'], 0.05, 1200, 100)
    return dark(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div class="h" style="font-size:72px;max-width:1300px;">Why 'Compressing Your<br>Embeddings' Can Silently<br>Destroy Your Rankings</div>
    <div style="display:flex;gap:48px;margin-top:56px;">
      <div style="flex:1;padding:28px;border-left:5px solid {T['berry']};">
        <div style="font-size:22px;font-weight:900;color:{T['berry']};margin-bottom:8px;">The Math</div>
        <div style="font-size:72px;font-weight:900;margin-bottom:8px;">2/π</div>
        <div style="font-size:20px;color:{T['gray']};">bias at 1-bit quantization</div></div>
      <div style="flex:1;padding:28px;border-left:5px solid {T['sand']};">
        <div style="font-size:22px;font-weight:900;color:{T['sand']};margin-bottom:8px;">The System</div>
        <div style="font-size:36px;font-weight:900;margin-bottom:8px;">Broken Compass</div>
        <div style="font-size:20px;color:{T['gray']};">Cosine similarity stops reflecting true similarity</div></div>
      <div style="flex:1;padding:28px;border-left:5px solid {T['gray']};">
        <div style="font-size:22px;font-weight:900;color:{T['gray']};margin-bottom:8px;">The Consequence</div>
        <div style="font-size:36px;font-weight:900;margin-bottom:8px;">Invisible Degradation</div>
        <div style="font-size:20px;color:{T['gray']};">No error. No alert. Just worse answers.</div></div>
    </div>""", ca)

def slide_08():
    ca = svg_grid(G90, 50, 10, T['sky'], 0.05, 1100, 0)
    return dark(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div class="h" style="font-size:80px;max-width:1100px;">The 1-Bit<br>Zero-Bias<br>Realignment</div>
    <div style="margin-top:44px;padding:36px;border:2px solid rgba(255,255,255,0.1);
                background:rgba(52,82,219,0.05);max-width:1000px;">
      <div style="font-size:28px;line-height:1.7;">
        <span style="color:{T['sky']};font-weight:700;">QJL correction →</span>
        Inner product estimates are now<br><span style="font-weight:900;">provably unbiased.</span></div>
    </div>
    <div class="bar" style="width:60px;background:{T['leaf']};margin-top:48px;"></div>
    <div style="font-size:22px;color:{T['gray']};margin-top:16px;">
      3,957s → 0.002s indexing at billion scale</div>""", ca)

def slide_09():
    ca = svg_grid(G90s, 30, 6, T['sky'], 0.05, 1400, 500)
    return light(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">The Quantization Landscape</div>
    <div style="margin-top:36px;">
      <table style="width:100%;border-collapse:collapse;font-size:22px;">
        <tr style="border-bottom:2px solid {T['dark2']};">
          <th style="text-align:left;padding:16px;font-weight:700;">Algorithm</th>
          <th style="text-align:center;padding:16px;font-weight:700;">Unbiased</th>
          <th style="text-align:center;padding:16px;font-weight:700;">Codebook-Free</th>
          <th style="text-align:center;padding:16px;font-weight:700;">GPU-Native</th>
          <th style="text-align:center;padding:16px;font-weight:700;">Data-Oblivious</th></tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:16px;color:{T['gray']};">PQ / OPQ</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:16px;color:{T['gray']};">ScaNN</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">partial</td><td style="text-align:center;">✗</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:16px;color:{T['gray']};">RaBitQ</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">✓</td><td style="text-align:center;">✗</td></tr>
        <tr style="background:{T['sky']}10;border-bottom:2px solid {T['sky']};">
          <td style="padding:16px;font-weight:900;color:{T['sky']};">TurboQuant</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td></tr>
      </table></div>
    <div class="bar" style="width:50px;background:{T['sky']};margin-top:40px;"></div>
    <div style="font-size:18px;color:{T['gray']};margin-top:16px;">First algorithm with all four properties simultaneously</div>""", ca)

def slide_10():
    """NEW — TurboQuant Demo — big, minimal"""
    ca = svg_grid(G90, 50, 10, T['sky'], 0.10, T['W']//2-45*10, 150)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;display:flex;align-items:center;gap:100px;">
      <div style="flex:1;">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">Try It</div>
        <div class="h" style="font-size:80px;">Watch It<br>Compress<br>Your Content</div>
        <div class="bar" style="width:60px;background:{T['sky']};margin-top:32px;"></div>
      </div>
      <div style="flex:0 0 320px;text-align:center;">
        <div style="width:280px;height:280px;border:3px solid {T['sky']};border-radius:12px;
                    display:flex;align-items:center;justify-content:center;background:rgba(52,82,219,0.08);">
          <div><div style="font-size:60px;font-weight:900;color:{T['sky']};">QR</div>
            <div style="font-size:14px;color:{T['gray']};margin-top:8px;">Scan to try live</div></div></div>
        <div style="margin-top:20px;font-size:20px;font-weight:700;font-family:monospace;color:{T['sky']};">wor.ai/turbo-quant</div>
      </div>
    </div>""", ca)


# ═══════════════════════════════════════════════════════════
# ACT III — THE NAVIGATOR (11–17)
# ═══════════════════════════════════════════════════════════

def slide_10b():
    """NEW — Context Timeline 2017→Today — DARK"""
    ca = svg_grid(G30, 50, 10, T['sky'], 0.06, 0, 400)
    return dark(f"""
    <div class="section">Act III — The Navigator</div>
    <div class="h" style="font-size:72px;margin-bottom:48px;">The Context Explosion<br>in Numbers</div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <div style="display:flex;gap:24px;align-items:flex-end;">
      <div style="flex:1;text-align:center;">
        <div style="font-size:22px;color:{T['gray']};margin-bottom:8px;">2017</div>
        <div style="height:60px;background:{T['gray']};opacity:0.3;border-radius:4px 4px 0 0;"></div>
        <div style="font-size:18px;color:{T['gray']};margin-top:8px;">512 tokens</div>
        <div style="font-size:14px;color:{T['gray']};opacity:0.5;">First WordLift model</div></div>
      <div style="flex:1;text-align:center;">
        <div style="font-size:22px;color:{T['gray']};margin-bottom:8px;">2020</div>
        <div style="height:100px;background:{T['gray']};opacity:0.4;border-radius:4px 4px 0 0;"></div>
        <div style="font-size:18px;color:{T['gray']};margin-top:8px;">4K tokens</div>
        <div style="font-size:14px;color:{T['gray']};opacity:0.5;">GPT-3</div></div>
      <div style="flex:1;text-align:center;">
        <div style="font-size:22px;color:{T['gray']};margin-bottom:8px;">2023</div>
        <div style="height:200px;background:{T['sand']};opacity:0.5;border-radius:4px 4px 0 0;"></div>
        <div style="font-size:18px;color:{T['gray']};margin-top:8px;">128K tokens</div>
        <div style="font-size:14px;color:{T['gray']};opacity:0.5;">GPT-4 Turbo</div></div>
      <div style="flex:1;text-align:center;">
        <div style="font-size:22px;color:{T['gray']};margin-bottom:8px;">2024</div>
        <div style="height:340px;background:{T['sky']};opacity:0.6;border-radius:4px 4px 0 0;"></div>
        <div style="font-size:18px;color:{T['gray']};margin-top:8px;">1M+ tokens</div>
        <div style="font-size:14px;color:{T['gray']};opacity:0.5;">Gemini</div></div>
      <div style="flex:1;text-align:center;">
        <div style="font-size:22px;color:{T['sky']};font-weight:700;margin-bottom:8px;">2026</div>
        <div style="height:420px;background:{T['sky']};border-radius:4px 4px 0 0;"></div>
        <div style="font-size:20px;font-weight:700;color:{T['sky']};margin-top:8px;">∞ context</div>
        <div style="font-size:14px;color:{T['sky']};opacity:0.7;">The question is now traversal</div></div>
    </div>
    </div>
    <div style="font-size:22px;color:{T['gray']};margin-bottom:40px;">
      <span style="color:{T['white']};font-weight:700;">Context windows grew 2,000,000×.</span> The question shifted from capacity to navigation.</div>""", ca)

def slide_10c():
    """NEW — Librarian vs Speed Reader — DARK"""
    ca = svg_grid(G110, 40, 8, T['sky'], 0.06, T['W']-50*8, 300)
    return dark(f"""
    <div class="section">Act III — The Navigator</div>
    <div class="h" style="font-size:72px;margin-bottom:auto;">Context Is Not a Bucket<br>to Fill. It's an Environment<br>to Explore.</div>
    <div style="display:flex;gap:40px;margin-bottom:60px;">
      <div style="flex:1;padding:40px;border-top:5px solid {T['gray']};">
        <div style="font-size:16px;font-weight:700;color:{T['gray']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;text-decoration:line-through;">Speed Reader</div>
        <div style="font-size:28px;font-weight:900;color:{T['gray']};margin-bottom:12px;">Traditional LLM</div>
        <div style="font-size:22px;color:{T['gray']};line-height:1.8;">
          Scans everything sequentially<br>
          Misses connections between sections<br>
          Loses context in long documents</div></div>
      <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">Librarian</div>
        <div style="font-size:28px;font-weight:900;color:{T['sky']};margin-bottom:12px;">RLM-on-KG</div>
        <div style="font-size:22px;color:{T['gray']};line-height:1.8;">
          Navigates the catalog of knowledge<br>
          Follows structural entity links<br>
          Finds what's connected, not just similar</div></div>
    </div>""", ca)

def slide_11():
    ca = svg_grid(G110, 70, 14, T['sky'], 0.25, 0, 0)
    box = "padding:16px 32px;font-size:20px;font-weight:700;border:2px solid rgba(255,255,255,0.25);"
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section">Act III — The Navigator</div>
      <div class="h" style="font-size:96px;">It Doesn't Search.</div>
      <div class="h" style="font-size:96px;color:{T['sky']};">It Explores.</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:80px;">
      <div style="{box}">Seed</div><div style="color:{T['gray']};font-size:22px;">→</div>
      <div style="{box}">Expand</div><div style="color:{T['gray']};font-size:22px;">→</div>
      <div style="{box} background:{T['sky']};border-color:{T['sky']};">Verify</div>
      <div style="color:{T['gray']};font-size:22px;">→</div>
      <div style="{box}">Collect</div><div style="color:{T['gray']};font-size:22px;">→</div>
      <div style="{box}">Cite</div>
      <div style="margin-left:auto;padding:8px 18px;font-size:13px;font-weight:700;
                  border:2px solid {T['berry']};color:{T['berry']};border-radius:20px;">arXiv 2025</div>
    </div>""", ca)

def slide_12():
    """NEW — RLM-on-KG Paper Announcement — BOLD"""
    ca = svg_grid(G110, 55, 12, T['sky'], 0.12, T['W']-60*12, 0)
    return dark(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="display:flex;gap:80px;margin-top:auto;margin-bottom:auto;">
      <div style="flex:0 0 45%;">
        <div style="font-size:14px;color:{T['berry']};font-weight:700;letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">Publishing Today · arXiv 2025</div>
        <div class="h" style="font-size:96px;">RLM-<br>on-KG</div>
        <div style="font-size:32px;font-weight:700;color:{T['sky']};margin-top:16px;">Live Navigation</div>
        <div class="bar" style="width:60px;background:{T['sky']};margin-top:28px;"></div>
        <div style="margin-top:28px;font-size:18px;font-weight:700;font-family:monospace;color:{T['sky']};">wor.ai/rlm-on-kg-explorer</div>
      </div>
      <div style="flex:1;display:flex;align-items:center;justify-content:center;">
        <div style="width:100%;height:380px;border:2px solid rgba(255,255,255,0.08);border-radius:8px;
                    background:rgba(52,82,219,0.03);display:flex;align-items:center;justify-content:center;">
          <svg width="440" height="280" xmlns="http://www.w3.org/2000/svg">
            <circle cx="220" cy="60" r="28" fill="{T['sky']}" opacity="0.9"/>
            <text x="220" y="65" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica Neue,sans-serif">Entity</text>
            <circle cx="80" cy="170" r="24" fill="{T['leaf']}" opacity="0.8"/>
            <text x="80" y="175" text-anchor="middle" fill="white" font-size="11" font-weight="700" font-family="Helvetica Neue,sans-serif">Action</text>
            <circle cx="360" cy="170" r="24" fill="{T['sand']}" opacity="0.8"/>
            <text x="360" y="175" text-anchor="middle" fill="white" font-size="11" font-weight="700" font-family="Helvetica Neue,sans-serif">Data</text>
            <circle cx="150" cy="250" r="22" fill="{T['berry']}" opacity="0.8"/>
            <text x="150" y="255" text-anchor="middle" fill="white" font-size="11" font-weight="700" font-family="Helvetica Neue,sans-serif">Result</text>
            <circle cx="290" cy="250" r="22" fill="{T['sky']}" opacity="0.6"/>
            <text x="290" y="255" text-anchor="middle" fill="white" font-size="11" font-weight="700" font-family="Helvetica Neue,sans-serif">Entity</text>
            <line x1="220" y1="88" x2="80" y2="146" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="220" y1="88" x2="360" y2="146" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="80" y1="194" x2="150" y2="228" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="360" y1="194" x2="290" y2="228" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="150" y1="250" x2="290" y2="250" stroke="{T['sky']}" stroke-width="2" opacity="0.3"/>
          </svg>
        </div>
      </div>
    </div>
    <div style="font-size:15px;color:{T['gray']};margin-bottom:60px;">
      Open-source · RDF-native · Graph traversal, live, in your browser ·
      <span style="color:{T['sky']};font-weight:700;">github.com/wordlift/rlm-on-kg</span></div>""", ca)

def slide_13():
    """FIX — 71% + scatter table — LIGHT, BOLD stat"""
    ca = svg_grid(G110s, 40, 10, T['sky'], 0.06, T['W']-80*10, 50)
    return light(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="display:flex;gap:60px;align-items:flex-start;">
      <div style="flex:0 0 auto;">
        <div style="font-size:220px;font-weight:900;line-height:0.82;letter-spacing:-12px;
                    color:{T['sky']};">71<span style="font-size:140px;">%</span></div>
        <div style="font-size:24px;color:{T['dark2']};margin-top:8px;font-weight:400;">
          LLM win rate on<br>complex reasoning</div>
      </div>
      <div style="flex:1;margin-top:24px;">
        <table style="width:100%;border-collapse:collapse;font-size:17px;">
          <tr style="border-bottom:2px solid {T['dark2']};">
            <th style="text-align:left;padding:12px;font-weight:700;">Evidence Distribution</th>
            <th style="text-align:center;padding:12px;font-weight:700;">Win Rate</th>
            <th style="text-align:center;padding:12px;font-weight:700;">F1 Gain</th></tr>
          <tr style="border-bottom:1px solid #e0e0e0;">
            <td style="padding:12px;color:{T['gray']};">Concentrated (1–5)</td>
            <td style="text-align:center;">62%</td><td style="text-align:center;">+1.85pp</td></tr>
          <tr style="border-bottom:1px solid #e0e0e0;">
            <td style="padding:12px;color:{T['gray']};">Scattered (6–10)</td>
            <td style="text-align:center;">65%</td><td style="text-align:center;">+3.21pp</td></tr>
          <tr style="border-bottom:1px solid #e0e0e0;">
            <td style="padding:12px;color:{T['gray']};">Highly scattered (11+)</td>
            <td style="text-align:center;">62%</td><td style="text-align:center;">+2.42pp</td></tr>
          <tr style="background:{T['sky']}10;border-bottom:2px solid {T['sky']};">
            <td style="padding:12px;font-weight:900;color:{T['sky']};">Complex Reasoning 11+</td>
            <td style="text-align:center;font-weight:900;color:{T['sky']};">71%</td>
            <td style="text-align:center;font-weight:900;color:{T['sky']};">+4.55pp</td></tr>
        </table>
      </div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['berry']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:17px;color:{T['gray']};">
        When the answer requires connecting facts across three product pages, two editorial pieces and a case study — the graph wins decisively.</div>
    </div>""", ca)

def slide_14():
    ca = svg_grid(G110, 40, 8, T['sky'], 0.04, 0, 700)
    return dark(f"""
    <div class="section">Act III — The Navigator</div>
    <div class="h" style="font-size:72px;margin-bottom:48px;">Separation of Concerns</div>
    <div style="display:flex;gap:40px;margin-top:auto;margin-bottom:80px;">
      <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:36px;font-weight:900;margin-bottom:12px;color:{T['sky']};">LLM Explores</div>
        <div style="font-size:24px;color:{T['gray']};line-height:1.6;">Navigation breadth<br>Graph traversal<br>Multi-hop reasoning</div></div>
      <div style="display:flex;align-items:center;font-size:56px;color:{T['gray']};">×</div>
      <div style="flex:1;padding:40px;border-top:5px solid {T['leaf']};background:rgba(34,162,134,0.05);">
        <div style="font-size:36px;font-weight:900;margin-bottom:12px;color:{T['leaf']};">Vectors Rank</div>
        <div style="font-size:24px;color:{T['gray']};line-height:1.6;">Cosine similarity<br>Geometric precision<br>Final ordering</div></div>
    </div>
    <div style="font-size:26px;color:{T['gray']};margin-bottom:60px;">
      <span style="color:{T['white']};font-weight:700;">Content must be structurally reachable.</span></div>""", ca)

def slide_15():
    ca = svg_grid(G110s, 30, 6, T['sky'], 0.04, 100, 700)
    models = [("Claude Haiku","+4.37pp",T['sky'],"Strong gain"),("Gemini Flash Lite","+0.84pp",T['sand'],"Marginal"),("Gemma 4","−0.78pp",T['berry'],"Negative")]
    cards = ""
    for name, delta, color, note in models:
        cards += f'''<div style="flex:1;padding:32px;border-top:5px solid {color};background:{color}08;">
          <div style="font-size:26px;font-weight:900;color:{T['dark2']};margin-bottom:8px;">{name}</div>
          <div style="font-size:80px;font-weight:900;color:{color};line-height:1;letter-spacing:-4px;">{delta}</div>
          <div style="font-size:20px;color:{T['gray']};margin-top:8px;">{note}</div></div>'''
    return light(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">The Model Capability Gap</div>
    <div style="font-size:24px;color:{T['gray']};margin-top:8px;">The gap is behavioral, not architectural</div>
    <div style="display:flex;gap:24px;margin-top:48px;">{cards}</div>
    <div class="bar" style="width:50px;background:{T['sky']};margin-top:40px;"></div>
    <div style="font-size:22px;color:{T['gray']};margin-top:16px;">
      The right model with the right graph beats a bigger model without one</div>""", ca)

def slide_15b():
    """NEW — GraphRAG Head-to-Head Benchmark — LIGHT"""
    ca = svg_grid(G110s, 25, 6, T['sky'], 0.04, 1500, 200)
    return light(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">Head-to-Head:<br>RLM vs GraphRAG</div>
    <div style="font-size:24px;color:{T['gray']};margin-top:8px;">Same benchmark. Same knowledge graph. Different approach.</div>
    <div style="display:flex;gap:40px;margin-top:48px;">
      <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(52,82,219,0.03);">
        <div style="font-size:20px;font-weight:700;color:{T['sky']};letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;">RLM-on-KG</div>
        <div style="font-size:100px;font-weight:900;color:{T['sky']};line-height:0.9;letter-spacing:-5px;">45.8</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">F1 Score</div></div>
      <div style="flex:1;padding:40px;border-top:5px solid {T['gray']};">
        <div style="font-size:20px;font-weight:700;color:{T['gray']};letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;">Microsoft GraphRAG</div>
        <div style="font-size:100px;font-weight:900;color:{T['gray']};line-height:0.9;letter-spacing:-5px;">45.6</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:8px;">F1 Score</div></div>
    </div>
    <div class="bar" style="width:70px;background:{T['berry']};margin-top:40px;"></div>
    <div style="font-size:24px;color:{T['gray']};margin-top:16px;">
      When evidence is scattered across <span style="color:{T['sky']};font-weight:700;">11+ chunks</span>:
      RLM wins <span style="color:{T['sky']};font-weight:700;">56%</span> of the time</div>""", ca)

def slide_17():
    """NEW — Distillation Bridge — BOLD, minimal"""
    ca = svg_grid(G110, 45, 10, T['sky'], 0.08, T['W']-55*10, 0)
    return dark(f"""
    <div class="section">Act III → IV — Bridge</div>
    <div class="h" style="font-size:80px;margin-bottom:56px;">
      The Gap Is Behavioral.<br><span style="color:{T['sky']};">That Means It's Trainable.</span></div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <div style="display:flex;gap:36px;margin-bottom:48px;">
      <div style="font-size:64px;font-weight:900;color:{T['sky']};line-height:1;min-width:90px;">01</div>
      <div><div style="font-size:30px;font-weight:900;">Decisions, not architecture</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:6px;">83% behavioral tie with heuristic. Same tools, same graph.</div></div>
    </div>
    <div style="display:flex;gap:36px;margin-bottom:48px;">
      <div style="font-size:64px;font-weight:900;color:{T['sky']};line-height:1;min-width:90px;">02</div>
      <div><div style="font-size:30px;font-weight:900;">Exploration traces = training data</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:6px;">519 navigation trajectories with F1 as ground truth.</div></div>
    </div>
    <div style="display:flex;gap:36px;margin-bottom:48px;">
      <div style="font-size:64px;font-weight:900;color:{T['sky']};line-height:1;min-width:90px;">03</div>
      <div><div style="font-size:30px;font-weight:900;">Fine-tune, distill, deploy</div>
        <div style="font-size:22px;color:{T['gray']};margin-top:6px;">TRL on Gemma 4 → on-device navigator, zero per query.</div></div>
    </div>
    </div>
    <div style="display:flex;align-items:center;gap:20px;
                padding:24px;border:2px solid rgba(255,255,255,0.1);background:rgba(52,82,219,0.03);">
      <div style="padding:16px 28px;background:{T['sky']};font-size:20px;font-weight:700;">Claude traces</div>
      <div style="color:{T['gray']};font-size:28px;">→</div>
      <div style="padding:16px 28px;border:2px solid {T['sky']};font-size:20px;font-weight:700;">TRL fine-tuning</div>
      <div style="color:{T['gray']};font-size:28px;">→</div>
      <div style="padding:16px 28px;background:{T['leaf']};font-size:20px;font-weight:700;">Gemma on-device</div>
    </div>""", ca)


# ═══════════════════════════════════════════════════════════
# ACT IV — SLM NAVIGATOR (18–20)
# ═══════════════════════════════════════════════════════════

def slide_18():
    ca = svg_grid(G90s, 40, 8, T['sky'], 0.05, 1400, 0)
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="h" style="font-size:80px;max-width:1100px;margin-bottom:44px;">
      Your Next Agent<br>Doesn't Live in the Cloud</div>
    <div style="display:flex;gap:32px;margin-top:auto;margin-bottom:60px;">
      <div style="flex:1;padding:32px;border-left:5px solid {T['leaf']};">
        <div style="font-size:32px;font-weight:900;color:{T['leaf']};margin-bottom:8px;">Secure</div>
        <div style="font-size:22px;color:{T['gray']};">Data never leaves the device</div></div>
      <div style="flex:1;padding:32px;border-left:5px solid {T['sky']};">
        <div style="font-size:32px;font-weight:900;color:{T['sky']};margin-bottom:8px;">Fast</div>
        <div style="font-size:22px;color:{T['gray']};">Sub-second, no round-trip</div></div>
      <div style="flex:1;padding:32px;border-left:5px solid {T['sand']};">
        <div style="font-size:32px;font-weight:900;color:{T['sand']};margin-bottom:8px;">Yours</div>
        <div style="font-size:22px;color:{T['gray']};">Trained on your graph</div></div>
    </div>
    <div style="font-size:14px;color:{T['gray']};opacity:0.5;margin-bottom:60px;">
      github.com/wordlift/google-ai-edge/tree/main/wordlift-graphql</div>""", ca)

def slide_19():
    ca = svg_grid(G90, 35, 8, T['sky'], 0.04, 200, 650)
    steps = [("01","Connectivity enables distillation","Connected data teaches your model to navigate"),
             ("02","Connected data multiplies","Cross-property links compound the advantage"),
             ("03","Disconnected data = dead end","Without structure, training has no signal")]
    items = ""
    for num, title, desc in steps:
        items += f'''<div style="display:flex;gap:36px;margin-bottom:56px;align-items:flex-start;">
          <div style="font-size:80px;font-weight:900;color:{T['sky']};line-height:1;min-width:120px;">{num}</div>
          <div><div style="font-size:36px;font-weight:900;margin-bottom:8px;">{title}</div>
          <div style="font-size:24px;color:{T['gray']};">{desc}</div></div></div>'''
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="h" style="font-size:72px;margin-bottom:auto;">Well-Connected Data Is<br>the Training Advantage</div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">{items}</div>
    <div class="bar" style="width:70px;background:{T['berry']};"></div>
    <div style="font-size:24px;color:{T['gray']};margin-top:16px;">Data connectivity is your AI training pipeline.</div>""", ca)

def slide_20():
    ca = svg_grid(G90s, 30, 8, T['leaf'], 0.05, 1300, 400)
    checks = [("Compression","✓",T['leaf'],"TurboQuant"),("Navigation","✓*",T['sky'],"Conditional"),
              ("On-Device","→",T['sand'],"18 months"),("Data Connectivity","?",T['berry'],"You control this today")]
    items = ""
    for label, status, color, note in checks:
        items += f'''<div style="display:flex;align-items:center;gap:32px;margin-bottom:40px;">
          <div style="width:80px;height:80px;border-radius:50%;border:4px solid {color};
                      display:flex;align-items:center;justify-content:center;
                      font-size:32px;font-weight:900;color:{color};">{status}</div>
          <div><div style="font-size:34px;font-weight:900;">{label}</div>
          <div style="font-size:22px;color:{T['gray']};">{note}</div></div></div>'''
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="h" style="font-size:72px;margin-bottom:auto;">The Floor Is Set</div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">{items}</div>""", ca)


# ═══════════════════════════════════════════════════════════
# ACT V — STRUCTURE IS THE MOAT (21–30)
# ═══════════════════════════════════════════════════════════

def slide_21():
    ca_sky = svg_grid(G90, 65, 12, T['sky'], 0.15, T['W']//2-60*12, 40)
    ca_leaf = svg_grid(G110s, 35, 10, T['leaf'], 0.08, T['W']-50*10, T['H']-35*10)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="h" style="font-size:80px;">The Moat Is Not<br>the Model.</div>
      <div class="h" style="font-size:80px;color:{T['sky']};margin-top:8px;">The Moat Is<br>the Graph.</div>
    </div>
    <div style="display:flex;gap:16px;margin-bottom:80px;">
      <div style="flex:1;padding:24px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:20px;font-weight:900;">Limitless Context</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:20px;font-weight:900;">Billion-Scale Search</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:20px;font-weight:900;">On-Device Intelligence</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['sky']};background:{T['sky']};">
        <div style="font-size:20px;font-weight:900;">Navigable Knowledge Graph</div></div>
    </div>""", ca_sky + ca_leaf)

def slide_22():
    ca = svg_grid(G110, 70, 12, T['sky'], 0.08, T['W']//2-50*12, 100)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section" style="margin-bottom:40px;">Act V</div>
      <div class="h" style="font-size:130px;">The SEO<br>Playbook</div>
      <div class="bar" style="width:90px;background:{T['sky']};"></div>
      <div style="font-size:28px;color:{T['gray']};margin-top:28px;">What to actually do about all of this</div>
    </div>""", ca)

def slide_23():
    """Visibility Shift — LIGHT"""
    ca = svg_grid(G110s, 35, 8, T['sky'], 0.05, T['W']-60*8, 200)
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      AI Visibility Is Shifting</div>
    <div style="font-size:22px;color:{T['gray']};margin-top:8px;">From mentions to reasoning utility</div>
    <div style="display:flex;gap:32px;margin-top:40px;">
      <div style="flex:1;padding:32px;border-top:5px solid {T['gray']};">
        <div style="font-size:16px;font-weight:700;color:{T['gray']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;text-decoration:line-through;">Mentions Era</div>
        <div style="font-size:22px;color:{T['gray']};line-height:2;">
          Present in training data<br>Passive: be cited<br>Measured by: brand recall</div>
      </div>
      <div style="flex:1;padding:32px;border-top:5px solid {T['sky']};">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">Reasoning Utility</div>
        <div style="font-size:22px;color:{T['dark2']};line-height:2;">
          Entities connected and traversable<br>Active: be <span style="color:{T['sky']};font-weight:700;">reachable</span>, verifiable, citable<br>Measured by: citation in agent outputs</div>
      </div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['sky']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:17px;color:{T['gray']};font-style:italic;">
        "GPT-5.4 decides whether your content is worth navigating to. That decision is made by following entity links."</div>
    </div>""", ca)

def slide_24():
    """Ghost Citations — LIGHT"""
    ca = svg_grid(G30, 40, 8, T['berry'], 0.05, 0, 550)
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="margin-top:32px;">
      <div style="font-size:300px;font-weight:900;line-height:0.82;letter-spacing:-16px;
                  color:{T['berry']};">7<span style="font-size:200px;">%</span></div>
      <div style="font-size:36px;font-weight:700;color:{T['dark2']};margin-top:12px;">Ghost Citations</div>
      <div class="bar" style="width:60px;background:{T['berry']};margin-top:24px;"></div>
      <div style="font-size:22px;color:{T['gray']};margin-top:20px;max-width:1000px;line-height:1.6;">
        AI agents cite content that never appeared in the top-10.<br>
        They navigated there through entity links — not ranking signals.</div>
    </div>
    <div style="display:flex;gap:24px;margin-top:auto;margin-bottom:60px;">
      <div style="flex:1;padding:24px;border-top:3px solid {T['berry']};">
        <div style="font-size:18px;font-weight:700;color:{T['dark2']};">Rankings ≠ AI citations</div></div>
      <div style="flex:1;padding:24px;border-top:3px solid {T['sky']};">
        <div style="font-size:18px;font-weight:700;color:{T['dark2']};">Navigation graph = new signal</div></div>
    </div>""", ca)

def slide_25():
    """How AI Reads — LIGHT"""
    ca = svg_grid(G110s, 25, 6, T['sky'], 0.04, 1500, 600)
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="font-size:64px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">How AI Reads Your Content</div>
    <div style="margin-top:32px;">
      <table style="width:100%;border-collapse:collapse;font-size:20px;">
        <tr style="border-bottom:2px solid {T['dark2']};">
          <th style="text-align:left;padding:14px;font-weight:700;width:20%;"></th>
          <th style="text-align:center;padding:14px;font-weight:700;color:{T['gray']};">GPT-3 era</th>
          <th style="text-align:center;padding:14px;font-weight:700;color:{T['gray']};">GPT-4 era</th>
          <th style="text-align:center;padding:14px;font-weight:700;color:{T['sky']};">GPT-5.4 era</th></tr>
        <tr style="border-bottom:1px solid #e0e0e0;"><td style="padding:14px;font-weight:700;">Method</td>
          <td style="text-align:center;color:{T['gray']};">Pattern match</td>
          <td style="text-align:center;color:{T['gray']};">Semantic similarity</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Graph traversal</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;"><td style="padding:14px;font-weight:700;">Unit</td>
          <td style="text-align:center;color:{T['gray']};">Token</td>
          <td style="text-align:center;color:{T['gray']};">Embedding</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Entity</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;"><td style="padding:14px;font-weight:700;">What matters</td>
          <td style="text-align:center;color:{T['gray']};">Keyword density</td>
          <td style="text-align:center;color:{T['gray']};">Vector proximity</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Structural connectivity</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;"><td style="padding:14px;font-weight:700;">Content's job</td>
          <td style="text-align:center;color:{T['gray']};">Be present</td>
          <td style="text-align:center;color:{T['gray']};">Be similar</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Be reachable</td></tr>
        <tr style="border-bottom:2px solid {T['dark2']};"><td style="padding:14px;font-weight:700;">Failure mode</td>
          <td style="text-align:center;color:{T['gray']};">Not indexed</td>
          <td style="text-align:center;color:{T['gray']};">Low similarity</td>
          <td style="text-align:center;font-weight:700;color:{T['berry']};">Disconnected from graph</td></tr>
      </table></div>
    <div class="bar" style="width:60px;background:{T['sky']};margin-top:40px;"></div>
    <div style="font-size:18px;color:{T['gray']};margin-top:16px;">
      Each generation changed what 'findable' means. You can't optimize for GPT-5.4 using GPT-4 intuitions.</div>""", ca)

def slide_26():
    """Consistency — LIGHT"""
    ca = svg_grid(G110s, 20, 6, T['sky'], 0.04, 100, 750)
    bars = [("High volume, inconsistent naming",30,T['gray'],"Low"),
            ("Moderate volume, consistent naming",58,T['sand'],"Moderate"),
            ("Consistent + cross-property links",92,T['sky'],"High")]
    bar_html = ""
    for label, pct, color, note in bars:
        bar_html += f'''<div style="margin-bottom:28px;">
          <div style="font-size:17px;color:{T['gray']};margin-bottom:8px;">{label}</div>
          <div style="height:44px;width:{pct}%;background:{color};border-radius:3px;
                      display:flex;align-items:center;padding-left:16px;">
            <span style="font-size:15px;font-weight:700;color:white;">{note} citation rate</span></div></div>'''
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="font-size:56px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">Consistency,<br>Not Crawling</div>
    <div style="margin-top:56px;max-width:1000px;">{bar_html}</div>
    <div style="padding:16px 24px;border-left:4px solid {T['sky']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:17px;color:{T['gray']};">
        If your entity is named differently in your blog, product pages and Schema.org — the agent can't resolve them. Three weak signals instead of one strong one.</div>
    </div>""", ca)

def slide_27():
    """Explore → Verify → Cite — ELEVATED paradigm shift — DARK"""
    ca = svg_grid(G110, 55, 10, T['sky'], 0.10, T['W']-60*10, 0)
    return dark(f"""
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
      <div class="section">The New Paradigm</div>
      <div style="font-size:48px;font-weight:900;text-decoration:line-through;color:{T['gray']};opacity:0.4;margin-bottom:24px;">
        Crawl → Index → Rank</div>
      <div class="h" style="font-size:88px;color:{T['sky']};margin-bottom:80px;">Explore → Verify → Cite</div>
      <div style="display:flex;gap:60px;">
        <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(52,82,219,0.05);">
          <div style="font-size:32px;font-weight:900;color:{T['sky']};margin-bottom:16px;">Explore</div>
          <div style="font-size:24px;font-weight:700;margin-bottom:12px;">Can the agent find you?</div>
          <div style="font-size:18px;color:{T['gray']};">Entity links · stable URIs · navigable KG</div></div>
        <div style="flex:1;padding:40px;border-top:5px solid {T['leaf']};background:rgba(34,162,134,0.05);">
          <div style="font-size:32px;font-weight:900;color:{T['leaf']};margin-bottom:16px;">Verify</div>
          <div style="font-size:24px;font-weight:700;margin-bottom:12px;">Can the agent confirm you?</div>
          <div style="font-size:18px;color:{T['gray']};">Provenance · attribution · consistent IDs</div></div>
        <div style="flex:1;padding:40px;border-top:5px solid {T['sand']};background:rgba(194,164,29,0.05);">
          <div style="font-size:32px;font-weight:900;color:{T['sand']};margin-bottom:16px;">Cite</div>
          <div style="font-size:24px;font-weight:700;margin-bottom:12px;">Can the agent cite you?</div>
          <div style="font-size:18px;color:{T['gray']};">Stable URLs · canonical entities · machine-readable</div></div>
      </div>
    </div>
    <div style="padding:24px 32px;border-left:5px solid {T['berry']};margin-top:40px;margin-bottom:60px;">
      <div style="font-size:24px;color:{T['gray']};">
        The pipeline has changed. The optimization targets have changed.<br>
        <span style="color:{T['white']};font-weight:700;">Most content strategies haven't.</span></div>
    </div>""", ca)

def slide_28():
    """AutoResearch — DARK"""
    ca = svg_grid(G90, 40, 10, T['sky'], 0.06, T['W']//2-40*10, 300)
    return dark(f"""
    <div class="section">Act V — Structure Is the Moat</div>
    <div class="h" style="font-size:64px;margin-bottom:16px;">What Happens When<br>You Build the Graph</div>
    <div style="font-size:22px;color:{T['sky']};font-weight:700;margin-bottom:48px;">
      AutoResearch — Autonomous knowledge work</div>
    <div style="display:flex;gap:24px;">
      <div style="flex:1;padding:32px;border-top:4px solid {T['leaf']};background:rgba(34,162,134,0.05);">
        <div style="font-size:28px;font-weight:900;color:{T['leaf']};margin-bottom:12px;">Discover</div>
        <div style="font-size:16px;color:{T['gray']};line-height:1.6;">
          Surface gaps, unanswered questions.<br>No manual curation.</div></div>
      <div style="flex:1;padding:32px;border-top:4px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:28px;font-weight:900;color:{T['sky']};margin-bottom:12px;">Synthesize</div>
        <div style="font-size:16px;color:{T['gray']};line-height:1.6;">
          Grounded, citable summaries.<br>Every claim traces to a source.</div></div>
      <div style="flex:1;padding:32px;border-top:4px solid {T['sand']};background:rgba(194,164,29,0.05);">
        <div style="font-size:28px;font-weight:900;color:{T['sand']};margin-bottom:12px;">Act</div>
        <div style="font-size:16px;color:{T['gray']};line-height:1.6;">
          Missing links, inconsistent IDs,<br>unclaimed Wikidata entries — queued.</div></div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['berry']};margin-top:auto;margin-bottom:60px;">
      <div style="font-size:18px;color:{T['gray']};">
        This isn't a future capability. This is what well-connected data enables now.</div>
    </div>""", ca)

def slide_29():
    ca = svg_grid(G90, 55, 10, T['sky'], 0.08, T['W']//2-55*10, 80)
    return light(f"""
    <div class="section">Act V — Structure Is the Moat</div>
    <div style="font-size:56px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      What 'Well-Connected'<br>Actually Means</div>
    <div style="display:flex;gap:24px;margin-top:48px;">
      <div style="flex:1;">
        <div style="font-size:14px;font-weight:700;color:{T['sky']};letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;">Internal</div>
        <div style="padding:24px;border:2px solid #e0e0e0;margin-bottom:12px;">
          <div style="font-size:18px;font-weight:700;color:{T['dark2']};">Products → Editorial</div></div>
        <div style="padding:24px;border:2px solid #e0e0e0;">
          <div style="font-size:18px;font-weight:700;color:{T['dark2']};">Docs → Support → Product</div></div>
      </div>
      <div style="flex:1;">
        <div style="font-size:14px;font-weight:700;color:{T['sky']};letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;">External</div>
        <div style="padding:24px;border:2px solid #e0e0e0;margin-bottom:12px;">
          <div style="font-size:18px;font-weight:700;color:{T['dark2']};">Wikidata / Schema.org</div></div>
        <div style="padding:24px;border:2px solid #e0e0e0;">
          <div style="font-size:18px;font-weight:700;color:{T['dark2']};">Partner Ecosystems</div></div>
      </div>
    </div>
    <div class="bar" style="width:80px;background:{T['sky']};margin-top:48px;"></div>
    <div style="font-size:20px;color:{T['gray']};margin-top:16px;font-style:italic;">
      Can an agent that starts from something adjacent find its way to you?</div>""", ca)

def slide_30():
    ca_sky = svg_grid(G90, 65, 12, T['sky'], 0.30, T['W']//2-60*12, 50)
    ca_berry = svg_grid(G30, 30, 6, T['berry'], 0.04, 0, 0)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;max-width:1100px;">
      <div class="h" style="font-size:64px;">Context windows will keep growing.<br>Models will keep getting cheaper.</div>
      <div style="margin-top:32px;">
        <div class="h" style="font-size:64px;color:{T['sky']};">The variable that compounds<br>is your data connectivity.</div>
      </div>
      <div class="bar" style="width:90px;background:{T['sky']};margin-top:44px;"></div>
      <div style="font-size:32px;margin-top:28px;font-weight:700;">Structure your knowledge now.</div>
    </div>
    <div style="margin-top:auto;margin-bottom:80px;display:flex;gap:32px;">
      <div style="font-size:15px;color:{T['gray']};"><span style="font-weight:700;color:{T['sky']};">Paper</span> · github.com/wordlift/rlm-on-kg</div>
      <div style="font-size:15px;color:{T['gray']};"><span style="font-weight:700;color:{T['sky']};">Code</span> · github.com/cyberandy/infinite-context</div>
      <div style="font-size:15px;color:{T['gray']};"><span style="font-weight:700;color:{T['sky']};">GraphQL</span> · github.com/wordlift/google-ai-edge</div>
      <div style="font-size:15px;color:{T['gray']};">Andrea Volpini · WordLift · SEO Week 2026</div>
    </div>""", ca_sky + ca_berry)


ALL_SLIDES = [
    ("01_title.png", slide_01), ("02_weight_problem.png", slide_02),
    ("03_query_to_journey.png", slide_03), ("04_three_shifts.png", slide_04),
    ("04b_memory_layer.png", slide_04b),
    ("05_compression_paradox.png", slide_05), ("06_turboquant.png", slide_06),
    ("07_silent_ranking.png", slide_07), ("08_zero_bias.png", slide_08),
    ("09_quant_landscape.png", slide_09), ("10_turbo_demo.png", slide_10),
    ("10b_context_timeline.png", slide_10b), ("10c_librarian.png", slide_10c),
    ("11_navigator.png", slide_11), ("12_rlm_demo.png", slide_12),
    ("13_conditional_advantage.png", slide_13), ("14_separation.png", slide_14),
    ("15_model_gap.png", slide_15), ("15b_graphrag.png", slide_15b),
    ("17_distillation.png", slide_17),
    ("18_slm_edge.png", slide_18), ("19_connected_data.png", slide_19),
    ("20_floor_set.png", slide_20), ("21_moat_graph.png", slide_21),
    ("22_seo_playbook_chapter.png", slide_22), ("23_visibility_shift.png", slide_23),
    ("24_ghost_citations.png", slide_24), ("25_gpt_reads_differently.png", slide_25),
    ("26_consistency_not_crawling.png", slide_26), ("27_explore_verify_cite.png", slide_27),
    ("28_autoResearch.png", slide_28), ("29_well_connected.png", slide_29),
    ("30_closing.png", slide_30),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    # Clean old files
    for f in OUT.glob("*.png"): f.unlink()
    print(f"Generating {len(ALL_SLIDES)} slides — v2 BOLD style...\n")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": T["W"], "height": T["H"]}, device_scale_factor=1)
        for fname, gen in ALL_SLIDES:
            print(f"  {fname}...", end=" ", flush=True)
            await page.set_content(gen(), wait_until="domcontentloaded")
            path = OUT / fname
            await page.screenshot(path=str(path), type="png")
            print(f"✓ ({path.stat().st_size//1024} KB)")
        await browser.close()
    total = sum(f.stat().st_size for f in OUT.glob("*.png")) // 1024
    print(f"\n✓ All {len(ALL_SLIDES)} slides → {OUT}/ ({total} KB total)")

if __name__ == "__main__":
    asyncio.run(main())

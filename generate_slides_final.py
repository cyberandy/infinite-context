#!/usr/bin/env python3
"""
Generate all 19 base slide PNGs — Style V3 (dark/light rhythm).
Dark slides: narrative flow, CA textures.
Light slides: emphasis moments (key stats, pivots, data reveals).

Slide → mode mapping:
  01 Title → DARK (hero)
  02 Context Weight → DARK
  03 Query→Journey → DARK
  04 Three Shifts → DARK
  05 Compression Paradox (chapter) → DARK
  06 TurboQuant → LIGHT (data emphasis)
  07 Silent Ranking → DARK
  08 Zero-Bias → DARK
  09 Quantization Landscape → LIGHT (data emphasis)
  10 Navigator Intro → DARK
  11 71% Stat → LIGHT (stat emphasis)
  12 Separation → DARK
  13 Model Gap → LIGHT (data emphasis)
  14 SLM Edge → DARK
  15 Connected Data → DARK
  16 Floor Is Set → DARK
  17 Four Pillars → DARK (climax)
  18 Well-Connected → LIGHT (pivot emphasis)
  19 Closing → DARK (hero)
"""

import asyncio
import math
from pathlib import Path

OUT = Path("slides_final")

# ═══════════════════════════════════════
# DESIGN TOKENS
# ═══════════════════════════════════════
T = {
    "dark": "#0D0D0D",
    "dark2": "#191919",
    "white": "#FFFFFF",
    "sky": "#3452DB",
    "berry": "#D55471",
    "leaf": "#22A286",
    "sand": "#C2A41D",
    "petal": "#A10269",
    "moss": "#125054",
    "gray": "#A1A7AF",
    "gray_light": "#F6F6F7",
    "W": 1920,
    "H": 1080,
    "font": "'Helvetica Neue','Helvetica','Arial',sans-serif",
}

# ═══════════════════════════════════════
# CA ENGINE
# ═══════════════════════════════════════
def rule_row(prev, rule_num):
    n = len(prev)
    row = [0]*n
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

# Pre-generate grids
G30 = gen_grid(30, 100, 140, "center")
G90 = gen_grid(90, 80, 120, "center")
G110 = gen_grid(110, 90, 150, "right")
G90s = gen_grid(90, 50, 80, "center")  # small
G110s = gen_grid(110, 60, 100, "right")  # small


# ═══════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════
def html_slide(body, bg, fg, ca_svg=""):
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};
font-family:{T['font']};overflow:hidden;position:relative;color:{fg};}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}}
.c{{position:relative;z-index:1;width:100%;height:100%;padding:80px 100px;
display:flex;flex-direction:column;}}
.section{{font-size:14px;font-weight:700;letter-spacing:5px;text-transform:uppercase;
color:{T['sky']};margin-bottom:28px;}}
.headline{{font-weight:900;line-height:0.94;letter-spacing:-5px;}}
.sub{{font-weight:400;line-height:1.5;}}
.bar{{height:4px;margin-top:36px;margin-bottom:0;}}
.pill{{padding:14px 26px;font-size:16px;font-weight:700;border-radius:3px;}}
</style></head><body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""


def dark(body, ca=""):
    return html_slide(body, T['dark'], T['white'], ca)

def light(body, ca=""):
    return html_slide(body, T['white'], T['dark2'], ca)


# ═══════════════════════════════════════
# ALL 19 SLIDES
# ═══════════════════════════════════════

def slide_01():
    """Title: Structure Is the Moat"""
    ca = svg_grid(G30, 80, 14, T['sky'], 0.30, 520, 0)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section">SEO Week 2026</div>
      <div class="headline" style="font-size:120px;max-width:700px;">
        Structure<br>Is the<br>Moat</div>
      <div class="bar" style="width:80px;background:{T['sky']};"></div>
      <div style="font-size:22px;color:{T['gray']};margin-top:28px;max-width:700px;line-height:1.6;">
        What the context explosion means for how AI<br>finds, navigates and ranks your content</div>
      <div style="font-size:17px;color:{T['gray']};opacity:0.6;margin-top:40px;">
        Andrea Volpini · WordLift</div>
    </div>""", ca)

def slide_02():
    """Why Context Has a Weight Problem"""
    ca = svg_grid(G30, 50, 10, T['sky'], 0.06, 0, 500)
    panels = [
        ("KV Cache", "Memory grows\nquadratically", T['sky']),
        ("Vector DBs", "Index bloat at\nbillion scale", T['sky']),
        ("On-Device", "Models can't fit\nin your pocket", T['sky']),
        ("AI Search\nAgents", "Lose context mid-\nreasoning. Silently.", T['berry']),
    ]
    cards = ""
    for title, desc, color in panels:
        cards += f'''<div style="flex:1;padding:32px;border-top:4px solid {color};background:rgba(255,255,255,0.03);">
          <div style="font-size:22px;font-weight:900;margin-bottom:12px;white-space:pre-line;">{title}</div>
          <div style="font-size:16px;color:{T['gray']};white-space:pre-line;">{desc}</div></div>'''
    return dark(f"""
    <div class="section">Act I — The Context Explosion</div>
    <div class="headline" style="font-size:64px;margin-bottom:48px;">
      Why Context Has<br>a Weight Problem</div>
    <div style="display:flex;gap:20px;margin-top:auto;margin-bottom:80px;">
      {cards}
    </div>""", ca)

def slide_03():
    """Search Used to Be a Query. Now It's a Journey."""
    ca = svg_grid(G30, 90, 14, T['sky'], 0.35, 520, -50)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section">Act I — The Context Explosion</div>
      <div class="headline" style="font-size:88px;max-width:800px;">
        Search Used<br>to Be a<br>Query.</div>
      <div class="headline" style="font-size:88px;color:{T['sky']};margin-top:8px;">
        Now It's a<br>Journey.</div>
    </div>""", ca)

def slide_04():
    """Three Shifts"""
    ca = svg_grid(G30, 40, 8, T['sky'], 0.04, 1200, 600)
    shifts = [
        ("01", "Retrieval → Navigation", "Content competes on reachability, not relevance"),
        ("02", "Documents → Entities", "The unit of search is now an entity, not a page"),
        ("03", "One Model → A System", "Compression · Navigation · Structure working together"),
    ]
    items = ""
    for num, title, desc in shifts:
        items += f'''<div style="display:flex;gap:28px;margin-bottom:44px;align-items:flex-start;">
          <div style="font-size:56px;font-weight:900;color:{T['sky']};line-height:1;min-width:80px;">{num}</div>
          <div>
            <div style="font-size:28px;font-weight:900;margin-bottom:8px;">{title}</div>
            <div style="font-size:18px;color:{T['gray']};">{desc}</div>
          </div></div>'''
    return dark(f"""
    <div class="section">Act I — The Context Explosion</div>
    <div class="headline" style="font-size:56px;margin-bottom:56px;">
      Three Shifts That Changed<br>What 'Findable' Means</div>
    {items}""", ca)

def slide_05():
    """Act II Chapter — The Compression Paradox"""
    ca = svg_grid(G90, 65, 10, T['sky'], 0.06, T['W']//2 - 60*10, 200)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section" style="margin-bottom:40px;">Act II</div>
      <div class="headline" style="font-size:120px;max-width:1100px;">
        The<br>Compression<br>Paradox</div>
      <div class="bar" style="width:80px;background:{T['sky']};"></div>
      <div style="font-size:20px;color:{T['gray']};margin-top:28px;">
        High compression · Zero overhead · Geometric accuracy<br>
        <span style="color:{T['berry']};">Get it wrong and your similarity scores are silently biased.</span></div>
    </div>""", ca)

def slide_06():
    """TurboQuant — LIGHT emphasis"""
    ca = svg_grid(G90s, 40, 8, T['sky'], 0.06, 60, 680)
    return light(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div style="font-size:56px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      TurboQuant</div>
    <div style="font-size:20px;color:{T['gray']};margin-top:8px;">
      Geometric compression without information loss</div>
    <div style="display:flex;gap:60px;margin-top:64px;align-items:flex-end;">
      <div>
        <div style="font-size:130px;font-weight:900;line-height:0.9;color:{T['sky']};letter-spacing:-6px;">4.5×</div>
        <div style="font-size:20px;color:{T['gray']};margin-top:8px;">smaller KV cache</div>
      </div>
      <div>
        <div style="font-size:130px;font-weight:900;line-height:0.9;color:{T['sky']};letter-spacing:-6px;">8×</div>
        <div style="font-size:20px;color:{T['gray']};margin-top:8px;">faster attention</div>
      </div>
      <div>
        <div style="font-size:130px;font-weight:900;line-height:0.9;color:{T['dark2']};letter-spacing:-6px;">0</div>
        <div style="font-size:20px;color:{T['gray']};margin-top:8px;">retrieval degradation</div>
      </div>
    </div>
    <div class="bar" style="width:60px;background:{T['berry']};margin-top:48px;"></div>
    <div style="font-size:17px;color:{T['gray']};margin-top:20px;">
      Two-stage pipeline: PolarQuant → QJL · Data-oblivious · GPU-native · Zero codebook</div>
    """, ca)

def slide_07():
    """Silent Ranking Destruction"""
    ca = svg_grid(G90, 30, 8, T['berry'], 0.05, 1200, 100)
    return dark(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div class="headline" style="font-size:56px;max-width:1200px;">
      Why 'Compressing Your<br>Embeddings' Can Silently<br>Destroy Your Rankings</div>
    <div style="display:flex;gap:60px;margin-top:64px;">
      <div style="flex:1;padding:28px;border-left:4px solid {T['berry']};">
        <div style="font-size:18px;font-weight:900;color:{T['berry']};margin-bottom:8px;">The Math</div>
        <div style="font-size:56px;font-weight:900;margin-bottom:8px;">2/π</div>
        <div style="font-size:16px;color:{T['gray']};">bias at 1-bit quantization</div>
      </div>
      <div style="flex:1;padding:28px;border-left:4px solid {T['sand']};">
        <div style="font-size:18px;font-weight:900;color:{T['sand']};margin-bottom:8px;">The System</div>
        <div style="font-size:28px;font-weight:900;margin-bottom:8px;">Broken Compass</div>
        <div style="font-size:16px;color:{T['gray']};">Cosine similarity stops reflecting true similarity</div>
      </div>
      <div style="flex:1;padding:28px;border-left:4px solid {T['gray']};">
        <div style="font-size:18px;font-weight:900;color:{T['gray']};margin-bottom:8px;">The Consequence</div>
        <div style="font-size:28px;font-weight:900;margin-bottom:8px;">Invisible Degradation</div>
        <div style="font-size:16px;color:{T['gray']};">Rankings shift. No error. No alert. Just worse answers.</div>
      </div>
    </div>""", ca)

def slide_08():
    """Zero-Bias Realignment"""
    ca = svg_grid(G90, 50, 10, T['sky'], 0.05, 1100, 0)
    return dark(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div class="headline" style="font-size:64px;max-width:1000px;">
      The 1-Bit<br>Zero-Bias<br>Realignment</div>
    <div style="margin-top:48px;padding:36px;border:2px solid rgba(255,255,255,0.1);
                background:rgba(52,82,219,0.05);max-width:900px;">
      <div style="font-size:22px;line-height:1.7;">
        <span style="color:{T['sky']};font-weight:700;">QJL correction →</span>
        Inner product estimates are now provably unbiased.</div>
      <div style="font-size:22px;line-height:1.7;margin-top:12px;">
        Your compressed vector index scores similarity<br>
        with <span style="font-weight:900;">mathematical correctness.</span></div>
    </div>
    <div class="bar" style="width:60px;background:{T['leaf']};margin-top:56px;"></div>
    <div style="font-size:17px;color:{T['gray']};margin-top:16px;">
      3,957 seconds → 0.002 seconds indexing time at billion scale</div>
    """, ca)

def slide_09():
    """Quantization Landscape — LIGHT"""
    ca = svg_grid(G90s, 30, 6, T['sky'], 0.05, 1400, 500)
    return light(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div style="font-size:48px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      The Quantization Landscape</div>
    <div style="margin-top:40px;">
      <table style="width:100%;border-collapse:collapse;font-size:16px;">
        <tr style="border-bottom:2px solid {T['dark2']};">
          <th style="text-align:left;padding:14px 16px;font-weight:700;">Algorithm</th>
          <th style="text-align:center;padding:14px 16px;font-weight:700;">Unbiased</th>
          <th style="text-align:center;padding:14px 16px;font-weight:700;">Codebook-Free</th>
          <th style="text-align:center;padding:14px 16px;font-weight:700;">GPU-Native</th>
          <th style="text-align:center;padding:14px 16px;font-weight:700;">Data-Oblivious</th>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:14px 16px;color:{T['gray']};">PQ / OPQ</td>
          <td style="text-align:center;padding:14px;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:14px 16px;color:{T['gray']};">ScaNN</td>
          <td style="text-align:center;padding:14px;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">partial</td><td style="text-align:center;">✗</td>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:14px 16px;color:{T['gray']};">RaBitQ</td>
          <td style="text-align:center;padding:14px;">✗</td><td style="text-align:center;">✓</td>
          <td style="text-align:center;">✓</td><td style="text-align:center;">✗</td>
        </tr>
        <tr style="background:{T['sky']}10;border-bottom:2px solid {T['sky']};">
          <td style="padding:14px 16px;font-weight:900;color:{T['sky']};">TurboQuant</td>
          <td style="text-align:center;padding:14px;color:{T['sky']};font-weight:900;">✓</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td>
          <td style="text-align:center;color:{T['sky']};font-weight:900;">✓</td>
        </tr>
      </table>
    </div>
    <div class="bar" style="width:50px;background:{T['sky']};margin-top:40px;"></div>
    <div style="font-size:16px;color:{T['gray']};margin-top:16px;">
      First algorithm with all four properties simultaneously</div>
    """, ca)

def slide_10():
    """Navigator Intro"""
    ca = svg_grid(G110, 70, 14, T['sky'], 0.25, 0, 0)
    box = "padding:14px 28px;font-size:17px;font-weight:700;border:2px solid rgba(255,255,255,0.25);"
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section">Act III — The Navigator</div>
      <div class="headline" style="font-size:72px;max-width:900px;">
        It Doesn't Search.</div>
      <div class="headline" style="font-size:72px;color:{T['sky']};">
        It Explores.</div>
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

def slide_11():
    """71% Stat — LIGHT"""
    ca = svg_grid(G110s, 55, 12, T['sky'], 0.08, T['W']-100*12, 100)
    return light(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:32px;color:{T['gray']};margin-top:16px;">
      When the evidence is scattered</div>
    <div style="margin-top:48px;">
      <div style="font-size:280px;font-weight:900;line-height:0.82;letter-spacing:-14px;
                  color:{T['sky']};">71<span style="font-size:180px;">%</span></div>
      <div style="font-size:28px;font-weight:400;color:{T['dark2']};margin-top:12px;">
        LLM win rate on complex reasoning</div>
      <div class="bar" style="width:50px;background:{T['berry']};margin-top:32px;"></div>
      <div style="font-size:17px;color:{T['gray']};margin-top:16px;">
        +4.55pp F1 over heuristic · p &lt; 0.001 · n=519</div>
    </div>""", ca)

def slide_12():
    """Separation of Concerns"""
    ca = svg_grid(G110, 40, 8, T['sky'], 0.04, 0, 700)
    return dark(f"""
    <div class="section">Act III — The Navigator</div>
    <div class="headline" style="font-size:56px;margin-bottom:56px;">
      Separation of Concerns</div>
    <div style="display:flex;gap:40px;margin-top:auto;margin-bottom:100px;">
      <div style="flex:1;padding:40px;border-top:4px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:28px;font-weight:900;margin-bottom:12px;color:{T['sky']};">LLM Explores</div>
        <div style="font-size:18px;color:{T['gray']};line-height:1.6;">Navigation breadth<br>
          Graph traversal<br>Multi-hop reasoning</div>
      </div>
      <div style="display:flex;align-items:center;font-size:40px;color:{T['gray']};">×</div>
      <div style="flex:1;padding:40px;border-top:4px solid {T['leaf']};background:rgba(34,162,134,0.05);">
        <div style="font-size:28px;font-weight:900;margin-bottom:12px;color:{T['leaf']};">Vectors Rank</div>
        <div style="font-size:18px;color:{T['gray']};line-height:1.6;">Cosine similarity<br>
          Geometric precision<br>Final ordering</div>
      </div>
    </div>
    <div style="font-size:20px;color:{T['gray']};margin-bottom:80px;">
      Let the LLM explore. Let the vectors decide.<br>
      <span style="color:{T['white']};font-weight:700;">Content must be structurally reachable.</span></div>
    """, ca)

def slide_13():
    """Model Capability Gap — LIGHT"""
    ca = svg_grid(G110s, 30, 6, T['sky'], 0.04, 100, 700)
    models = [
        ("Claude Haiku", "+4.37pp", T['sky'], "Strong gain"),
        ("Gemini Flash Lite", "+0.84pp", T['sand'], "Marginal gain"),
        ("Gemma 4", "−0.78pp", T['berry'], "Negative"),
    ]
    cards = ""
    for name, delta, color, note in models:
        cards += f'''<div style="flex:1;padding:32px;border-top:4px solid {color};background:{color}08;">
          <div style="font-size:20px;font-weight:900;color:{T['dark2']};margin-bottom:8px;">{name}</div>
          <div style="font-size:64px;font-weight:900;color:{color};line-height:1;letter-spacing:-3px;">{delta}</div>
          <div style="font-size:15px;color:{T['gray']};margin-top:8px;">{note}</div></div>'''
    return light(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:48px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      The Model Capability Gap</div>
    <div style="font-size:20px;color:{T['gray']};margin-top:8px;">
      The gap is behavioral, not architectural</div>
    <div style="display:flex;gap:24px;margin-top:56px;">{cards}</div>
    <div class="bar" style="width:50px;background:{T['sky']};margin-top:48px;"></div>
    <div style="font-size:17px;color:{T['gray']};margin-top:16px;">
      Distillation implication: the right model with the right graph beats a bigger model without one</div>
    """, ca)

def slide_14():
    """SLM Edge"""
    ca = svg_grid(G90s, 40, 8, T['sky'], 0.05, 1400, 0)
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="headline" style="font-size:60px;max-width:1000px;margin-bottom:48px;">
      Your Next Agent<br>Doesn't Live in the Cloud</div>
    <div style="display:flex;gap:32px;margin-top:auto;margin-bottom:80px;">
      <div style="flex:1;padding:32px;border-left:4px solid {T['leaf']};">
        <div style="font-size:22px;font-weight:900;color:{T['leaf']};margin-bottom:8px;">Secure</div>
        <div style="font-size:16px;color:{T['gray']};">Data never leaves the device</div>
      </div>
      <div style="flex:1;padding:32px;border-left:4px solid {T['sky']};">
        <div style="font-size:22px;font-weight:900;color:{T['sky']};margin-bottom:8px;">Fast</div>
        <div style="font-size:16px;color:{T['gray']};">Sub-second, no round-trip</div>
      </div>
      <div style="flex:1;padding:32px;border-left:4px solid {T['sand']};">
        <div style="font-size:22px;font-weight:900;color:{T['sand']};margin-bottom:8px;">Yours</div>
        <div style="font-size:16px;color:{T['gray']};">Trained on your graph</div>
      </div>
    </div>
    <div style="font-size:16px;color:{T['gray']};opacity:0.5;margin-bottom:80px;">
      Phone/Edge + SLM + GraphQL → Local Knowledge Graph</div>
    """, ca)

def slide_15():
    """Connected Data = Training Advantage"""
    ca = svg_grid(G90, 35, 8, T['sky'], 0.04, 200, 650)
    steps = [
        ("01", "Connectivity enables distillation", "Connected data teaches your model to navigate"),
        ("02", "Connected data multiplies", "Cross-property links compound the advantage"),
        ("03", "Disconnected data = dead end", "Without structure, training has no signal"),
    ]
    items = ""
    for num, title, desc in steps:
        items += f'''<div style="display:flex;gap:24px;margin-bottom:40px;align-items:flex-start;">
          <div style="font-size:48px;font-weight:900;color:{T['sky']};line-height:1;min-width:70px;">{num}</div>
          <div>
            <div style="font-size:26px;font-weight:900;margin-bottom:6px;">{title}</div>
            <div style="font-size:17px;color:{T['gray']};">{desc}</div>
          </div></div>'''
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="headline" style="font-size:56px;margin-bottom:56px;">
      Well-Connected Data Is<br>the Training Advantage</div>
    {items}
    <div class="bar" style="width:60px;background:{T['berry']};"></div>
    <div style="font-size:18px;color:{T['gray']};margin-top:16px;">
      Data connectivity is your AI training pipeline.</div>
    """, ca)

def slide_16():
    """Floor Is Set"""
    ca = svg_grid(G90s, 30, 8, T['leaf'], 0.05, 1300, 400)
    checks = [
        ("Compression", "✓", T['leaf'], "TurboQuant"),
        ("Navigation", "✓*", T['sky'], "Conditional (model-dependent)"),
        ("On-Device", "→", T['sand'], "18 months"),
        ("Data Connectivity", "?", T['berry'], "The variable you control today"),
    ]
    items = ""
    for label, status, color, note in checks:
        items += f'''<div style="display:flex;align-items:center;gap:20px;margin-bottom:24px;">
          <div style="width:52px;height:52px;border-radius:50%;border:3px solid {color};
                      display:flex;align-items:center;justify-content:center;
                      font-size:22px;font-weight:900;color:{color};">{status}</div>
          <div>
            <div style="font-size:22px;font-weight:900;">{label}</div>
            <div style="font-size:15px;color:{T['gray']};">{note}</div>
          </div></div>'''
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="headline" style="font-size:56px;margin-bottom:56px;">
      The Floor Is Set —<br>What's Left to Solve</div>
    {items}""", ca)

def slide_17():
    """Four Pillars — The Moat"""
    ca_sky = svg_grid(G90, 65, 12, T['sky'], 0.15, T['W']//2 - 60*12, 40)
    ca_leaf = svg_grid(G110s, 35, 10, T['leaf'], 0.08, T['W']-50*10, T['H']-35*10)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="headline" style="font-size:64px;max-width:1000px;">
        The Moat Is Not<br>the Model.</div>
      <div class="headline" style="font-size:64px;color:{T['sky']};margin-top:8px;">
        The Moat Is<br>the Graph.</div>
    </div>
    <div style="display:flex;gap:16px;margin-bottom:80px;">
      <div style="flex:1;padding:24px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:15px;font-weight:900;">Limitless Context</div>
        <div style="font-size:12px;color:{T['gray']};margin-top:4px;">TurboQuant compression</div>
      </div>
      <div style="flex:1;padding:24px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:15px;font-weight:900;">Billion-Scale Search</div>
        <div style="font-size:12px;color:{T['gray']};margin-top:4px;">Zero-bias vector indexing</div>
      </div>
      <div style="flex:1;padding:24px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:15px;font-weight:900;">On-Device Intelligence</div>
        <div style="font-size:12px;color:{T['gray']};margin-top:4px;">SLM navigator distillation</div>
      </div>
      <div style="flex:1;padding:24px;border-top:3px solid {T['sky']};background:{T['sky']};">
        <div style="font-size:15px;font-weight:900;">Navigable Knowledge Graph</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:4px;">The organizational layer</div>
      </div>
    </div>""", ca_sky + ca_leaf)

def slide_18():
    """Well-Connected — LIGHT"""
    ca = svg_grid(G90, 55, 10, T['sky'], 0.08, T['W']//2 - 55*10, 80)
    return light(f"""
    <div class="section">Act V — Structure Is the Moat</div>
    <div style="font-size:48px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      What 'Well-Connected'<br>Actually Means</div>
    <div style="display:flex;gap:24px;margin-top:48px;">
      <div style="flex:1;">
        <div style="font-size:14px;font-weight:700;color:{T['sky']};letter-spacing:3px;
                    text-transform:uppercase;margin-bottom:16px;">Internal</div>
        <div style="padding:20px;border:2px solid #e0e0e0;margin-bottom:12px;">
          <div style="font-size:16px;font-weight:700;color:{T['dark2']};">Products → Editorial</div>
          <div style="font-size:14px;color:{T['gray']};">Feature pages linked to how-to content</div>
        </div>
        <div style="padding:20px;border:2px solid #e0e0e0;">
          <div style="font-size:16px;font-weight:700;color:{T['dark2']};">Docs → Support → Product</div>
          <div style="font-size:14px;color:{T['gray']};">Every knowledge base article ↔ product feature</div>
        </div>
      </div>
      <div style="flex:1;">
        <div style="font-size:14px;font-weight:700;color:{T['sky']};letter-spacing:3px;
                    text-transform:uppercase;margin-bottom:16px;">External</div>
        <div style="padding:20px;border:2px solid #e0e0e0;margin-bottom:12px;">
          <div style="font-size:16px;font-weight:700;color:{T['dark2']};">Wikidata / Schema.org</div>
          <div style="font-size:14px;color:{T['gray']};">Your entities linked to the open knowledge graph</div>
        </div>
        <div style="padding:20px;border:2px solid #e0e0e0;">
          <div style="font-size:16px;font-weight:700;color:{T['dark2']};">Partner Ecosystems</div>
          <div style="font-size:14px;color:{T['gray']};">Cross-organizational entity alignment</div>
        </div>
      </div>
    </div>
    <div class="bar" style="width:80px;background:{T['sky']};margin-top:48px;"></div>
    <div style="font-size:18px;color:{T['gray']};margin-top:16px;font-style:italic;">
      Can an agent that starts from something adjacent find its way to you?</div>
    """, ca)

def slide_19():
    """Closing Thesis"""
    ca_sky = svg_grid(G90, 65, 12, T['sky'], 0.30, T['W']//2 - 60*12, 50)
    ca_berry = svg_grid(G30, 30, 6, T['berry'], 0.04, 0, 0)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;max-width:1100px;">
      <div class="headline" style="font-size:52px;">
        Context windows will keep growing.<br>
        Models will keep getting cheaper.</div>
      <div style="margin-top:32px;">
        <div class="headline" style="font-size:52px;color:{T['sky']};">
          The variable that compounds<br>is your data connectivity.</div>
      </div>
      <div class="bar" style="width:80px;background:{T['sky']};margin-top:48px;"></div>
      <div style="font-size:24px;margin-top:28px;font-weight:700;">
        Structure your knowledge now.</div>
    </div>
    <div style="margin-top:auto;margin-bottom:80px;display:flex;gap:40px;">
      <div style="font-size:15px;color:{T['gray']};">
        <span style="font-weight:700;color:{T['sky']};">Paper</span> · github.com/wordlift/rlm-on-kg</div>
      <div style="font-size:15px;color:{T['gray']};">
        <span style="font-weight:700;color:{T['sky']};">Code</span> · github.com/cyberandy/infinite-context</div>
      <div style="font-size:15px;color:{T['gray']};">
        Andrea Volpini · WordLift · SEO Week 2026</div>
    </div>""", ca_sky + ca_berry)


# ═══════════════════════════════════════
ALL_SLIDES = [
    ("01_title.png", slide_01),
    ("02_weight_problem.png", slide_02),
    ("03_query_to_journey.png", slide_03),
    ("04_three_shifts.png", slide_04),
    ("05_compression_paradox.png", slide_05),
    ("06_turboquant.png", slide_06),
    ("07_silent_ranking.png", slide_07),
    ("08_zero_bias.png", slide_08),
    ("09_quant_landscape.png", slide_09),
    ("10_navigator.png", slide_10),
    ("11_stat_71pct.png", slide_11),
    ("12_separation.png", slide_12),
    ("13_model_gap.png", slide_13),
    ("14_slm_edge.png", slide_14),
    ("15_connected_data.png", slide_15),
    ("16_floor_set.png", slide_16),
    ("17_moat_graph.png", slide_17),
    ("18_well_connected.png", slide_18),
    ("19_closing.png", slide_19),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ALL_SLIDES)} slides in Style V3 (dark/light rhythm)...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": T["W"], "height": T["H"]},
            device_scale_factor=1,
        )
        for fname, gen in ALL_SLIDES:
            print(f"  {fname}...", end=" ", flush=True)
            await page.set_content(gen(), wait_until="domcontentloaded")
            path = OUT / fname
            await page.screenshot(path=str(path), type="png")
            print(f"✓ ({path.stat().st_size//1024} KB)")
        await browser.close()

    total = sum(f.stat().st_size for f in OUT.glob("*.png")) // 1024
    print(f"\n✓ All 19 slides saved to {OUT}/ ({total} KB total)")


if __name__ == "__main__":
    asyncio.run(main())

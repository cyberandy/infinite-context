#!/usr/bin/env python3
"""
SEO Week 2026 — "Structure Is the Moat" — Editorial Plan v2
30 slides: 2 fixes, 11 new slides, renumbered throughout.

Dark/Light rhythm:
  DARK: 01,02,03,04,05,07,08,10,11,12,14,17,18,19,20,21,22,27,28,30
  LIGHT: 06,09,13,15,23,24,25,26,29

CA mapping by act:
  Act I  (01-04): Rule 30 — chaos from simplicity
  Act II (05-10): Rule 90 — fractal compression symmetry
  Act III(11-17): Rule 110 — Turing completeness, live computation
  Act IV (18-20): Rule 90 small — distilled, portable
  Act V  (21-30): Rule 110/90 — resolution, connected structure
"""

import asyncio
import math
from pathlib import Path

OUT = Path("slides_v2")

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

G30 = gen_grid(30, 100, 140, "center")
G90 = gen_grid(90, 80, 120, "center")
G110 = gen_grid(110, 90, 150, "right")
G90s = gen_grid(90, 50, 80, "center")
G110s = gen_grid(110, 60, 100, "right")

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
</style></head><body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""

def dark(body, ca=""): return html_slide(body, T['dark'], T['white'], ca)
def light(body, ca=""): return html_slide(body, T['white'], T['dark2'], ca)


# ═══════════════════════════════════════════════════════════════
# ACT I — The Context Explosion (Slides 1–4)
# ═══════════════════════════════════════════════════════════════

def slide_01():
    """KEEP — Title: Structure Is the Moat"""
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
    """KEEP — Why Context Has a Weight Problem"""
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
    """FIX — Search Used to Be a Query. Now It's a Journey. — FULL TWO-COLUMN"""
    ca = svg_grid(G30, 60, 10, T['sky'], 0.08, 1200, 0)
    return dark(f"""
    <div class="section">Act I — The Context Explosion</div>
    <div class="headline" style="font-size:56px;margin-bottom:48px;">
      Search Used to Be a Query.<br>
      <span style="color:{T['sky']};">Now It's a Journey.</span></div>
    <div style="display:flex;gap:40px;margin-bottom:20px;">
      <div style="flex:1;padding:32px;border-top:3px solid {T['gray']};background:rgba(255,255,255,0.03);">
        <div style="font-size:16px;font-weight:700;color:{T['gray']};letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;">The Old Model</div>
        <div style="font-size:17px;color:{T['gray']};line-height:1.8;">
          User types query → system scores documents<br>
          Stateless, symmetric, one-shot<br>
          Competed on: keyword match + link authority<br>
          <span style="font-weight:700;color:{T['white']};">The document was the unit</span></div>
      </div>
      <div style="flex:1;padding:32px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;">The Agent Model</div>
        <div style="font-size:17px;color:{T['gray']};line-height:1.8;">
          Agent interprets intent → seeds entities → traverses graph<br>
          Stateful, asymmetric, multi-hop<br>
          Competes on: <span style="color:{T['sky']};font-weight:700;">reachability</span><br>
          <span style="font-weight:700;color:{T['white']};">The entity is the unit</span></div>
      </div>
    </div>
    <div style="padding:20px 28px;border-left:4px solid {T['berry']};background:rgba(213,84,113,0.05);margin-top:auto;margin-bottom:60px;">
      <div style="font-size:16px;color:{T['gray']};line-height:1.7;font-style:italic;">
        "Agents increasingly do not retrieve your content directly. They arrive at it through entity traversal
        from adjacent content. If your entities aren't connected, you're invisible to the traversal — even if
        your content is semantically relevant."</div>
    </div>""", ca)

def slide_04():
    """KEEP — Three Shifts"""
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


# ═══════════════════════════════════════════════════════════════
# ACT II — The Compression Solution (Slides 5–10)
# ═══════════════════════════════════════════════════════════════

def slide_05():
    """KEEP — Compression Paradox chapter card"""
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
    """KEEP — TurboQuant — LIGHT"""
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
    """KEEP — Silent Ranking Destruction"""
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
    """KEEP — Zero-Bias Realignment"""
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
    """KEEP — Quantization Landscape — LIGHT"""
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
          <td style="text-align:center;padding:14px;">✗</td><td style="text-align:center;">✗</td>
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
    """NEW — TurboQuant Demo"""
    ca = svg_grid(G90, 45, 10, T['sky'], 0.10, T['W']//2 - 45*10, 200)
    return dark(f"""
    <div class="section">Act II — The Compression Solution</div>
    <div style="margin-top:auto;margin-bottom:auto;display:flex;align-items:center;gap:80px;">
      <div style="flex:1;">
        <div style="font-size:16px;font-weight:700;color:{T['sky']};letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">Try It</div>
        <div class="headline" style="font-size:64px;max-width:700px;">
          Watch It<br>Compress<br>Your Content</div>
        <div style="font-size:18px;color:{T['gray']};margin-top:32px;line-height:1.7;max-width:600px;">
          Paste any text. See TurboQuant quantize your embeddings in real time.
          Inner products preserved. No degradation. No codebook.</div>
        <div class="bar" style="width:60px;background:{T['sky']};margin-top:36px;"></div>
      </div>
      <div style="flex:0 0 320px;display:flex;flex-direction:column;align-items:center;">
        <div style="width:280px;height:280px;border:3px solid {T['sky']};border-radius:12px;
                    display:flex;align-items:center;justify-content:center;
                    background:rgba(52,82,219,0.08);">
          <div style="text-align:center;">
            <div style="font-size:60px;font-weight:900;color:{T['sky']};">QR</div>
            <div style="font-size:14px;color:{T['gray']};margin-top:8px;">Scan to try live</div>
          </div>
        </div>
        <div style="margin-top:20px;font-size:18px;font-weight:700;font-family:monospace;color:{T['sky']};">
          wor.ai/turbo-quant</div>
      </div>
    </div>""", ca)


# ═══════════════════════════════════════════════════════════════
# ACT III — The Navigator (Slides 11–17)
# ═══════════════════════════════════════════════════════════════

def slide_11():
    """KEEP (was 10) — Navigator Intro"""
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

def slide_12():
    """NEW — RLM-on-KG Demo + Paper Announcement"""
    ca = svg_grid(G110, 60, 12, T['sky'], 0.15, T['W'] - 70*12, 0)
    return dark(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="display:flex;gap:60px;margin-top:auto;margin-bottom:auto;">
      <div style="flex:0 0 40%;">
        <div style="font-size:14px;color:{T['berry']};font-weight:700;letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;">Publishing Today · arXiv 2025</div>
        <div class="headline" style="font-size:72px;">RLM-<br>on-KG</div>
        <div style="font-size:28px;font-weight:700;color:{T['sky']};margin-top:16px;">Live Navigation</div>
        <div style="margin-top:32px;width:200px;height:200px;border:3px solid {T['sky']};border-radius:12px;
                    display:flex;align-items:center;justify-content:center;
                    background:rgba(52,82,219,0.08);">
          <div style="text-align:center;">
            <div style="font-size:48px;font-weight:900;color:{T['sky']};">QR</div>
            <div style="font-size:12px;color:{T['gray']};margin-top:4px;">Scan to explore</div>
          </div>
        </div>
        <div style="margin-top:16px;font-size:16px;font-weight:700;font-family:monospace;color:{T['sky']};">
          wor.ai/rlm-on-kg-explorer</div>
        <div style="font-size:15px;color:{T['gray']};margin-top:8px;font-style:italic;">Watch It Think</div>
      </div>
      <div style="flex:1;display:flex;align-items:center;justify-content:center;">
        <div style="width:100%;height:400px;border:2px solid rgba(255,255,255,0.1);border-radius:8px;
                    background:rgba(52,82,219,0.03);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;">
          <svg width="500" height="300" xmlns="http://www.w3.org/2000/svg">
            <circle cx="250" cy="80" r="24" fill="{T['sky']}" opacity="0.9"/>
            <text x="250" y="84" text-anchor="middle" fill="white" font-size="11" font-weight="700" font-family="Helvetica Neue,sans-serif">Entity</text>
            <circle cx="120" cy="180" r="20" fill="{T['leaf']}" opacity="0.8"/>
            <text x="120" y="184" text-anchor="middle" fill="white" font-size="10" font-weight="700" font-family="Helvetica Neue,sans-serif">Action</text>
            <circle cx="380" cy="180" r="20" fill="{T['sand']}" opacity="0.8"/>
            <text x="380" y="184" text-anchor="middle" fill="white" font-size="10" font-weight="700" font-family="Helvetica Neue,sans-serif">Data</text>
            <circle cx="180" cy="260" r="18" fill="{T['berry']}" opacity="0.8"/>
            <text x="180" y="264" text-anchor="middle" fill="white" font-size="10" font-weight="700" font-family="Helvetica Neue,sans-serif">Result</text>
            <circle cx="320" cy="260" r="18" fill="{T['sky']}" opacity="0.6"/>
            <text x="320" y="264" text-anchor="middle" fill="white" font-size="10" font-weight="700" font-family="Helvetica Neue,sans-serif">Entity</text>
            <line x1="250" y1="104" x2="120" y2="160" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="250" y1="104" x2="380" y2="160" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="120" y1="200" x2="180" y2="242" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="380" y1="200" x2="320" y2="242" stroke="{T['sky']}" stroke-width="2" opacity="0.4"/>
            <line x1="180" y1="260" x2="320" y2="260" stroke="{T['sky']}" stroke-width="2" opacity="0.3"/>
          </svg>
          <div style="font-size:13px;color:{T['gray']};margin-top:12px;">Graph traversal visualization · Click a node to focus</div>
        </div>
      </div>
    </div>
    <div style="display:flex;gap:32px;margin-bottom:60px;">
      <div style="font-size:14px;color:{T['gray']};">Open-source · RDF-native · Graph traversal, live, in your browser</div>
      <div style="font-size:14px;color:{T['gray']};margin-left:auto;">
        <span style="color:{T['sky']};font-weight:700;">github.com/wordlift/rlm-on-kg</span></div>
    </div>""", ca)

def slide_13():
    """FIX (was 11) — Conditional Advantage — 71% + scatter table — LIGHT"""
    ca = svg_grid(G110s, 40, 10, T['sky'], 0.06, T['W']-80*10, 50)
    return light(f"""
    <div class="section">Act III — The Navigator</div>
    <div style="font-size:28px;color:{T['gray']};margin-bottom:8px;">
      When the evidence is scattered</div>
    <div style="display:flex;gap:60px;align-items:flex-start;">
      <div style="flex:0 0 auto;">
        <div style="font-size:200px;font-weight:900;line-height:0.82;letter-spacing:-10px;
                    color:{T['sky']};">71<span style="font-size:130px;">%</span></div>
        <div style="font-size:22px;color:{T['dark2']};margin-top:8px;">
          LLM win rate on complex reasoning</div>
      </div>
      <div style="flex:1;margin-top:20px;">
        <table style="width:100%;border-collapse:collapse;font-size:15px;">
          <tr style="border-bottom:2px solid {T['dark2']};">
            <th style="text-align:left;padding:10px 12px;font-weight:700;">Evidence Distribution</th>
            <th style="text-align:center;padding:10px 12px;font-weight:700;">Win Rate</th>
            <th style="text-align:center;padding:10px 12px;font-weight:700;">F1 Gain</th>
          </tr>
          <tr style="border-bottom:1px solid #e0e0e0;">
            <td style="padding:10px 12px;color:{T['gray']};">Concentrated (1–5 chunks)</td>
            <td style="text-align:center;padding:10px;">62%</td>
            <td style="text-align:center;">+1.85pp</td>
          </tr>
          <tr style="border-bottom:1px solid #e0e0e0;">
            <td style="padding:10px 12px;color:{T['gray']};">Scattered (6–10 chunks)</td>
            <td style="text-align:center;padding:10px;">65%</td>
            <td style="text-align:center;">+3.21pp</td>
          </tr>
          <tr style="border-bottom:1px solid #e0e0e0;">
            <td style="padding:10px 12px;color:{T['gray']};">Highly scattered (11+)</td>
            <td style="text-align:center;padding:10px;">62%</td>
            <td style="text-align:center;">+2.42pp</td>
          </tr>
          <tr style="background:{T['sky']}10;border-bottom:2px solid {T['sky']};">
            <td style="padding:10px 12px;font-weight:900;color:{T['sky']};">Complex Reasoning 11+</td>
            <td style="text-align:center;padding:10px;font-weight:900;color:{T['sky']};">71%</td>
            <td style="text-align:center;font-weight:900;color:{T['sky']};">+4.55pp</td>
          </tr>
        </table>
      </div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['berry']};margin-top:auto;margin-bottom:24px;">
      <div style="font-size:15px;color:{T['gray']};line-height:1.6;">
        In your terms: when a query requires connecting facts across three product pages, two editorial pieces
        and a case study — that's the 11+ chunk scenario. That's where the graph wins decisively.</div>
    </div>
    <div style="font-size:13px;color:{T['gray']};opacity:0.7;">
      Delta confirmed on MuSiQue (Wikipedia multi-hop QA): +1.67pp Claude, +1.33pp Gemini. Not a fiction-corpus artefact.</div>
    """, ca)

def slide_14():
    """KEEP (was 12) — Separation of Concerns"""
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

def slide_15():
    """KEEP (was 13) — Model Capability Gap — LIGHT"""
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

def slide_17():
    """NEW — Distillation Bridge"""
    ca = svg_grid(G110, 50, 10, T['sky'], 0.08, T['W']-60*10, 0)
    steps = [
        ("01", "The gap is in decisions, not architecture",
         "Gemma 4 uses the same tools, the same graph, the same 9-tool interface. It achieves 83% behavioral tie rate with a rule-based heuristic. The difference isn't capability — it's the training to make adaptive decisions."),
        ("02", "Exploration traces are labeled training data",
         "Every question Claude solves on the graph produces a (state → action → reward) trajectory. 519 questions = 519 navigation trajectories with F1 as ground truth."),
        ("03", "Fine-tune, distill, deploy locally",
         "TRL on Gemma 4 E2B. Target: close the behavioral gap to Claude Haiku. Result: an on-device navigator that costs zero per query."),
    ]
    items = ""
    for num, title, desc in steps:
        items += f'''<div style="display:flex;gap:24px;margin-bottom:28px;align-items:flex-start;">
          <div style="font-size:40px;font-weight:900;color:{T['sky']};line-height:1;min-width:60px;">{num}</div>
          <div>
            <div style="font-size:22px;font-weight:900;margin-bottom:6px;">{title}</div>
            <div style="font-size:15px;color:{T['gray']};line-height:1.6;max-width:800px;">{desc}</div>
          </div></div>'''
    return dark(f"""
    <div class="section">Act III → IV — Bridge</div>
    <div class="headline" style="font-size:52px;margin-bottom:40px;">
      The Gap Is Behavioral.<br>
      <span style="color:{T['sky']};">That Means It's Trainable.</span></div>
    {items}
    <div style="display:flex;align-items:center;gap:16px;margin-top:auto;margin-bottom:60px;
                padding:20px;border:2px solid rgba(255,255,255,0.1);background:rgba(52,82,219,0.03);">
      <div style="padding:12px 20px;background:{T['sky']};font-size:14px;font-weight:700;">Claude traces</div>
      <div style="color:{T['gray']};font-size:18px;">→</div>
      <div style="padding:12px 20px;border:2px solid {T['sky']};font-size:14px;font-weight:700;">TRL fine-tuning</div>
      <div style="color:{T['gray']};font-size:18px;">→</div>
      <div style="padding:12px 20px;background:{T['leaf']};font-size:14px;font-weight:700;">Gemma on-device</div>
    </div>""", ca)


# ═══════════════════════════════════════════════════════════════
# ACT IV — The SLM Navigator (Slides 18–20)
# ═══════════════════════════════════════════════════════════════

def slide_18():
    """KEEP (was 14) — SLM Edge + GitHub ref"""
    ca = svg_grid(G90s, 40, 8, T['sky'], 0.05, 1400, 0)
    return dark(f"""
    <div class="section">Act IV — The SLM Navigator</div>
    <div class="headline" style="font-size:60px;max-width:1000px;margin-bottom:48px;">
      Your Next Agent<br>Doesn't Live in the Cloud</div>
    <div style="display:flex;gap:32px;margin-top:auto;margin-bottom:60px;">
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
    <div style="font-size:15px;color:{T['gray']};opacity:0.5;margin-bottom:60px;">
      Phone/Edge + SLM + GraphQL → Local Knowledge Graph</div>
    <div style="font-size:13px;color:{T['gray']};opacity:0.6;">
      github.com/wordlift/google-ai-edge/tree/main/wordlift-graphql — GraphQL interface for on-device KG navigation</div>
    """, ca)

def slide_19():
    """KEEP (was 15) — Connected Data"""
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

def slide_20():
    """KEEP (was 16) — Floor Is Set"""
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


# ═══════════════════════════════════════════════════════════════
# ACT V — Structure Is the Moat (Slides 21–30)
# ═══════════════════════════════════════════════════════════════

def slide_21():
    """KEEP (was 17) — Four Pillars — The Moat"""
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

def slide_22():
    """NEW — SEO Playbook Chapter Card"""
    ca = svg_grid(G110, 70, 12, T['sky'], 0.08, T['W']//2 - 50*12, 100)
    return dark(f"""
    <div style="margin-top:auto;margin-bottom:auto;">
      <div class="section" style="margin-bottom:40px;">Act V</div>
      <div class="headline" style="font-size:120px;max-width:1100px;">
        The SEO<br>Playbook</div>
      <div class="bar" style="width:80px;background:{T['sky']};"></div>
      <div style="font-size:22px;color:{T['gray']};margin-top:28px;">
        What to actually do about all of this</div>
    </div>""", ca)

def slide_23():
    """NEW — Visibility Shift — LIGHT"""
    ca = svg_grid(G110s, 35, 8, T['sky'], 0.05, T['W']-60*8, 200)
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="font-size:48px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      AI Visibility Is Shifting</div>
    <div style="font-size:20px;color:{T['gray']};margin-top:8px;">
      From mentions to reasoning utility</div>
    <div style="display:flex;gap:32px;margin-top:40px;">
      <div style="flex:1;padding:28px;border-top:3px solid {T['gray']};background:rgba(0,0,0,0.02);">
        <div style="font-size:14px;font-weight:700;color:{T['gray']};letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;text-decoration:line-through;">Mentions Era</div>
        <div style="font-size:15px;color:{T['gray']};line-height:1.8;">
          Your brand appears in training data<br>
          LLM "knows" you from pre-training<br>
          Passive: be present, be cited<br>
          Measured by: brand recall, mention frequency</div>
      </div>
      <div style="flex:1;padding:28px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.04);">
        <div style="font-size:14px;font-weight:700;color:{T['sky']};letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;">Reasoning Utility Era</div>
        <div style="font-size:15px;color:{T['dark2']};line-height:1.8;">
          Your entities are connected and traversable<br>
          LLM can <span style="font-weight:700;color:{T['sky']};">navigate</span> to your content at query time<br>
          Active: be reachable, be verifiable, be citable<br>
          Measured by: evidence retrieval rate, citation in agent outputs</div>
      </div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['sky']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:15px;color:{T['gray']};line-height:1.6;font-style:italic;">
        "GPT-5.4 doesn't just retrieve your content anymore. It decides whether your content is worth
        navigating to. That decision is made by following entity links — not by ranking pages."</div>
    </div>""", ca)

def slide_24():
    """NEW — Ghost Citations — LIGHT"""
    ca = svg_grid(G30, 40, 8, T['berry'], 0.05, 0, 600)
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="display:flex;gap:60px;align-items:flex-start;">
      <div style="flex:0 0 auto;">
        <div style="font-size:240px;font-weight:900;line-height:0.82;letter-spacing:-12px;
                    color:{T['berry']};">7<span style="font-size:160px;">%</span></div>
        <div style="font-size:24px;font-weight:700;color:{T['dark2']};margin-top:8px;">Ghost Citations</div>
      </div>
      <div style="flex:1;margin-top:20px;">
        <div style="font-size:17px;color:{T['gray']};line-height:1.7;margin-bottom:28px;">
          AI agents cite content that never appeared in the top-10 search results.
          The agent navigated there through entity links — not through the ranking signal
          you spent years optimizing.</div>
        <div style="display:flex;gap:20px;">
          <div style="flex:1;padding:20px;border-top:3px solid {T['berry']};background:rgba(213,84,113,0.04);">
            <div style="font-size:15px;font-weight:700;color:{T['dark2']};margin-bottom:6px;">Rankings ≠ AI citations</div>
            <div style="font-size:13px;color:{T['gray']};line-height:1.6;">
              Content you've ranked #1 for years may be invisible to traversal.</div>
          </div>
          <div style="flex:1;padding:20px;border-top:3px solid {T['sky']};background:rgba(52,82,219,0.04);">
            <div style="font-size:15px;font-weight:700;color:{T['dark2']};margin-bottom:6px;">Navigation graph = new signal</div>
            <div style="font-size:13px;color:{T['gray']};line-height:1.6;">
              Can an agent find me by traversing from a related entity?</div>
          </div>
        </div>
      </div>
    </div>""", ca)

def slide_25():
    """NEW — How AI Reads Your Content — LIGHT"""
    ca = svg_grid(G110s, 25, 6, T['sky'], 0.04, 1500, 600)
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="font-size:48px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      How AI Reads Your Content in 2026</div>
    <div style="margin-top:36px;">
      <table style="width:100%;border-collapse:collapse;font-size:15px;">
        <tr style="border-bottom:2px solid {T['dark2']};">
          <th style="text-align:left;padding:12px;font-weight:700;width:20%;"></th>
          <th style="text-align:center;padding:12px;font-weight:700;color:{T['gray']};">GPT-3 era</th>
          <th style="text-align:center;padding:12px;font-weight:700;color:{T['gray']};">GPT-4 era</th>
          <th style="text-align:center;padding:12px;font-weight:700;color:{T['sky']};">GPT-5.4 era</th>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:12px;font-weight:700;">Method</td>
          <td style="text-align:center;padding:12px;color:{T['gray']};">Pattern match</td>
          <td style="text-align:center;color:{T['gray']};">Semantic similarity</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Graph traversal</td>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:12px;font-weight:700;">Unit</td>
          <td style="text-align:center;padding:12px;color:{T['gray']};">Token</td>
          <td style="text-align:center;color:{T['gray']};">Embedding</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Entity</td>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:12px;font-weight:700;">What matters</td>
          <td style="text-align:center;padding:12px;color:{T['gray']};">Keyword density</td>
          <td style="text-align:center;color:{T['gray']};">Vector proximity</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Structural connectivity</td>
        </tr>
        <tr style="border-bottom:1px solid #e0e0e0;">
          <td style="padding:12px;font-weight:700;">Content's job</td>
          <td style="text-align:center;padding:12px;color:{T['gray']};">Be present</td>
          <td style="text-align:center;color:{T['gray']};">Be similar</td>
          <td style="text-align:center;font-weight:700;color:{T['sky']};">Be reachable</td>
        </tr>
        <tr style="border-bottom:2px solid {T['dark2']};">
          <td style="padding:12px;font-weight:700;">Failure mode</td>
          <td style="text-align:center;padding:12px;color:{T['gray']};">Not indexed</td>
          <td style="text-align:center;color:{T['gray']};">Low embedding similarity</td>
          <td style="text-align:center;font-weight:700;color:{T['berry']};">Disconnected from graph</td>
        </tr>
      </table>
    </div>
    <div class="bar" style="width:60px;background:{T['sky']};margin-top:40px;"></div>
    <div style="font-size:16px;color:{T['gray']};margin-top:16px;">
      Each generation didn't just improve — it changed what 'findable' means. You can't optimize for GPT-5.4 using GPT-4 intuitions.</div>
    """, ca)

def slide_26():
    """NEW — Consistency Not Crawling — LIGHT"""
    ca = svg_grid(G110s, 20, 6, T['sky'], 0.04, 100, 750)
    bars = [
        ("High volume,\ninconsistent naming", 35, T['gray'], "Low citation rate"),
        ("Moderate volume,\nconsistent naming", 60, T['sand'], "Moderate citation rate"),
        ("Moderate volume,\nconsistent + cross-links", 90, T['sky'], "High citation rate"),
    ]
    bar_html = ""
    for label, pct, color, note in bars:
        bar_html += f'''<div style="margin-bottom:24px;">
          <div style="font-size:14px;color:{T['gray']};margin-bottom:6px;white-space:pre-line;">{label}</div>
          <div style="height:36px;width:{pct}%;background:{color};border-radius:3px;
                      display:flex;align-items:center;padding-left:14px;">
            <span style="font-size:13px;font-weight:700;color:{T['white']};">{note}</span>
          </div></div>'''
    return light(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div style="font-size:48px;font-weight:900;letter-spacing:-3px;color:{T['dark2']};">
      Consistency, Not Crawling</div>
    <div style="font-size:18px;color:{T['gray']};margin-top:8px;max-width:900px;">
      The strongest predictor of AI citation is the consistency of entity representation across properties.</div>
    <div style="margin-top:48px;max-width:900px;">
      {bar_html}
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['sky']};margin-top:auto;margin-bottom:40px;">
      <div style="font-size:15px;color:{T['gray']};line-height:1.6;">
        Agents verify entities against what they already know. If your entity is named differently in your blog,
        your product pages and your Schema.org markup — the agent can't resolve them to the same node.
        You become three weak signals instead of one strong one.</div>
    </div>""", ca)

def slide_27():
    """NEW — Explore → Verify → Cite — DARK"""
    ca = svg_grid(G110, 55, 10, T['sky'], 0.10, T['W'] - 60*10, 0)
    return dark(f"""
    <div class="section">Act V — The SEO Playbook</div>
    <div class="headline" style="font-size:48px;margin-bottom:8px;">
      From <span style="text-decoration:line-through;color:{T['gray']};">Crawl-Index-Rank</span></div>
    <div class="headline" style="font-size:56px;color:{T['sky']};margin-bottom:48px;">
      Explore → Verify → Cite</div>
    <div style="display:flex;gap:28px;">
      <div style="flex:1;padding:28px;border-top:4px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:24px;font-weight:900;color:{T['sky']};margin-bottom:12px;">Explore</div>
        <div style="font-size:17px;font-weight:700;margin-bottom:8px;">Can the agent find you?</div>
        <div style="font-size:14px;color:{T['gray']};line-height:1.6;">
          Entity links, stable URIs,<br>navigable knowledge graph</div>
      </div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['leaf']};background:rgba(34,162,134,0.05);">
        <div style="font-size:24px;font-weight:900;color:{T['leaf']};margin-bottom:12px;">Verify</div>
        <div style="font-size:17px;font-weight:700;margin-bottom:8px;">Can the agent confirm you?</div>
        <div style="font-size:14px;color:{T['gray']};line-height:1.6;">
          Provenance anchors, chunk-level<br>attribution, consistent entity IDs</div>
      </div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['sand']};background:rgba(194,164,29,0.05);">
        <div style="font-size:24px;font-weight:900;color:{T['sand']};margin-bottom:12px;">Cite</div>
        <div style="font-size:17px;font-weight:700;margin-bottom:8px;">Can the agent cite you?</div>
        <div style="font-size:14px;color:{T['gray']};line-height:1.6;">
          Stable URLs, canonical entities,<br>machine-readable attribution</div>
      </div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['berry']};margin-top:auto;margin-bottom:60px;">
      <div style="font-size:16px;color:{T['gray']};line-height:1.6;">
        AI agents don't rank pages. They navigate structure. The pipeline has changed.
        The optimization targets have changed. Most content strategies haven't.</div>
    </div>""", ca)

def slide_28():
    """NEW — AutoResearch — DARK"""
    ca = svg_grid(G90, 40, 10, T['sky'], 0.06, T['W']//2 - 40*10, 300)
    return dark(f"""
    <div class="section">Act V — Structure Is the Moat</div>
    <div class="headline" style="font-size:52px;margin-bottom:16px;">
      What Happens When<br>You Build the Graph</div>
    <div style="font-size:20px;color:{T['sky']};font-weight:700;margin-bottom:40px;">
      AutoResearch — Autonomous knowledge work, powered by connected data</div>
    <div style="display:flex;gap:24px;">
      <div style="flex:1;padding:28px;border-top:4px solid {T['leaf']};background:rgba(34,162,134,0.05);">
        <div style="font-size:22px;font-weight:900;color:{T['leaf']};margin-bottom:12px;">Discover</div>
        <div style="font-size:14px;color:{T['gray']};line-height:1.6;">
          Agent traverses your KG to surface related content, gaps in coverage,
          unanswered questions. No manual curation.</div>
      </div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['sky']};background:rgba(52,82,219,0.05);">
        <div style="font-size:22px;font-weight:900;color:{T['sky']};margin-bottom:12px;">Synthesize</div>
        <div style="font-size:14px;color:{T['gray']};line-height:1.6;">
          Agent collects evidence across your properties, verifies against external KGs,
          produces grounded, citable summaries. No hallucination.</div>
      </div>
      <div style="flex:1;padding:28px;border-top:4px solid {T['sand']};background:rgba(194,164,29,0.05);">
        <div style="font-size:22px;font-weight:900;color:{T['sand']};margin-bottom:12px;">Act</div>
        <div style="font-size:14px;color:{T['gray']};line-height:1.6;">
          Agent identifies structural gaps — missing entity links, inconsistent identifiers,
          unclaimed Wikidata entries — and queues them for remediation.</div>
      </div>
    </div>
    <div style="padding:16px 24px;border-left:4px solid {T['berry']};margin-top:auto;margin-bottom:60px;">
      <div style="font-size:16px;color:{T['gray']};line-height:1.6;">
        This isn't a future capability. This is what well-connected data enables now.
        The graph is already there for organizations that built it.</div>
    </div>""", ca)

def slide_29():
    """KEEP (was 18) — Well-Connected — LIGHT + GitHub ref"""
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
    <div style="font-size:13px;color:{T['gray']};opacity:0.6;margin-top:12px;">
      github.com/wordlift/google-ai-edge/tree/main/wordlift-graphql</div>
    """, ca)

def slide_30():
    """KEEP (was 19) — Closing + extra ref"""
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
    <div style="margin-top:auto;margin-bottom:80px;display:flex;gap:32px;flex-wrap:wrap;">
      <div style="font-size:15px;color:{T['gray']};">
        <span style="font-weight:700;color:{T['sky']};">Paper</span> · github.com/wordlift/rlm-on-kg</div>
      <div style="font-size:15px;color:{T['gray']};">
        <span style="font-weight:700;color:{T['sky']};">Code</span> · github.com/cyberandy/infinite-context</div>
      <div style="font-size:15px;color:{T['gray']};">
        <span style="font-weight:700;color:{T['sky']};">GraphQL</span> · github.com/wordlift/google-ai-edge</div>
      <div style="font-size:15px;color:{T['gray']};">
        Andrea Volpini · WordLift · SEO Week 2026</div>
    </div>""", ca_sky + ca_berry)


# ═══════════════════════════════════════════════════════════════
ALL_SLIDES = [
    # Act I
    ("01_title.png", slide_01),
    ("02_weight_problem.png", slide_02),
    ("03_query_to_journey.png", slide_03),
    ("04_three_shifts.png", slide_04),
    # Act II
    ("05_compression_paradox.png", slide_05),
    ("06_turboquant.png", slide_06),
    ("07_silent_ranking.png", slide_07),
    ("08_zero_bias.png", slide_08),
    ("09_quant_landscape.png", slide_09),
    ("10_turbo_demo.png", slide_10),
    # Act III
    ("11_navigator.png", slide_11),
    ("12_rlm_demo.png", slide_12),
    ("13_conditional_advantage.png", slide_13),
    ("14_separation.png", slide_14),
    ("15_model_gap.png", slide_15),
    # slide 16 removed (renumbered)
    ("17_distillation.png", slide_17),
    # Act IV
    ("18_slm_edge.png", slide_18),
    ("19_connected_data.png", slide_19),
    ("20_floor_set.png", slide_20),
    # Act V
    ("21_moat_graph.png", slide_21),
    ("22_seo_playbook_chapter.png", slide_22),
    ("23_visibility_shift.png", slide_23),
    ("24_ghost_citations.png", slide_24),
    ("25_gpt_reads_differently.png", slide_25),
    ("26_consistency_not_crawling.png", slide_26),
    ("27_explore_verify_cite.png", slide_27),
    ("28_autoResearch.png", slide_28),
    ("29_well_connected.png", slide_29),
    ("30_closing.png", slide_30),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ALL_SLIDES)} slides — Editorial Plan v2...\n")

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
    print(f"\n✓ All {len(ALL_SLIDES)} slides saved to {OUT}/ ({total} KB total)")


if __name__ == "__main__":
    asyncio.run(main())

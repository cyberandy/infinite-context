#!/usr/bin/env python3
"""
"Structure Is the Moat" — Final Editorial Plan v2 BOLD.
32 slides based on the April 18th final keynote outline.
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
    for _ in range(rows - 1): grid.append(rule_row(grid[-1], rule))
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

def html_slide(body, bg, fg, ca_svg=""):
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{T['W']}px;height:{T['H']}px;background:{bg};
font-family:{T['font']};overflow:hidden;position:relative;color:{fg};}}
.ca{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}}
.c{{position:relative;z-index:1;width:100%;height:100%;padding:100px 120px;
display:flex;flex-direction:column;justify-content:center;}}
.section{{font-size:18px;font-weight:700;letter-spacing:6px;text-transform:uppercase;
color:{T['sky']};margin-bottom:32px;}}
.h{{font-weight:900;line-height:1.05;letter-spacing:-4px;}}
.bar{{height:6px;margin-top:40px;}}
.point{{font-size:32px;line-height:1.4;margin-bottom:24px;color:{T['gray']};}}
.point b{{color:{fg};}}
</style></head><body>
<div class="ca"><svg width="{T['W']}" height="{T['H']}" xmlns="http://www.w3.org/2000/svg">{ca_svg}</svg></div>
<div class="c">{body}</div>
</body></html>"""

def dark(body, ca=""): return html_slide(body, T['dark'], T['white'], ca)
def light(body, ca=""): return html_slide(body, T['white'], T['dark2'], ca)

# ═══════════════════════════════════════════════════════════
# ACT I — THE CONTEXT EXPLOSION
# ═══════════════════════════════════════════════════════════

def slide_01():
    ca = svg_grid(G30, 80, 20, T['sky'], 0.25, 600, 0)
    return dark(f"""
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
      <div class="section">SEO Week 2026</div>
      <div class="h" style="font-size:160px;max-width:1000px;">Structure<br>Is the<br>Moat</div>
      <div class="bar" style="width:120px;background:{T['sky']};"></div>
      <div style="font-size:36px;color:{T['gray']};margin-top:40px;max-width:1000px;line-height:1.4;">
        What the context explosion means for how AI<br>finds, navigates and ranks your content</div>
    </div>""", ca)

def slide_02():
    ca = svg_grid(G30, 40, 15, T['sky'], 0.08, 0, 500)
    return dark(f"""
    <div class="section">The Origin Story</div>
    <div class="h" style="font-size:90px;margin-bottom:48px;">9 Years Ago,<br>I Trained a Model with<br><span style="color:{T['sky']};">200 Tokens</span> of Context</div>
    <div style="max-width:900px;">
      <div class="point"><b>Context used to be tiny.</b> If it didn't fit, it didn't exist.</div>
      <div class="point"><b>The main bottleneck</b> was always capacity.</div>
    </div>""", ca)

def slide_03():
    ca = svg_grid(G90, 60, 14, T['sky'], 0.15, 800, 0)
    return dark(f"""
    <div class="section">The Numbers</div>
    <div class="h" style="font-size:100px;margin-bottom:60px;">The Context Explosion</div>
    <div style="display:flex;gap:40px;align-items:flex-end;height:400px;margin-bottom:40px;">
       <div style="flex:1;height:20px;background:{T['gray']};opacity:0.3;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:14px;">512 (2017)</div>
       <div style="flex:1;height:50px;background:{T['gray']};opacity:0.5;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:14px;">4K (2020)</div>
       <div style="flex:1;height:120px;background:{T['sand']};border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:14px;">128K (2023)</div>
       <div style="flex:1;height:240px;background:{T['sky']};border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:900;">1M+ (2024)</div>
       <div style="flex:1;height:380px;background:{T['sky']};border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;">∞ context (2026)</div>
    </div>
    <div class="point">Abundance did not remove the problem.<br><b>It moved it elsewhere.</b></div>""", ca)

def slide_04():
    ca = svg_grid(G30, 50, 12, T['berry'], 0.05, 1200, 0)
    return dark(f"""
    <div class="section">The Limit</div>
    <div class="h" style="font-size:90px;margin-bottom:64px;">Why More Context<br><span style="color:{T['berry']};">Is Not Enough</span></div>
    <div style="display:flex;gap:44px;">
      <div style="flex:1;padding:48px;background:rgba(255,255,255,0.03);border-top:6px solid {T['sky']};">
        <div style="font-size:28px;font-weight:900;margin-bottom:16px;">Quadratic Wall</div>
        <div style="font-size:20px;color:{T['gray']};">More context gets<br>expensive fast.</div></div>
      <div style="flex:1;padding:48px;background:rgba(255,255,255,0.03);border-top:6px solid {T['sand']};">
        <div style="font-size:28px;font-weight:900;margin-bottom:16px;">Context Rot</div>
        <div style="font-size:20px;color:{T['gray']};">More input can mean<br>less understanding.</div></div>
      <div style="flex:1;padding:48px;background:rgba(213,84,113,0.1);border-top:6px solid {T['berry']};">
        <div style="font-size:28px;font-weight:900;margin-bottom:16px;">Bigger Window</div>
        <div style="font-size:20px;color:{T['gray']};">Bottleneck shifts to<br>selection and navigation.</div></div>
    </div>""", ca)

def slide_05():
    ca = svg_grid(G110, 60, 20, T['sky'], 0.2, 0, 0)
    return dark(f"""
    <div class="h" style="font-size:120px;line-height:0.95;">Search was a <span style="color:{T['gray']};">query</span>.</div>
    <div class="h" style="font-size:120px;margin-top:20px;">Now it’s a <span style="color:{T['sky']};">journey</span>.</div>
    <div class="bar" style="width:100px;background:{T['sky']};margin-bottom:48px;"></div>
    <div style="font-size:36px;color:{T['gray']};line-height:1.5;max-width:1000px;">
      Answers are no longer found in a single page.<br>
      They emerge across chunks, entities, hops and tools.</div>""", ca)

def slide_06():
    ca = svg_grid(G30, 40, 12, T['sky'], 0.1, 800, 600)
    return light(f"""
    <div class="section">Three Shifts</div>
    <div class="h" style="font-size:80px;margin-bottom:60px;">What “Findable” Means</div>
    <div style="display:flex;flex-direction:column;gap:32px;">
      <div style="display:flex;gap:40px;align-items:center;">
        <div style="width:300px;font-size:22px;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:{T['sky']};">Retrieval → Navigation</div>
        <div style="font-size:24px;color:{T['gray']};">Path selection, not just rank.</div></div>
      <div style="display:flex;gap:40px;align-items:center;">
        <div style="width:300px;font-size:22px;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:{T['sky']};">Docs → Entities</div>
        <div style="font-size:24px;color:{T['gray']};">Relations matter more than pages.</div></div>
      <div style="display:flex;gap:40px;align-items:center;">
        <div style="width:300px;font-size:22px;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:{T['sky']};">Model → System</div>
        <div style="font-size:24px;color:{T['gray']};">Retrieval, ranking and reasoning succeed together.</div></div>
    </div>""", ca)

def slide_07():
    return dark(f"""
    <div class="section">Responses to Infinite Context</div>
    <div style="display:flex;gap:60px;">
      <div style="flex:1;">
        <div style="font-size:20px;font-weight:700;color:{T['sky']};letter-spacing:3px;margin-bottom:20px;">ARCHITECTURAL</div>
        <div class="h" style="font-size:52px;margin-bottom:24px;">Bigger models.<br>More throughput.</div>
        <div style="font-size:20px;color:{T['gray']};">Brute force context management.</div>
      </div>
      <div style="flex:1;">
        <div style="font-size:20px;font-weight:700;color:{T['leaf']};letter-spacing:3px;margin-bottom:20px;">PHILOSOPHICAL</div>
        <div class="h" style="font-size:52px;margin-bottom:24px;">Smarter memory.<br>Selective retrieval.</div>
        <div style="font-size:20px;color:{T['gray']};">Navigable, structured knowledge.</div>
      </div>
    </div>
    <div class="bar" style="width:100px;background:{T['sky']};margin-top:60px;"></div>
    <div style="font-size:28px;color:{T['white']};font-weight:900;margin-top:24px;">
      Memory and structure must become first-class citizens.</div>""")

# ═══════════════════════════════════════════════════════════
# ACT II — PAPER 1: STRUCTURED DATA AS A MEMORY LAYER
# ═══════════════════════════════════════════════════════════

def slide_08():
    return light(f"""
    <div class="section">Act II — Paper 1</div>
    <div class="h" style="font-size:100px;">AI Needs a<br>Memory Layer,<br><span style="color:{T['sky']};">Not Just Markup</span></div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:32px;color:{T['gray']};margin-top:40px;max-width:900px;">
      Real gain appears when structure becomes accessible,<br>dereferenceable, and agent-readable.</div>""")

def slide_09():
    ca = svg_grid(G110, 40, 10, T['sky'], 0.05, 0, 0)
    return light(f"""
    <div class="section">The Three-Layer Experiment</div>
    <div style="display:flex;gap:32px;align-items:flex-end;height:450px;">
      <div style="flex:1;height:30%;background:{T['gray_light']};border:2px solid {T['gray']};display:flex;flex-direction:column;justify-content:center;align-items:center;padding:20px;text-align:center;">
        <div style="font-size:18px;font-weight:900;">Layer 1</div><div style="font-size:14px;">Plain HTML</div></div>
      <div style="flex:1;height:45%;background:{T['gray_light']};border:2px solid {T['sky']};display:flex;flex-direction:column;justify-content:center;align-items:center;padding:20px;text-align:center;">
        <div style="font-size:18px;font-weight:900;color:{T['sky']};">Layer 2</div><div style="font-size:14px;">HTML + JSON-LD</div></div>
      <div style="flex:1;height:100%;background:rgba(52,82,219,0.1);border:4px solid {T['sky']};display:flex;flex-direction:column;justify-content:center;align-items:center;padding:20px;text-align:center;">
        <div style="font-size:24px;font-weight:900;color:{T['sky']};">Layer 3</div><div style="font-size:18px;font-weight:700;">Enhanced Entity Pages</div><div style="font-size:14px;margin-top:8px;">Standard & Agentic RAG</div></div>
    </div>
    <div style="margin-top:40px;font-size:24px;color:{T['gray']};">
      Same content, different memory conditions.<br>
      <b>The variable is whether the system can traverse the structure.</b></div>""", ca)

def slide_10():
    return light(f"""
    <div class="section">Paper 1 Takeaway</div>
    <div class="h" style="font-size:80px;line-height:1.2;">Structure matters when it<br><span style="color:{T['sky']};">changes retrieval behavior,</span><br>not only when it validates markup.</div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>""")

# ═══════════════════════════════════════════════════════════
# ACT III — COMPRESSION: WHY EFFICIENT MEMORY MATTERS
# ═══════════════════════════════════════════════════════════

def slide_11():
    ca = svg_grid(G30, 40, 40, T['sky'], 0.1, 0, 0)
    return dark(f"""
    <div class="section">Act III — Compression</div>
    <div class="h" style="font-size:110px;">The<br>Compression<br>Paradox</div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:40px;max-width:800px;">
      Bigger context requires compression.<br>
      But poor compression silently breaks retrieval.<br>
      <span style="color:{T['berry']};">Scale without geometry is fragile.</span></div>""", ca)

def slide_12():
    return dark(f"""
    <div class="section">TurboQuant</div>
    <div class="h" style="font-size:100px;color:{T['sky']};">Compress the cache,<br>not the context.</div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:32px;color:{T['gray']};margin-top:40px;max-width:900px;">
      Reduces KV cache burden. Speeds attention.<br>
      Preserves retrieval quality via <b>geometric fidelity.</b></div>""")

def slide_13():
    return dark(f"""
    <div class="section">Silent Failure</div>
    <div class="h" style="font-size:84px;">Bad Embedding Compression<br><span style="color:{T['berry']};">Destroys Rankings</span></div>
    <div class="bar" style="width:100px;background:{T['berry']};"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:40px;max-width:900px;">
      The system still returns results. No crash. No warning.<br>
      But <b>similarity drifts</b> and rankings degrade silently.</div>""")

def slide_14():
    return dark(f"""
    <div class="section">The Solution</div>
    <div class="h" style="font-size:120px;">Zero-Bias<br>Correction</div>
    <div class="bar" style="width:100px;background:{T['leaf']};"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:40px;max-width:900px;">
      TurboQuant corrects the directional bias of quantization.<br>
      <b>Trustworthy similarity</b> even under aggressive compression.</div>""")

def slide_15():
    return light(f"""
    <div class="section">The Quantization Landscape</div>
    <div class="h" style="font-size:64px;margin-bottom:48px;">Why TurboQuant Wins</div>
    <div style="display:flex;gap:32px;">
      <div style="flex:1;padding:32px;background:{T['gray_light']};">
        <div style="font-size:18px;font-weight:900;color:{T['sky']};">UNBIASED</div>
        <div style="font-size:14px;margin-top:8px;">Geometric accuracy</div></div>
      <div style="flex:1;padding:32px;background:{T['gray_light']};">
        <div style="font-size:18px;font-weight:900;color:{T['sky']};">DEPLOYABLE</div>
        <div style="font-size:14px;margin-top:8px;">GPU-native performance</div></div>
      <div style="flex:1;padding:32px;background:{T['gray_light']};">
        <div style="font-size:18px;font-weight:900;color:{T['sky']};">OBLIVIOUS</div>
        <div style="font-size:14px;margin-top:8px;">No data-specific tuning</div></div>
    </div>
    <div style="font-size:28px;font-weight:900;margin-top:48px;">It’s about combining speed with reliability.</div>""")

def slide_16():
    return dark(f"""
    <div class="section">Why This Matters</div>
    <div class="h" style="font-size:72px;">Retrieval infrastructure shapes<br>what is surfaced, cited and trusted.</div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:32px;color:{T['gray']};margin-top:40px;">
      Memory efficiency is no longer just infrastructure.<br>
      <b>It defines visibility.</b></div>""")

# ═══════════════════════════════════════════════════════════
# ACT IV — PAPER 2: RLM-ON-KG
# ═══════════════════════════════════════════════════════════

def slide_17():
    ca = svg_grid(G110, 50, 15, T['sky'], 0.1, 800, 0)
    return dark(f"""
    <div class="section">Act IV — Paper 2</div>
    <div class="h" style="font-size:80px;margin-bottom:48px;">Context is not a bucket to fill.<br><span style="color:{T['sky']};">It’s an environment to explore.</span></div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:24px;color:{T['gray']};margin-top:40px;max-width:900px;">
      Long context should not be read as one giant slab.<br>
      It must be explored as a structured environment.</div>""", ca)

def slide_18():
    return dark(f"""
    <div class="section">Recursive Language Models</div>
    <div style="display:flex;gap:80px;">
      <div style="flex:1;">
        <div style="font-size:24px;font-weight:700;color:{T['berry']};letter-spacing:4px;margin-bottom:32px;">STANDARD LLM</div>
        <div class="h" style="font-size:64px;">The Speed<br>Reader</div>
      </div>
      <div style="flex:1;">
        <div style="font-size:24px;font-weight:700;color:{T['sky']};letter-spacing:4px;margin-bottom:32px;">RLM</div>
        <div class="h" style="font-size:64px;">The<br>Librarian</div>
      </div>
    </div>
    <div class="bar" style="width:100px;background:{T['sky']};margin-top:60px;"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:32px;">
      It explores, chooses, checks and gathers evidence iteratively.</div>""")

def slide_19():
    return dark(f"""
    <div class="section">How RLMs Work</div>
    <div style="display:flex;gap:32px;margin-top:32px;">
      <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(255,255,255,0.02);">
        <div style="font-size:32px;font-weight:900;margin-bottom:16px;">Search</div><div style="font-size:18px;color:{T['gray']};">Navigate relations</div></div>
      <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(255,255,255,0.02);">
        <div style="font-size:32px;font-weight:900;margin-bottom:16px;">Peek</div><div style="font-size:18px;color:{T['gray']};">Preview chunks</div></div>
      <div style="flex:1;padding:40px;border-top:5px solid {T['sky']};background:rgba(255,255,255,0.02);">
        <div style="font-size:32px;font-weight:900;margin-bottom:16px;">Verify</div><div style="font-size:18px;color:{T['gray']};">Check evidence</div></div>
    </div>
    <div style="font-size:28px;font-weight:900;margin-top:48px;">Programmatic exploration instead of passive reading.</div>""")

def slide_20():
    return light(f"""
    <div class="section">RLM-on-KG</div>
    <div class="h" style="font-size:110px;">The KG becomes the<br><span style="color:{T['sky']};">environment.</span></div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:32px;color:{T['gray']};margin-top:40px;">
      The system navigates entity-first.<br>
      Retrieval becomes <b>live graph traversal</b> at query time.</div>""")

def slide_21():
    ca = svg_grid(G30, 60, 10, T['sky'], 0.1, 0, 0)
    return dark(f"""
    <div class="h" style="font-size:120px;">It doesn't search.<br><span style="color:{T['sky']};">It explores.</span></div>
    <div style="display:flex;gap:24px;margin-top:60px;font-size:28px;font-weight:900;color:{T['gray']};">
      <div>Seed</div><div>→</div><div>Expand</div><div>→</div><div>Verify</div><div>→</div><div>Collect</div><div>→</div><div>Cite</div>
    </div>
    <div style="font-size:32px;margin-top:60px;">Retrieval as policy, not lookup.</div>""", ca)

def slide_22():
    return light(f"""
    <div class="section">Benchmark Results</div>
    <div class="h" style="font-size:80px;">Why Graphs Win When<br>Evidence is Scattered</div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:40px;max-width:900px;">
      Across distant parts of the corpus, flat retrieval weakens.<br>
      <b>Graph-guided navigation</b> maintains a clear advantage.</div>""")

def slide_23():
    return dark(f"""
    <div class="section">Separation of Concerns</div>
    <div style="display:flex;gap:80px;">
      <div style="flex:1;">
        <div style="font-size:20px;font-weight:700;color:{T['sky']};margin-bottom:24px;letter-spacing:3px;">LLM EXPLORES</div>
        <div style="font-size:28px;line-height:1.4;">Breadth, traversal,<br>reasoning.</div>
      </div>
      <div style="flex:1;">
        <div style="font-size:20px;font-weight:700;color:{T['leaf']};margin-bottom:24px;letter-spacing:3px;">VECTORS RANK</div>
        <div style="font-size:28px;line-height:1.4;">Proximity, precision,<br>ordering.</div>
      </div>
    </div>
    <div style="font-size:32px;font-weight:900;margin-top:60px;">Conflating them is why systems fail.</div>""")

def slide_24():
    return dark(f"""
    <div class="section">Capabilities</div>
    <div class="h" style="font-size:90px;">The Model<br><span style="color:{T['sky']};">Capability Gap</span></div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:40px;max-width:900px;">
      The difference is not architecture alone.<br>
      It’s how well a model follows an <b>exploration policy</b> over structure.</div>""")

def slide_25():
    return light(f"""
    <div class="section">Comparison</div>
    <div class="h" style="font-size:80px;">RLM vs GraphRAG</div>
    <div style="display:flex;gap:40px;margin-top:48px;">
      <div style="flex:1;padding:40px;background:{T['gray_light']};border-bottom:6px solid {T['sky']};">
        <div style="font-size:36px;font-weight:900;">45.8</div><div style="font-size:16px;">RLM-on-KG</div></div>
      <div style="flex:1;padding:40px;background:{T['gray_light']};border-bottom:6px solid {T['gray']};">
        <div style="font-size:36px;font-weight:900;">45.6</div><div style="font-size:16px;">GraphRAG</div></div>
    </div>
    <div style="font-size:28px;margin-top:48px;font-weight:900;">Same graph. Different exploration policy.</div>""")

# ═══════════════════════════════════════════════════════════
# ACT V — FROM RESEARCH TO STRATEGY
# ═══════════════════════════════════════════════════════════

def slide_26():
    return light(f"""
    <div class="section">Act V</div>
    <div class="h" style="font-size:84px;">The gap is behavioral.<br><span style="color:{T['sky']};">That means it’s trainable.</span></div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:28px;color:{T['gray']};margin-top:40px;max-width:900px;">
      Better search is a policy problem.<br>
      Graph-grounded exploration can be distilled and fine-tuned.</div>""")

def slide_27():
    return dark(f"""
    <div class="section">Evolution</div>
    <div style="display:flex;gap:60px;align-items:center;">
       <div style="font-size:100px;font-weight:900;color:{T['gray']};">2024</div>
       <div style="font-size:60px;">→</div>
       <div style="font-size:100px;font-weight:900;color:{T['sky']};">2026</div>
    </div>
    <div class="h" style="font-size:48px;margin-top:40px;">AI visibility is shifting from<br>mentions to <b>reasoning utility.</b></div>""")

def slide_28():
    return light(f"""
    <div class="section">The New Workflow</div>
    <div style="display:flex;gap:40px;align-items:center;margin-top:32px;">
      <div style="flex:1;text-align:center;">
        <div style="font-size:14px;font-weight:700;letter-spacing:2px;margin-bottom:16px;">CLASSIC SEO</div>
        <div style="font-size:24px;font-weight:900;">Crawl<br>Index<br>Rank</div>
      </div>
      <div style="font-size:40px;">→</div>
      <div style="flex:1;text-align:center;">
        <div style="font-size:14px;font-weight:700;letter-spacing:2px;margin-bottom:16px;color:{T['sky']};">AI VISIBILITY</div>
        <div style="font-size:24px;font-weight:900;color:{T['sky']};">Explore<br>Verify<br>Cite</div>
      </div>
    </div>""")

def slide_29():
    return dark(f"""
    <div class="section">Diagnostic Metrics</div>
    <div class="h" style="font-size:72px;margin-bottom:48px;">The Navigability Audit</div>
    <div style="display:flex;flex-wrap:wrap;gap:20px;max-width:1000px;">
      <div style="padding:20px;border:1px solid rgba(255,255,255,0.2);font-size:18px;">Entity Reachability</div>
      <div style="padding:20px;border:1px solid rgba(255,255,255,0.2);font-size:18px;">Chunk-to-Entity Coverage</div>
      <div style="padding:20px;border:1px solid rgba(255,255,255,0.2);font-size:18px;">Evidence Path Length</div>
      <div style="padding:20px;border:1px solid rgba(255,255,255,0.2);font-size:18px;">Branching Ambiguity</div>
      <div style="padding:20px;border:1px solid rgba(255,255,255,0.2);font-size:18px;">Citation Usefulness</div>
    </div>""")

def slide_30():
    return light(f"""
    <div class="section">Final Contribution</div>
    <div class="h" style="font-size:80px;line-height:1.1;">Valid markup is not enough.<br><span style="color:{T['sky']};">Navigability is the goal.</span></div>
    <div class="bar" style="width:100px;background:{T['sky']};"></div>
    <div style="font-size:24px;color:{T['gray']};margin-top:40px;">
      Does the structure improve exploration, verification, and evidence collection?</div>""")

def slide_31():
    ca = svg_grid(G30, 80, 20, T['sky'], 0.2, 800, 0)
    return dark(f"""
    <div class="h" style="font-size:100px;">As context expands,<br>the moat is no longer<br>content volume.</div>
    <div class="h" style="font-size:100px;color:{T['sky']};margin-top:32px;">It is the structure.</div>
    <div style="font-size:32px;color:{T['gray']};margin-top:60px;">It’s what lets agents compress, navigate and verify.</div>""", ca)

def slide_32():
    return dark(f"""
    <div class="section">Thank You</div>
    <div class="h" style="font-size:90px;margin-bottom:60px;">Structure Is the Moat</div>
    <div style="display:flex;gap:48px;font-size:20px;color:{T['gray']};">
      <div><b>Preprints</b> · WL.ai/Research</div>
      <div><b>Code</b> · github.com/wordlift</div>
      <div><b>Connect</b> · @cyberandy</div>
    </div>
    <div style="margin-top:80px;font-size:32px;font-weight:900;color:{T['sky']};">SEO as memory design, not page publishing.</div>""")

ALL_SLIDES = [
    ("01_title.png", slide_01),
    ("02_origin.png", slide_02),
    ("03_numbers.png", slide_03),
    ("04_more_context.png", slide_04),
    ("05_journey.png", slide_05),
    ("06_three_shifts.png", slide_06),
    ("07_two_responses.png", slide_07),
    ("08_memory_layer.png", slide_08),
    ("09_experiment.png", slide_09),
    ("10_takeaway_1.png", slide_10),
    ("11_compression.png", slide_11),
    ("12_turboquant.png", slide_12),
    ("13_silent_failure.png", slide_13),
    ("14_zero_bias.png", slide_14),
    ("15_landscape.png", slide_15),
    ("16_visibility.png", slide_16),
    ("17_environment.png", slide_17),
    ("18_rlm.png", slide_18),
    ("19_how_it_works.png", slide_19),
    ("20_rlm_on_kg.png", slide_20),
    ("21_explores.png", slide_21),
    ("22_benchmark.png", slide_22),
    ("23_separation.png", slide_23),
    ("24_capability.png", slide_24),
    ("25_comparison.png", slide_25),
    ("26_behavioral.png", slide_26),
    ("27_evolution.png", slide_27),
    ("28_new_workflow.png", slide_28),
    ("29_audit.png", slide_29),
    ("30_conclusion.png", slide_30),
    ("31_thesis.png", slide_31),
    ("32_cta.png", slide_32),
]

async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    # Clean old files
    for f in OUT.glob("*.png"): f.unlink()
    print(f"Generating {len(ALL_SLIDES)} slides — Final Editorial Plan v2...\n")
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

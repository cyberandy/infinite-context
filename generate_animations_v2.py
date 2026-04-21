#!/usr/bin/env python3
"""
Full animation set — one GIF per slide (29 total).
Transparent-ready overlays for Google Slides assembly.
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

    # ── 01 TITLE ───────────────────────────────────────
    ("01_title_reveal", "dark", """
    <style>
    @keyframes titleUp{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:translateY(0)}}
    @keyframes barGrow{from{width:0}to{width:80px}}
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    </style>
    <div style="padding:80px 100px;font-family:%(font)s;color:white;display:flex;flex-direction:column;height:100%%;">
      <div style="margin-top:auto;margin-bottom:auto;">
        <div style="font-size:14px;font-weight:700;letter-spacing:5px;text-transform:uppercase;
             color:%(sky)s;animation:fadeIn 0.6s ease-out forwards;opacity:0;">SEO Week 2026</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;margin-top:20px;
             animation:titleUp 0.8s ease-out 0.3s forwards;opacity:0;transform:translateY(40px);">Structure</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;
             animation:titleUp 0.8s ease-out 0.5s forwards;opacity:0;transform:translateY(40px);">Is the</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;
             animation:titleUp 0.8s ease-out 0.7s forwards;opacity:0;transform:translateY(40px);">Moat</div>
        <div style="height:4px;background:%(sky)s;margin-top:36px;animation:barGrow 0.6s ease-out 1.2s forwards;width:0;"></div>
        <div style="font-size:20px;color:%(gray)s;margin-top:24px;animation:fadeIn 0.8s ease-out 1.5s forwards;opacity:0;">
          What the context explosion means for how AI finds, navigates and ranks your content</div>
      </div>
    </div>"""),

    # ── 02 WEIGHT PROBLEM ──────────────────────────────
    ("02_context_chaos", "dark", """
    <style>
    @keyframes barEntropy{0%%{width:0;opacity:0}20%%{width:20%%;opacity:1}100%%{width:100%%;opacity:0.2}}
    @keyframes chaosFlow{0%%{background-position:0%% 0%%}100%%{background-position:100%% 100%%}}
    @keyframes signalDecay{0%%{opacity:1;transform:scale(1)}80%%{opacity:0.3;transform:scale(0.8)}100%%{opacity:0;transform:scale(0.5)}}
    @keyframes glitch{0%%{transform:skew(0deg)}20%%{transform:skew(2deg)}40%%{transform:skew(-2deg)}60%%{transform:skew(1deg)}100%%{transform:skew(0deg)}}
    
    .row{margin-bottom:24px;position:relative;}
    .label{font-size:16px;font-weight:700;color:%(sky)s;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
    .bar-chaos{height:12px;width:100%%;background:linear-gradient(90deg, %(sky)s, transparent);
               animation:barEntropy 4s ease-in-out infinite;opacity:0;}
    </style>
    <div style="padding:60px 80px;font-family:%(font)s;color:white;display:flex;flex-direction:column;height:100%%;">
      <div style="position:relative;z-index:10;">
        <div class="row" style="animation:glitch 2s infinite;">
          <div class="label">KV Cache O(n²)</div>
          <div class="bar-chaos" style="animation-delay:0s;"></div>
        </div>
        <div class="row" style="animation:glitch 2.5s infinite;">
          <div class="label">Vector Search Space</div>
          <div class="bar-chaos" style="animation-delay:0.5s;background:linear-gradient(90deg, %(sand)s, transparent);"></div>
        </div>
        <div class="row" style="animation:glitch 3s infinite;">
          <div class="label">Neural Context Loss</div>
          <div class="bar-chaos" style="animation-delay:1s;background:linear-gradient(90deg, %(berry)s, transparent);"></div>
        </div>
      </div>
      
      <div style="margin-top:auto;text-align:center;padding:40px;border:2px dashed %(gray)s;
           animation:signalDecay 5s ease-in forwards;">
        <div style="font-size:24px;font-weight:900;color:%(leaf)s;letter-spacing:2px;">RELEVANT SIGNAL</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:8px;">Burying the truth in the weight...</div>
      </div>
      
      <!-- Rule 30 Style Background Pattern -->
      <div style="position:absolute;right:0;top:0;width:100%%;height:100%%;opacity:0.1;z-index:1;overflow:hidden;pointer-events:none;">
        <svg width="800" height="600" viewBox="0 0 800 600">
          <defs>
            <pattern id="chaosPattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <rect width="2" height="2" fill="%(sky)s" opacity="0.5" />
              <rect x="10" y="10" width="4" height="4" fill="%(berry)s" opacity="0.3" />
            </pattern>
          </defs>
          <rect width="800" height="600" fill="url(#chaosPattern)" />
        </svg>
      </div>
    </div>"""),

    # ── 03 QUERY → JOURNEY ─────────────────────────────
    ("03_two_columns", "dark", """
    <style>
    @keyframes slideL{from{opacity:0;transform:translateX(-30px)}to{opacity:1;transform:translateX(0)}}
    @keyframes slideR{from{opacity:0;transform:translateX(30px)}to{opacity:1;transform:translateX(0)}}
    @keyframes pulseNode{0%%{transform:scale(1);opacity:0.6}50%%{transform:scale(1.3);opacity:1}100%%{transform:scale(1);opacity:0.6}}
    @keyframes traverse{
      0%%{offset-distance:0%%;opacity:0}
      10%%{opacity:1}
      90%%{opacity:1}
      100%%{offset-distance:100%%;opacity:0}
    }
    .node{width:10px;height:10px;background:%(sky)s;border-radius:50%%;position:absolute;opacity:0.6;}
    .edge{stroke:%(sky)s;stroke-width:1;opacity:0.2;}
    .traveler{
      width:6px;height:6px;background:%(leaf)s;border-radius:50%%;
      position:absolute;
      offset-path: path('M 50 150 L 150 50 L 250 180 L 350 80 L 450 200');
      animation: traverse 4s linear infinite;
      box-shadow: 0 0 10px %(leaf)s;
    }
    </style>
    <div style="display:flex;gap:40px;padding:40px;font-family:%(font)s;color:white;height:100%%;position:relative;">
      <!-- Left side: The Old Model -->
      <div style="flex:1;padding:28px;border-top:4px solid %(gray)s;
           animation:slideL 0.7s ease-out 0.3s forwards;opacity:0;z-index:10;background:rgba(13,13,13,0.8);">
        <div style="font-size:13px;font-weight:700;color:%(gray)s;letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">The Old Model</div>
        <div style="font-size:17px;color:%(gray)s;line-height:2;">Stateless · Symmetric · One-shot</div>
        <div style="font-size:20px;font-weight:700;margin-top:16px;">The document was the unit.</div>
      </div>

      <!-- Right side: The Agent Model -->
      <div style="flex:1;padding:28px;border-top:4px solid %(sky)s;
           animation:slideR 0.7s ease-out 0.6s forwards;opacity:0;position:relative;z-index:10;background:rgba(13,13,13,0.8);">
        <div style="font-size:13px;font-weight:700;color:%(sky)s;letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">The Agent Model</div>
        <div style="font-size:17px;color:%(gray)s;line-height:2;">Stateful · Asymmetric · Multi-hop</div>
        <div style="font-size:20px;font-weight:700;margin-top:16px;">The entity is the unit.</div>
        
        <!-- Subtle Traversal Animation in background of this column -->
        <div style="position:absolute;top:100px;left:0;width:100%%;height:200px;opacity:0.4;z-index:-1;">
          <svg width="400" height="250" viewBox="0 0 400 250">
            <path d="M 50 150 L 150 50 L 250 180 L 350 80 L 450 200" fill="none" stroke="%(sky)s" stroke-width="1" stroke-dasharray="4 4" opacity="0.2" />
            <circle cx="50" cy="150" r="4" fill="%(sky)s" style="animation:pulseNode 2s infinite 0s"/>
            <circle cx="150" cy="50" r="4" fill="%(sky)s" style="animation:pulseNode 2s infinite 0.5s"/>
            <circle cx="250" cy="180" r="4" fill="%(sky)s" style="animation:pulseNode 2s infinite 1.0s"/>
            <circle cx="350" cy="80" r="4" fill="%(sky)s" style="animation:pulseNode 2s infinite 1.5s"/>
            <div class="traveler"></div>
          </svg>
        </div>
      </div>
    </div>"""),

    # ── 04 THREE SHIFTS ────────────────────────────────
    ("04_three_shifts", "dark", """
    <style>
    @keyframes itemIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    @keyframes arrowPulse{0%%{opacity:0.2}50%%{opacity:1}100%%{opacity:0.2}}
    </style>
    <div style="padding:40px;font-family:%(font)s;color:white;height:100%%;">
      <div style="display:flex;gap:24px;margin-bottom:36px;align-items:flex-start;
           animation:itemIn 0.6s ease-out 0.2s forwards;opacity:0;">
        <div style="font-size:48px;font-weight:900;color:%(sky)s;line-height:1;min-width:70px;">01</div>
        <div><div style="font-size:24px;font-weight:900;">Retrieval <span style="animation:arrowPulse 2s infinite;">→</span> Navigation</div>
          <div style="font-size:16px;color:%(gray)s;margin-top:4px;">Reachability becomes the primary moat.</div></div></div>
      <div style="display:flex;gap:24px;margin-bottom:36px;align-items:flex-start;
           animation:itemIn 0.6s ease-out 0.7s forwards;opacity:0;">
        <div style="font-size:48px;font-weight:900;color:%(sky)s;line-height:1;min-width:70px;">02</div>
        <div><div style="font-size:24px;font-weight:900;">Documents <span style="animation:arrowPulse 2s infinite;">→</span> Entities</div>
          <div style="font-size:16px;color:%(gray)s;margin-top:4px;">The unit of search logic is the node.</div></div></div>
      <div style="display:flex;gap:24px;align-items:flex-start;
           animation:itemIn 0.6s ease-out 1.2s forwards;opacity:0;">
        <div style="font-size:48px;font-weight:900;color:%(sky)s;line-height:1;min-width:70px;">03</div>
        <div><div style="font-size:24px;font-weight:900;">One Model <span style="animation:arrowPulse 2s infinite;">→</span> A System</div>
          <div style="font-size:16px;color:%(gray)s;margin-top:4px;">Coordination between multiple layers.</div></div></div>
    </div>"""),

    # ── 05 COMPRESSION PARADOX (chapter) ───────────────
    ("05_chapter_reveal", "dark", """
    <style>
    @keyframes titleUp{from{opacity:0;transform:translateY(50px)}to{opacity:1;transform:translateY(0)}}
    @keyframes barGrow{from{width:0}to{width:80px}}
    </style>
    <div style="padding:80px 100px;font-family:%(font)s;color:white;display:flex;flex-direction:column;height:100%%;">
      <div style="margin-top:auto;margin-bottom:auto;">
        <div style="font-size:14px;font-weight:700;letter-spacing:5px;text-transform:uppercase;
             color:%(sky)s;animation:titleUp 0.6s ease-out forwards;opacity:0;">Act II</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;margin-top:20px;
             animation:titleUp 0.8s ease-out 0.3s forwards;opacity:0;">The</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;
             animation:titleUp 0.8s ease-out 0.5s forwards;opacity:0;">Compression</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;
             animation:titleUp 0.8s ease-out 0.7s forwards;opacity:0;">Paradox</div>
        <div style="height:4px;background:%(sky)s;margin-top:36px;animation:barGrow 0.6s ease-out 1.2s forwards;width:0;"></div>
      </div>
    </div>"""),

    # ── 06 TURBOQUANT ──────────────────────────────────
    ("06_turboquant_counter", "dark", """
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
    <div style="display:flex;gap:60px;padding:60px;font-family:%(font)s;">
      <div><div class="stat s1"></div><div style="font-size:18px;color:%(gray)s;margin-top:8px;">smaller</div></div>
      <div><div class="stat s2"></div><div style="font-size:18px;color:%(gray)s;margin-top:8px;">faster</div></div>
      <div><div class="stat s3" style="font-size:120px;font-weight:900;line-height:0.9;letter-spacing:-6px;">0</div>
        <div style="font-size:18px;color:%(gray)s;margin-top:8px;">degradation</div></div>
    </div>"""),

    # ── 07 SILENT RANKING ──────────────────────────────
    ("07_three_columns", "dark", """
    <style>
    @keyframes colIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="display:flex;gap:24px;padding:40px;font-family:%(font)s;color:white;">
      <div style="flex:1;padding:24px;border-left:4px solid %(berry)s;
           animation:colIn 0.6s ease-out 0.2s forwards;opacity:0;">
        <div style="font-size:16px;font-weight:900;color:%(berry)s;margin-bottom:8px;">The Math</div>
        <div style="font-size:56px;font-weight:900;">2/π</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:6px;">bias at 1-bit</div></div>
      <div style="flex:1;padding:24px;border-left:4px solid %(sand)s;
           animation:colIn 0.6s ease-out 0.6s forwards;opacity:0;">
        <div style="font-size:16px;font-weight:900;color:%(sand)s;margin-bottom:8px;">The System</div>
        <div style="font-size:28px;font-weight:900;">Broken Compass</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:6px;">Cosine stops reflecting similarity</div></div>
      <div style="flex:1;padding:24px;border-left:4px solid %(gray)s;
           animation:colIn 0.6s ease-out 1.0s forwards;opacity:0;">
        <div style="font-size:16px;font-weight:900;color:%(gray)s;margin-bottom:8px;">The Consequence</div>
        <div style="font-size:28px;font-weight:900;">Invisible Degradation</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:6px;">No error. Just worse answers.</div></div>
    </div>"""),

    # ── 08 ZERO-BIAS ───────────────────────────────────
    ("08_formula_reveal", "dark", """
    <style>
    @keyframes zoomIn{from{opacity:0;transform:scale(0.5)}to{opacity:1;transform:scale(1)}}
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    </style>
    <div style="padding:60px;font-family:%(font)s;color:white;">
      <div style="font-size:20px;color:%(sky)s;font-weight:700;margin-bottom:16px;
           animation:fadeIn 0.6s ease-out forwards;">QJL correction</div>
      <div style="font-size:64px;font-weight:900;animation:zoomIn 0.8s ease-out 0.4s forwards;opacity:0;">
        Inner products are now</div>
      <div style="font-size:64px;font-weight:900;color:%(sky)s;
           animation:zoomIn 0.8s ease-out 0.8s forwards;opacity:0;">provably unbiased.</div>
      <div style="height:4px;width:60px;background:%(leaf)s;margin-top:40px;
           animation:fadeIn 0.5s ease-out 1.5s forwards;opacity:0;"></div>
      <div style="font-size:18px;color:%(gray)s;margin-top:16px;
           animation:fadeIn 0.6s ease-out 1.8s forwards;opacity:0;">3,957s → 0.002s indexing</div>
    </div>"""),

    # ── 09 QUANT LANDSCAPE ─────────────────────────────
    ("09_table_highlight", "light", """
    <style>
    @keyframes rowIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
    @keyframes highlightRow{from{background:transparent}to{background:rgba(52,82,219,0.1)}}
    </style>
    <div style="padding:40px;font-family:%(font)s;color:%(dark)s;">
      <table style="width:100%%;border-collapse:collapse;font-size:17px;">
        <tr style="border-bottom:2px solid %(dark)s;">
          <th style="text-align:left;padding:12px;">Algorithm</th>
          <th style="text-align:center;padding:12px;">Unbiased</th>
          <th style="text-align:center;padding:12px;">Codebook-Free</th>
          <th style="text-align:center;padding:12px;">GPU-Native</th>
          <th style="text-align:center;padding:12px;">Data-Oblivious</th></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 0.2s forwards;opacity:0;">
          <td style="padding:12px;color:%(gray)s;">PQ / OPQ</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 0.5s forwards;opacity:0;">
          <td style="padding:12px;color:%(gray)s;">ScaNN</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">partial</td><td style="text-align:center;">✗</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 0.8s forwards;opacity:0;">
          <td style="padding:12px;color:%(gray)s;">RaBitQ</td>
          <td style="text-align:center;">✗</td><td style="text-align:center;">✗</td>
          <td style="text-align:center;">✓</td><td style="text-align:center;">✗</td></tr>
        <tr style="animation:rowIn 0.4s ease-out 1.2s forwards,highlightRow 0.5s ease-out 1.5s forwards;
            opacity:0;border-bottom:2px solid %(sky)s;">
          <td style="padding:12px;font-weight:900;color:%(sky)s;">TurboQuant</td>
          <td style="text-align:center;color:%(sky)s;font-weight:900;">✓</td>
          <td style="text-align:center;color:%(sky)s;font-weight:900;">✓</td>
          <td style="text-align:center;color:%(sky)s;font-weight:900;">✓</td>
          <td style="text-align:center;color:%(sky)s;font-weight:900;">✓</td></tr>
      </table>
    </div>"""),

    # ── 10 TURBO DEMO ──────────────────────────────────
    ("10_qr_pulse", "dark", """
    <style>
    @keyframes pulse{0%%{box-shadow:0 0 0 0 rgba(52,82,219,0.4)}70%%{box-shadow:0 0 0 30px rgba(52,82,219,0)}100%%{box-shadow:0 0 0 0 rgba(52,82,219,0)}}
    @keyframes fadeIn{from{opacity:0;transform:scale(0.8)}to{opacity:1;transform:scale(1)}}
    </style>
    <div style="display:flex;align-items:center;justify-content:center;height:100%%;font-family:%(font)s;">
      <div style="text-align:center;animation:fadeIn 0.8s ease-out forwards;">
        <div style="width:240px;height:240px;border:3px solid %(sky)s;border-radius:12px;
             display:flex;align-items:center;justify-content:center;
             background:rgba(52,82,219,0.08);animation:pulse 2s infinite;margin:0 auto;">
          <div><div style="font-size:52px;font-weight:900;color:%(sky)s;">QR</div>
            <div style="font-size:13px;color:%(gray)s;margin-top:6px;">Scan to try live</div></div></div>
        <div style="margin-top:20px;font-size:20px;font-weight:700;font-family:monospace;color:%(sky)s;">wor.ai/turbo-quant</div>
      </div>
    </div>"""),

    # ── 11 PIPELINE STEPS ──────────────────────────────
    ("11_pipeline_steps", "dark", """
    <style>
    @keyframes stepIn{from{opacity:0.15;transform:scale(0.95)}to{opacity:1;transform:scale(1)}}
    .step{padding:14px 22px;font-size:16px;font-weight:700;border:2px solid rgba(255,255,255,0.25);
          opacity:0.15;animation:stepIn 0.4s ease-out forwards;font-family:%(font)s;color:white;}
    .arrow{color:%(gray)s;font-size:22px;opacity:0.15;animation:stepIn 0.3s ease-out forwards;}
    </style>
    <div style="display:flex;align-items:center;gap:10px;padding:30px;">
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

    # ── 12 GRAPH NODES (RLM) ───────────────────────────
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

    # ── 13 STAT COUNTER (71%) ──────────────────────────
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

    # ── 14 SEPARATION ──────────────────────────────────
    ("14_separation_panels", "dark", """
    <style>
    @keyframes slideL{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:translateX(0)}}
    @keyframes slideR{from{opacity:0;transform:translateX(40px)}to{opacity:1;transform:translateX(0)}}
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    </style>
    <div style="display:flex;gap:24px;padding:40px;font-family:%(font)s;color:white;align-items:center;">
      <div style="flex:1;padding:36px;border-top:4px solid %(sky)s;background:rgba(52,82,219,0.05);
           animation:slideL 0.7s ease-out 0.3s forwards;opacity:0;">
        <div style="font-size:28px;font-weight:900;color:%(sky)s;margin-bottom:8px;">LLM Explores</div>
        <div style="font-size:16px;color:%(gray)s;line-height:1.6;">Navigation breadth<br>Graph traversal<br>Multi-hop reasoning</div></div>
      <div style="font-size:40px;color:%(gray)s;animation:fadeIn 0.5s ease-out 0.8s forwards;opacity:0;">×</div>
      <div style="flex:1;padding:36px;border-top:4px solid %(leaf)s;background:rgba(34,162,134,0.05);
           animation:slideR 0.7s ease-out 0.6s forwards;opacity:0;">
        <div style="font-size:28px;font-weight:900;color:%(leaf)s;margin-bottom:8px;">Vectors Rank</div>
        <div style="font-size:16px;color:%(gray)s;line-height:1.6;">Cosine similarity<br>Geometric precision<br>Final ordering</div></div>
    </div>"""),

    # ── 15 MODEL GAP ───────────────────────────────────
    ("15_model_cards", "light", """
    <style>
    @keyframes cardIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="display:flex;gap:20px;padding:40px;font-family:%(font)s;color:%(dark)s;">
      <div style="flex:1;padding:28px;border-top:4px solid %(sky)s;
           animation:cardIn 0.6s ease-out 0.2s forwards;opacity:0;">
        <div style="font-size:18px;font-weight:900;">Claude Haiku</div>
        <div style="font-size:60px;font-weight:900;color:%(sky)s;line-height:1;letter-spacing:-3px;margin-top:8px;">+4.37pp</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:6px;">Strong gain</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(sand)s;
           animation:cardIn 0.6s ease-out 0.6s forwards;opacity:0;">
        <div style="font-size:18px;font-weight:900;">Gemini Flash Lite</div>
        <div style="font-size:60px;font-weight:900;color:%(sand)s;line-height:1;letter-spacing:-3px;margin-top:8px;">+0.84pp</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:6px;">Marginal</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(berry)s;
           animation:cardIn 0.6s ease-out 1.0s forwards;opacity:0;">
        <div style="font-size:18px;font-weight:900;">Gemma 4</div>
        <div style="font-size:60px;font-weight:900;color:%(berry)s;line-height:1;letter-spacing:-3px;margin-top:8px;">−0.78pp</div>
        <div style="font-size:14px;color:%(gray)s;margin-top:6px;">Negative</div></div>
    </div>"""),

    # ── 17 DISTILLATION PIPELINE ───────────────────────
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

    # ── 18 SLM EDGE ────────────────────────────────────
    ("18_slm_props", "dark", """
    <style>
    @keyframes propIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
    </style>
    <div style="display:flex;gap:24px;padding:40px;font-family:%(font)s;color:white;">
      <div style="flex:1;padding:28px;border-left:4px solid %(leaf)s;
           animation:propIn 0.6s ease-out 0.2s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(leaf)s;">Secure</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:6px;">Data never leaves the device</div></div>
      <div style="flex:1;padding:28px;border-left:4px solid %(sky)s;
           animation:propIn 0.6s ease-out 0.6s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(sky)s;">Fast</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:6px;">Sub-second, no round-trip</div></div>
      <div style="flex:1;padding:28px;border-left:4px solid %(sand)s;
           animation:propIn 0.6s ease-out 1.0s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(sand)s;">Yours</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:6px;">Trained on your graph</div></div>
    </div>"""),

    # ── 19 CONNECTED DATA ──────────────────────────────
    ("19_connected_steps", "dark", """
    <style>
    @keyframes itemIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="padding:40px;font-family:%(font)s;color:white;">
      <div style="display:flex;gap:20px;margin-bottom:32px;align-items:flex-start;
           animation:itemIn 0.6s ease-out 0.2s forwards;opacity:0;">
        <div style="font-size:44px;font-weight:900;color:%(sky)s;line-height:1;min-width:60px;">01</div>
        <div><div style="font-size:22px;font-weight:900;">Connectivity enables distillation</div>
          <div style="font-size:15px;color:%(gray)s;">Connected data teaches navigation</div></div></div>
      <div style="display:flex;gap:20px;margin-bottom:32px;align-items:flex-start;
           animation:itemIn 0.6s ease-out 0.7s forwards;opacity:0;">
        <div style="font-size:44px;font-weight:900;color:%(sky)s;line-height:1;min-width:60px;">02</div>
        <div><div style="font-size:22px;font-weight:900;">Connected data multiplies</div>
          <div style="font-size:15px;color:%(gray)s;">Cross-property links compound</div></div></div>
      <div style="display:flex;gap:20px;align-items:flex-start;
           animation:itemIn 0.6s ease-out 1.2s forwards;opacity:0;">
        <div style="font-size:44px;font-weight:900;color:%(sky)s;line-height:1;min-width:60px;">03</div>
        <div><div style="font-size:22px;font-weight:900;">Disconnected = dead end</div>
          <div style="font-size:15px;color:%(gray)s;">Without structure, training has no signal</div></div></div>
    </div>"""),

    # ── 20 FLOOR IS SET ────────────────────────────────
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

    # ── 21 MOAT = GRAPH ────────────────────────────────
    ("21_four_pillars", "dark", """
    <style>
    @keyframes pillarIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="display:flex;gap:12px;padding:40px;font-family:%(font)s;color:white;">
      <div style="flex:1;padding:20px;border-top:3px solid %(sky)s;background:rgba(52,82,219,0.05);
           animation:pillarIn 0.6s ease-out 0s forwards;opacity:0;">
        <div style="font-size:15px;font-weight:900;">Limitless Context</div></div>
      <div style="flex:1;padding:20px;border-top:3px solid %(sky)s;background:rgba(52,82,219,0.05);
           animation:pillarIn 0.6s ease-out 0.3s forwards;opacity:0;">
        <div style="font-size:15px;font-weight:900;">Billion-Scale Search</div></div>
      <div style="flex:1;padding:20px;border-top:3px solid %(sky)s;background:rgba(52,82,219,0.05);
           animation:pillarIn 0.6s ease-out 0.6s forwards;opacity:0;">
        <div style="font-size:15px;font-weight:900;">On-Device Intelligence</div></div>
      <div style="flex:1;padding:20px;border-top:3px solid %(sky)s;background:%(sky)s;
           animation:pillarIn 0.6s ease-out 0.9s forwards;opacity:0;">
        <div style="font-size:15px;font-weight:900;">Navigable KG</div></div>
    </div>"""),

    # ── 22 SEO PLAYBOOK (chapter) ──────────────────────
    ("22_playbook_chapter", "dark", """
    <style>
    @keyframes titleUp{from{opacity:0;transform:translateY(50px)}to{opacity:1;transform:translateY(0)}}
    @keyframes barGrow{from{width:0}to{width:80px}}
    </style>
    <div style="padding:80px 100px;font-family:%(font)s;color:white;display:flex;flex-direction:column;height:100%%;">
      <div style="margin-top:auto;margin-bottom:auto;">
        <div style="font-size:14px;font-weight:700;letter-spacing:5px;text-transform:uppercase;
             color:%(sky)s;animation:titleUp 0.6s ease-out forwards;opacity:0;">Act V</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;margin-top:20px;
             animation:titleUp 0.8s ease-out 0.3s forwards;opacity:0;">The SEO</div>
        <div style="font-size:100px;font-weight:900;line-height:0.92;letter-spacing:-5px;
             animation:titleUp 0.8s ease-out 0.5s forwards;opacity:0;">Playbook</div>
        <div style="height:4px;background:%(sky)s;margin-top:36px;animation:barGrow 0.6s ease-out 1.0s forwards;width:0;"></div>
      </div>
    </div>"""),

    # ── 23 VISIBILITY SHIFT ────────────────────────────
    ("23_visibility_columns", "light", """
    <style>
    @keyframes slideL{from{opacity:0;transform:translateX(-30px)}to{opacity:1;transform:translateX(0)}}
    @keyframes slideR{from{opacity:0;transform:translateX(30px)}to{opacity:1;transform:translateX(0)}}
    </style>
    <div style="display:flex;gap:32px;padding:40px;font-family:%(font)s;color:%(dark)s;height:100%%;">
      <div style="flex:1;padding:28px;border-top:4px solid %(gray)s;
           animation:slideL 0.7s ease-out 0.3s forwards;opacity:0;">
        <div style="font-size:13px;font-weight:700;color:%(gray)s;letter-spacing:4px;text-transform:uppercase;text-decoration:line-through;margin-bottom:16px;">Mentions Era</div>
        <div style="font-size:16px;color:%(gray)s;line-height:2;">Present in training data<br>Passive: be cited<br>Measured by: brand recall</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(sky)s;
           animation:slideR 0.7s ease-out 0.6s forwards;opacity:0;">
        <div style="font-size:13px;font-weight:700;color:%(sky)s;letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">Reasoning Utility</div>
        <div style="font-size:16px;color:%(dark)s;line-height:2;">Entities connected & traversable<br>Active: be <span style="color:%(sky)s;font-weight:700;">reachable</span><br>Measured by: citation in agent outputs</div></div>
    </div>"""),

    # ── 24 GHOST CITATIONS ─────────────────────────────
    ("24_ghost_counter", "light", """
    <style>
    @keyframes count7{0%%{content:'0'}20%%{content:'1'}40%%{content:'3'}60%%{content:'5'}80%%{content:'6'}100%%{content:'7'}}
    .num::after{content:'7';font-size:240px;font-weight:900;line-height:0.82;letter-spacing:-12px;
    color:%(berry)s;animation:count7 1.5s steps(5) forwards;}
    </style>
    <div style="padding:40px;font-family:%(font)s;">
      <div><span class="num"></span><span style="font-size:160px;font-weight:900;color:%(berry)s;">%</span></div>
      <div style="font-size:28px;font-weight:700;color:%(dark)s;margin-top:12px;">Ghost Citations</div>
    </div>"""),

    # ── 25 GPT READS DIFFERENTLY ───────────────────────
    ("25_era_table", "light", """
    <style>
    @keyframes rowIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
    @keyframes colHighlight{from{background:transparent}to{background:rgba(52,82,219,0.08)}}
    </style>
    <div style="padding:40px;font-family:%(font)s;color:%(dark)s;">
      <table style="width:100%%;border-collapse:collapse;font-size:16px;">
        <tr style="border-bottom:2px solid %(dark)s;">
          <th style="text-align:left;padding:10px;width:18%%;"></th>
          <th style="text-align:center;padding:10px;color:%(gray)s;">GPT-3 era</th>
          <th style="text-align:center;padding:10px;color:%(gray)s;">GPT-4 era</th>
          <th style="text-align:center;padding:10px;color:%(sky)s;font-weight:900;">GPT-5.4 era</th></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 0.2s forwards;opacity:0;">
          <td style="padding:10px;font-weight:700;">Method</td>
          <td style="text-align:center;color:%(gray)s;">Pattern match</td>
          <td style="text-align:center;color:%(gray)s;">Semantic similarity</td>
          <td style="text-align:center;font-weight:700;color:%(sky)s;">Graph traversal</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 0.5s forwards;opacity:0;">
          <td style="padding:10px;font-weight:700;">Unit</td>
          <td style="text-align:center;color:%(gray)s;">Token</td>
          <td style="text-align:center;color:%(gray)s;">Embedding</td>
          <td style="text-align:center;font-weight:700;color:%(sky)s;">Entity</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 0.8s forwards;opacity:0;">
          <td style="padding:10px;font-weight:700;">What matters</td>
          <td style="text-align:center;color:%(gray)s;">Keyword density</td>
          <td style="text-align:center;color:%(gray)s;">Vector proximity</td>
          <td style="text-align:center;font-weight:700;color:%(sky)s;">Structural connectivity</td></tr>
        <tr style="border-bottom:1px solid #e0e0e0;animation:rowIn 0.4s ease-out 1.1s forwards;opacity:0;">
          <td style="padding:10px;font-weight:700;">Content's job</td>
          <td style="text-align:center;color:%(gray)s;">Be present</td>
          <td style="text-align:center;color:%(gray)s;">Be similar</td>
          <td style="text-align:center;font-weight:700;color:%(sky)s;">Be reachable</td></tr>
        <tr style="border-bottom:2px solid %(dark)s;animation:rowIn 0.4s ease-out 1.4s forwards;opacity:0;">
          <td style="padding:10px;font-weight:700;">Failure mode</td>
          <td style="text-align:center;color:%(gray)s;">Not indexed</td>
          <td style="text-align:center;color:%(gray)s;">Low similarity</td>
          <td style="text-align:center;font-weight:700;color:%(berry)s;">Disconnected</td></tr>
      </table>
    </div>"""),

    # ── 26 CONSISTENCY BARS ────────────────────────────
    ("26_consistency_bars", "light", """
    <style>
    @keyframes barGrow{from{width:0}to{width:var(--w)}}
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

    # ── 27 EXPLORE → VERIFY → CITE ────────────────────
    ("27_explore_verify_cite", "dark", """
    <style>
    @keyframes panelIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="display:flex;gap:20px;padding:40px;font-family:%(font)s;color:white;">
      <div style="flex:1;padding:28px;border-top:4px solid %(sky)s;background:rgba(52,82,219,0.05);
           animation:panelIn 0.6s ease-out 0s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(sky)s;">Explore</div>
        <div style="font-size:18px;font-weight:700;margin-top:8px;">Can the agent find you?</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(leaf)s;background:rgba(34,162,134,0.05);
           animation:panelIn 0.6s ease-out 0.4s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(leaf)s;">Verify</div>
        <div style="font-size:18px;font-weight:700;margin-top:8px;">Can the agent confirm you?</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(sand)s;background:rgba(194,164,29,0.05);
           animation:panelIn 0.6s ease-out 0.8s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(sand)s;">Cite</div>
        <div style="font-size:18px;font-weight:700;margin-top:8px;">Can the agent cite you?</div></div>
    </div>"""),

    # ── 28 AUTORESEARCH ────────────────────────────────
    ("28_autoresearch_panels", "dark", """
    <style>
    @keyframes panelIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    </style>
    <div style="display:flex;gap:20px;padding:40px;font-family:%(font)s;color:white;">
      <div style="flex:1;padding:28px;border-top:4px solid %(leaf)s;background:rgba(34,162,134,0.05);
           animation:panelIn 0.6s ease-out 0s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(leaf)s;">Discover</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:8px;">Surface gaps. No manual curation.</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(sky)s;background:rgba(52,82,219,0.05);
           animation:panelIn 0.6s ease-out 0.4s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(sky)s;">Synthesize</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:8px;">Grounded, citable summaries.</div></div>
      <div style="flex:1;padding:28px;border-top:4px solid %(sand)s;background:rgba(194,164,29,0.05);
           animation:panelIn 0.6s ease-out 0.8s forwards;opacity:0;">
        <div style="font-size:24px;font-weight:900;color:%(sand)s;">Act</div>
        <div style="font-size:15px;color:%(gray)s;margin-top:8px;">Queue remediation. Graph improves.</div></div>
    </div>"""),

    # ── 29 WELL-CONNECTED ──────────────────────────────
    ("29_connection_boxes", "light", """
    <style>
    @keyframes boxIn{from{opacity:0;transform:scale(0.9)}to{opacity:1;transform:scale(1)}}
    </style>
    <div style="display:flex;gap:24px;padding:40px;font-family:%(font)s;color:%(dark)s;">
      <div style="flex:1;">
        <div style="font-size:13px;font-weight:700;color:%(sky)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:12px;">Internal</div>
        <div style="padding:20px;border:2px solid #e0e0e0;margin-bottom:10px;
             animation:boxIn 0.5s ease-out 0.2s forwards;opacity:0;">
          <div style="font-size:16px;font-weight:700;">Products → Editorial</div></div>
        <div style="padding:20px;border:2px solid #e0e0e0;
             animation:boxIn 0.5s ease-out 0.5s forwards;opacity:0;">
          <div style="font-size:16px;font-weight:700;">Docs → Support → Product</div></div>
      </div>
      <div style="flex:1;">
        <div style="font-size:13px;font-weight:700;color:%(sky)s;letter-spacing:3px;text-transform:uppercase;margin-bottom:12px;">External</div>
        <div style="padding:20px;border:2px solid #e0e0e0;margin-bottom:10px;
             animation:boxIn 0.5s ease-out 0.8s forwards;opacity:0;">
          <div style="font-size:16px;font-weight:700;">Wikidata / Schema.org</div></div>
        <div style="padding:20px;border:2px solid #e0e0e0;
             animation:boxIn 0.5s ease-out 1.1s forwards;opacity:0;">
          <div style="font-size:16px;font-weight:700;">Partner Ecosystems</div></div>
      </div>
    </div>"""),

    # ── 30 CLOSING ─────────────────────────────────────
    ("30_closing_reveal", "dark", """
    <style>
    @keyframes lineIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    @keyframes barGrow{from{width:0}to{width:80px}}
    </style>
    <div style="padding:80px 100px;font-family:%(font)s;color:white;display:flex;flex-direction:column;height:100%%;">
      <div style="margin-top:auto;margin-bottom:auto;">
        <div style="font-size:48px;font-weight:900;line-height:1.1;
             animation:lineIn 0.7s ease-out 0.2s forwards;opacity:0;">Context windows will keep growing.</div>
        <div style="font-size:48px;font-weight:900;line-height:1.1;
             animation:lineIn 0.7s ease-out 0.5s forwards;opacity:0;">Models will keep getting cheaper.</div>
        <div style="font-size:48px;font-weight:900;line-height:1.1;color:%(sky)s;margin-top:24px;
             animation:lineIn 0.7s ease-out 1.0s forwards;opacity:0;">The variable that compounds</div>
        <div style="font-size:48px;font-weight:900;line-height:1.1;color:%(sky)s;
             animation:lineIn 0.7s ease-out 1.3s forwards;opacity:0;">is your data connectivity.</div>
        <div style="height:4px;background:%(sky)s;margin-top:40px;animation:barGrow 0.6s ease-out 1.8s forwards;width:0;"></div>
        <div style="font-size:24px;font-weight:700;margin-top:24px;
             animation:lineIn 0.6s ease-out 2.2s forwards;opacity:0;">Structure your knowledge now.</div>
      </div>
    </div>"""),
]


async def main():
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    print(f"Generating {len(ANIMATIONS)} animations (full deck)...\n")

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

            page = await browser.new_page(
                viewport={"width": T["W"], "height": T["H"]}, device_scale_factor=1)
            await page.set_content(full_html, wait_until="domcontentloaded")

            frames = []
            for i in range(30):
                await asyncio.sleep(0.1)
                frame_bytes = await page.screenshot(type="png")
                frames.append(frame_bytes)

            # Save preview
            preview_path = OUT / f"{name}_preview.png"
            with open(preview_path, "wb") as f:
                f.write(frames[-1])

            # Build GIF
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
                print(f"  {name}_preview.png ✓ (PIL not available)")

            await page.close()

        await browser.close()

    total = sum(f.stat().st_size for f in OUT.glob("*.gif")) // 1024 if list(OUT.glob("*.gif")) else 0
    print(f"\n✓ All {len(ANIMATIONS)} animations → {OUT}/ ({total} KB total)")


if __name__ == "__main__":
    asyncio.run(main())

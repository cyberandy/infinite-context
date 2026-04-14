#!/usr/bin/env python3
"""
Test: Build 3 slides natively in Google Slides API.
Real text elements, shapes, colors — no PNG backgrounds.
"""

import os, pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/presentations"]
CREDS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

# ── Design tokens ──────────────────────────────────────
# Google Slides API uses RGB 0–1
C = {
    "dark":  {"red": 0.051, "green": 0.051, "blue": 0.051},
    "dark2": {"red": 0.098, "green": 0.098, "blue": 0.098},
    "white": {"red": 1.0,   "green": 1.0,   "blue": 1.0},
    "sky":   {"red": 0.204, "green": 0.322, "blue": 0.859},
    "berry": {"red": 0.835, "green": 0.329, "blue": 0.443},
    "leaf":  {"red": 0.133, "green": 0.635, "blue": 0.525},
    "sand":  {"red": 0.761, "green": 0.643, "blue": 0.114},
    "gray":  {"red": 0.631, "green": 0.655, "blue": 0.686},
    "light": {"red": 0.965, "green": 0.965, "blue": 0.969},
}

# 1 inch = 914400 EMU. Slide is 10" × 5.625" (widescreen)
IN = 914400
SLIDE_W = 10 * IN
SLIDE_H = 5.625 * IN
MARGIN_L = 0.6 * IN  # left margin
MARGIN_T = 0.5 * IN  # top margin


def auth():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return creds


def rgb(color):
    return {"rgbColor": color}


def text_box(page_id, obj_id, x, y, w, h):
    """Create a text box shape."""
    return {
        "createShape": {
            "objectId": obj_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width":  {"magnitude": w, "unit": "EMU"},
                    "height": {"magnitude": h, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": x, "translateY": y,
                    "unit": "EMU",
                },
            },
        }
    }


def insert_text(obj_id, text):
    return {"insertText": {"objectId": obj_id, "text": text, "insertionIndex": 0}}


def style_text(obj_id, start, end, font_size, bold=False, color=None, font="Helvetica Neue", italic=False):
    style = {
        "fontSize": {"magnitude": font_size, "unit": "PT"},
        "bold": bold,
        "italic": italic,
        "fontFamily": font,
    }
    fields = "fontSize,bold,italic,fontFamily"
    if color:
        style["foregroundColor"] = {"opaqueColor": rgb(color)}
        fields += ",foregroundColor"
    return {
        "updateTextStyle": {
            "objectId": obj_id,
            "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end},
            "style": style,
            "fields": fields,
        }
    }


def set_bg(page_id, color):
    return {
        "updatePageProperties": {
            "objectId": page_id,
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {"color": rgb(color)}
                }
            },
            "fields": "pageBackgroundFill",
        }
    }


def rect(page_id, obj_id, x, y, w, h, fill_color):
    return {
        "createShape": {
            "objectId": obj_id,
            "shapeType": "RECTANGLE",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width":  {"magnitude": w, "unit": "EMU"},
                    "height": {"magnitude": h, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": x, "translateY": y,
                    "unit": "EMU",
                },
            },
        }
    }


def fill_shape(obj_id, color):
    return {
        "updateShapeProperties": {
            "objectId": obj_id,
            "shapeProperties": {
                "shapeBackgroundFill": {
                    "solidFill": {"color": rgb(color)}
                },
                "outline": {"propertyState": "NOT_RENDERED"},
            },
            "fields": "shapeBackgroundFill,outline",
        }
    }


def no_outline(obj_id):
    return {
        "updateShapeProperties": {
            "objectId": obj_id,
            "shapeProperties": {
                "outline": {"propertyState": "NOT_RENDERED"},
            },
            "fields": "outline",
        }
    }


# ══════════════════════════════════════════════════════════
# SLIDE BUILDERS
# ══════════════════════════════════════════════════════════

def build_slide_01(page_id):
    """Title: Structure Is the Moat"""
    reqs = [set_bg(page_id, C["dark"])]

    # Section label
    sid = f"{page_id}_section"
    reqs += [
        text_box(page_id, sid, MARGIN_L, 1.2*IN, 5*IN, 0.4*IN),
        insert_text(sid, "SEO WEEK 2026"),
        style_text(sid, 0, 13, 14, bold=True, color=C["sky"]),
    ]

    # Main title
    tid = f"{page_id}_title"
    title = "Structure\nIs the\nMoat"
    reqs += [
        text_box(page_id, tid, MARGIN_L, 1.6*IN, 6*IN, 3*IN),
        insert_text(tid, title),
        style_text(tid, 0, len(title), 80, bold=True, color=C["white"]),
    ]

    # Accent bar
    bid = f"{page_id}_bar"
    reqs += [
        rect(page_id, bid, MARGIN_L, 4.0*IN, 0.6*IN, 0.03*IN, C["sky"]),
        fill_shape(bid, C["sky"]),
        no_outline(bid),
    ]

    # Subtitle
    sub_id = f"{page_id}_sub"
    sub = "What the context explosion means for how AI\nfinds, navigates and ranks your content"
    reqs += [
        text_box(page_id, sub_id, MARGIN_L, 4.15*IN, 6*IN, 0.6*IN),
        insert_text(sub_id, sub),
        style_text(sub_id, 0, len(sub), 16, color=C["gray"]),
    ]

    # Author
    auth_id = f"{page_id}_author"
    auth_txt = "Andrea Volpini · WordLift"
    reqs += [
        text_box(page_id, auth_id, MARGIN_L, 4.8*IN, 5*IN, 0.3*IN),
        insert_text(auth_id, auth_txt),
        style_text(auth_id, 0, len(auth_txt), 13, color=C["gray"]),
    ]

    return reqs


def build_slide_06(page_id):
    """TurboQuant — light mode with big stats"""
    reqs = [set_bg(page_id, C["white"])]

    # Section
    sid = f"{page_id}_section"
    reqs += [
        text_box(page_id, sid, MARGIN_L, 0.4*IN, 6*IN, 0.3*IN),
        insert_text(sid, "ACT II — THE COMPRESSION SOLUTION"),
        style_text(sid, 0, 34, 11, bold=True, color=C["sky"]),
    ]

    # Product name
    pid = f"{page_id}_name"
    reqs += [
        text_box(page_id, pid, MARGIN_L, 0.8*IN, 5*IN, 0.7*IN),
        insert_text(pid, "TurboQuant"),
        style_text(pid, 0, 10, 42, bold=True, color=C["dark"]),
    ]

    # Tagline
    tag_id = f"{page_id}_tag"
    tag = "Geometric compression without information loss"
    reqs += [
        text_box(page_id, tag_id, MARGIN_L, 1.35*IN, 6*IN, 0.3*IN),
        insert_text(tag_id, tag),
        style_text(tag_id, 0, len(tag), 15, color=C["gray"]),
    ]

    # Big stats: 4.5×  8×  0
    stats = [("4.5×", "smaller", 0), ("8×", "faster", 2.8), ("0", "degradation", 5.2)]
    for i, (num, label, x_off) in enumerate(stats):
        n_id = f"{page_id}_stat{i}"
        l_id = f"{page_id}_label{i}"
        x = MARGIN_L + x_off * IN
        num_color = C["sky"] if i < 2 else C["dark"]
        reqs += [
            text_box(page_id, n_id, x, 2.0*IN, 2.5*IN, 1.2*IN),
            insert_text(n_id, num),
            style_text(n_id, 0, len(num), 96, bold=True, color=num_color),
            text_box(page_id, l_id, x, 3.2*IN, 2*IN, 0.3*IN),
            insert_text(l_id, label),
            style_text(l_id, 0, len(label), 15, color=C["gray"]),
        ]

    # Accent bar
    bid = f"{page_id}_bar"
    reqs += [
        rect(page_id, bid, MARGIN_L, 3.8*IN, 0.5*IN, 0.03*IN, C["berry"]),
        fill_shape(bid, C["berry"]),
        no_outline(bid),
    ]

    # Footer
    fid = f"{page_id}_footer"
    foot = "PolarQuant → QJL · Data-oblivious · GPU-native · Zero codebook"
    reqs += [
        text_box(page_id, fid, MARGIN_L, 4.0*IN, 7*IN, 0.3*IN),
        insert_text(fid, foot),
        style_text(fid, 0, len(foot), 13, color=C["gray"]),
    ]

    return reqs


def build_slide_24(page_id):
    """Ghost Citations — light mode with massive berry stat"""
    reqs = [set_bg(page_id, C["white"])]

    # Section
    sid = f"{page_id}_section"
    reqs += [
        text_box(page_id, sid, MARGIN_L, 0.4*IN, 6*IN, 0.3*IN),
        insert_text(sid, "ACT V — THE SEO PLAYBOOK"),
        style_text(sid, 0, 25, 11, bold=True, color=C["sky"]),
    ]

    # Giant 7%
    n_id = f"{page_id}_num"
    reqs += [
        text_box(page_id, n_id, MARGIN_L, 0.7*IN, 4*IN, 2.2*IN),
        insert_text(n_id, "7%"),
        style_text(n_id, 0, 2, 180, bold=True, color=C["berry"]),
    ]

    # Label
    l_id = f"{page_id}_label"
    reqs += [
        text_box(page_id, l_id, MARGIN_L, 2.7*IN, 4*IN, 0.5*IN),
        insert_text(l_id, "Ghost Citations"),
        style_text(l_id, 0, 15, 24, bold=True, color=C["dark"]),
    ]

    # Accent bar
    bid = f"{page_id}_bar"
    reqs += [
        rect(page_id, bid, MARGIN_L, 3.15*IN, 0.5*IN, 0.03*IN, C["berry"]),
        fill_shape(bid, C["berry"]),
        no_outline(bid),
    ]

    # Description
    did = f"{page_id}_desc"
    desc = "AI agents cite content that never appeared in the top-10.\nThey navigated there through entity links — not ranking signals."
    reqs += [
        text_box(page_id, did, MARGIN_L, 3.35*IN, 7*IN, 0.6*IN),
        insert_text(did, desc),
        style_text(did, 0, len(desc), 14, color=C["gray"]),
    ]

    # Two cards at bottom
    cards = [
        ("Rankings ≠ AI citations", C["berry"], 0),
        ("Navigation graph = new signal", C["sky"], 4.5),
    ]
    for i, (txt, color, x_off) in enumerate(cards):
        # Top border line
        r_id = f"{page_id}_cbar{i}"
        reqs += [
            rect(page_id, r_id, MARGIN_L + x_off*IN, 4.4*IN, 3.8*IN, 0.025*IN, color),
            fill_shape(r_id, color),
            no_outline(r_id),
        ]
        # Card text
        c_id = f"{page_id}_card{i}"
        reqs += [
            text_box(page_id, c_id, MARGIN_L + x_off*IN, 4.5*IN, 3.8*IN, 0.3*IN),
            insert_text(c_id, txt),
            style_text(c_id, 0, len(txt), 14, bold=True, color=C["dark"]),
        ]

    return reqs


def main():
    print("Authenticating...")
    creds = auth()
    service = build("slides", "v1", credentials=creds)

    # Create test presentation
    print("Creating test presentation...")
    pres = service.presentations().create(
        body={"title": "Structure Is the Moat — NATIVE TEST"}
    ).execute()
    pres_id = pres["presentationId"]
    print(f"  ✓ https://docs.google.com/presentation/d/{pres_id}/edit")

    # Get first slide, add 2 more
    first_id = pres["slides"][0]["objectId"]
    service.presentations().batchUpdate(
        presentationId=pres_id,
        body={"requests": [
            {"createSlide": {"objectId": "slide_06", "insertionIndex": 1, "slideLayoutReference": {"predefinedLayout": "BLANK"}}},
            {"createSlide": {"objectId": "slide_24", "insertionIndex": 2, "slideLayoutReference": {"predefinedLayout": "BLANK"}}},
        ]}
    ).execute()

    # Build all 3 slides
    reqs = []
    reqs += build_slide_01(first_id)
    reqs += build_slide_06("slide_06")
    reqs += build_slide_24("slide_24")

    # Submit
    print(f"  Applying {len(reqs)} requests...")
    service.presentations().batchUpdate(
        presentationId=pres_id,
        body={"requests": reqs}
    ).execute()

    print(f"\n✓ Test ready! Open:")
    print(f"  https://docs.google.com/presentation/d/{pres_id}/edit")


if __name__ == "__main__":
    main()

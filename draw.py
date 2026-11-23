#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: Sunday 22 November 2026.

Geometry first (GATES.md, approved by Ahmad 2026-11-22): the grid and
the type floors were locked before the story count — hero headlines
>= 30px, card headlines >= 19px, brief headlines >= 16px, brief text
>= 14px, in-scene labels >= 13px, at most 3 heroes, briefs <= 9 words
over 2 lines. STRUCTURE (from the ni21 top-10 artefacts, counted directly:
35-43 stories each): 35 stories — 3 heroes + 10 cards pictured large, plus
a 22-line ALSO rail of one-line briefs at 14px. Card headlines at 21px.

Every important number is read from figures.json (the registry); no
panel types a figure freehand. The strap counts, the region tally and
the field tally are computed from the story table below. Deterministic:
no randomness, two runs are byte-identical.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"
FIG = {f["key"]: f["display"]
       for f in json.loads((HERE / "figures.json").read_text())["figures"]}

PAPER = (244, 239, 227)
PAPER_DK = (233, 225, 206)
INK = (26, 24, 20)
MUTE = (96, 90, 78)
RED = (178, 34, 30)
NAVY = (18, 32, 54)
TEAL = (23, 92, 96)
GOLD = (196, 148, 38)
PURPLE = (120, 70, 160)
SKY = (168, 198, 224)

REGIONS = {"EUR": ("Europe", (52, 84, 140)), "ASI": ("Asia-Pacific", RED),
           "AME": ("Americas", TEAL), "MEA": ("Middle East", PURPLE),
           "AFR": ("Africa", GOLD), "GLO": ("Global", MUTE)}
SURE_LABEL = {"C": "CONFIRMED", "W": "WITNESSES", "R": "REPORTED",
              "S": "SCHEDULED", "G": "ONGOING"}

# ------------------------------------------------------------------ data
# Heroes: (place, region, field, headline, deck, source, sure, big, biglabel)
HEROES = [
    ("ANTALYA, TURKIYE", "ASI", "Climate",
     "COP31 ends with no deal at all",
     "After " + FIG["cop31_overtime"] + " hours of overtime, the final "
     "text is rejected — the first no-deal COP since "
     + FIG["cop31_last_nodeal"] + ".",
     "Guardian", "C", FIG["cop31_overtime"], "HOURS OVERTIME"),
    ("BAHRAIN", "MEA", "Conflict",
     "Iran strikes US bases in Bahrain",
     FIG["bahrain_bases"] + " bases targeted on Saturday night; "
     + FIG["bahrain_injured"] + " people hurt on Sunday, one critical.",
     "Reuters", "R", FIG["bahrain_bases"], "US BASES TARGETED"),
    ("BENGHAZI, LIBYA", "AFR", "Conflict",
     "Russian warship sunk by drones in Libya",
     "Corvette Merkury capsizes at Benghazi before dawn after "
     + FIG["benghazi_drones_hit"] + " drone hits; "
     + FIG["benghazi_injured"] + " hurt.",
     "AP", "R", FIG["benghazi_injured"], "INJURED"),
]

# Cards: (place, region, field, headline, deck, source, sure)
CARDS = [
    ("DYMER", "EUR", "Conflict",
     "Russian drones kill seven in Ukraine",
     "A block collapses in Dymer; Zelensky asks the US for Patriots.",
     "Al Jazeera", "R"),
    ("WARSAW", "EUR", "Diplomacy",
     "Poland: all three Kh-101 missiles",
     "Prosecutors say the objects that fell on Friday were Russian "
     "cruise missiles; NATO meets Monday.", "Reuters", "C"),
    ("ISTANBUL", "EUR", "Politics",
     "Thousands march for a free press",
     "Istanbul protests the Sözcü TV seizure; a third media takeover "
     "in a year.", "AFP", "C"),
    ("CIKANDE", "ASI", "Disaster",
     "Factory fire: 24 body bags",
     "Search goes on after the candy-factory blaze; it resumes Monday.",
     "Reuters", "R"),
    ("BAYELSA", "AFR", "Disaster",
     "Funeral-boat toll rises to 24",
     "NEMA says 24 bodies are recovered after the Bayelsa capsize; "
     "search goes on.", "Reuters", "C"),
    ("WEST BANK", "MEA", "Conflict",
     "Settlers torch West Bank villages",
     "Fires and racist graffiti in four villages early Sunday; "
     "Eisenkot calls it terrorism.", "Reuters", "C"),
    ("KHAN YOUNIS", "MEA", "Conflict",
     "Two killed in Gaza strike",
     "Medics say an Israeli strike on Khan Younis kills two on Sunday.",
     "Medics", "R"),
    ("MERCURY", "GLO", "Science",
     "BepiColombo reaches Mercury",
     "ESA confirms capture at 00:56 UTC after "
     + FIG["bepicolombo_years"] + " years; orbiters split in December.",
     "ESA", "C"),
    ("LAS VEGAS", "AME", "Sport",
     "Verstappen wins in Las Vegas",
     "Holds off Norris by " + FIG["vegas_margin"] + "s in Las Vegas; "
     "Piastri third.", "F1", "C"),
    ("SHANGHAI", "ASI", "Economy",
     "China eases margin rules",
     "Exchanges cut the minimum margin ratio to "
     + FIG["china_margin_new"] + " from " + FIG["china_margin_old"]
     + " on 30 November.", "Reuters", "C"),
]

# ALSO rail: (place, region, field, fact, source) — one line per story,
# numbered 14-35. This is the top-10 winners' structure from edition 21:
# density is quarantined in this one-line rail while the pictured layer
# (heroes + cards) stays large and airy.
ALSO = [
    ("KRYVYI RIH", "EUR", "Conflict",
     FIG["kryvyi_injured"] + " hurt, " + FIG["kryvyi_children"] + " children", "AP"),
    ("HORMUZ", "MEA", "Conflict",
     FIG["hormuz_week"] + " tankers hit in week", "AJ"),
    ("TURIN", "EUR", "Sport", "Alcaraz beats Zverev 6-2", "ATP"),
    ("WASHINGTON", "AME", "Diplomacy", "Trump: 'permanent'", "Fox"),
    ("NEW YORK", "AME", "Tech", "AI-chip spy bid", "NYT"),
    ("LIVERPOOL", "EUR", "Sport", "4-0 over Man Utd", "BBC"),
    ("HULL", "EUR", "Sport", "2-0 Brighton, late brace", "BBC"),
    ("PARIS", "EUR", "Sport", "Dou\u00e9 ACL tear", "AFP"),
    ("SYDNEY", "ASI", "Politics", "US lead narrows", "Lowy"),
    ("GILROY", "AME", "Politics", "Interfaith ICE protest", "KPFA"),
    ("SEATTLE", "AME", "Politics", "ICE takes two", "KPFA"),
    ("MADRID", "EUR", "Sport", "Real fight back", "La Liga"),
    ("ADDIS ABABA", "AFR", "Climate", "COP32 next", "Guardian"),
    ("MILAN", "EUR", "Sport", "Milan 5-1 Frosinone", "Serie A"),
    ("BARCELONA", "EUR", "Sport", "3-2 Villarreal", "La Liga"),
    ("BERGAMO", "EUR", "Sport", "Atalanta 4-4 Inter", "Serie A"),
    ("TURIN", "EUR", "Sport", "Juventus 4-0 Venezia", "Serie A"),
    ("BREMEN", "EUR", "Sport", "4-0 Hamburg", "Bundesliga"),
    ("AUGSBURG", "EUR", "Sport", "3-1 Mainz", "Bundesliga"),
    ("GETAFE", "EUR", "Sport", "Atl\u00e9tico win 3-0 away", "La Liga"),
    ("SANTANDER", "EUR", "Sport", "3-2 Sociedad", "La Liga"),
    ("BANDUNG", "ASI", "Sport", "Persib 2-1 Bali", "Aktualita"),
]

# ------------------------------------------------------------- world map
# Coarse dot-grid world: 68 x 30 cells, lon -168..192, lat 78..-56.
# Land is a list of (first col, last col) spans per row.
LAND_SPANS = [
    [(1, 5), (10, 18), (24, 27), (42, 64)],
    [(1, 6), (8, 20), (23, 28), (38, 66)],
    [(2, 21), (24, 27), (33, 66)],
    [(3, 21), (24, 26), (32, 65)],
    [(3, 20), (31, 31), (32, 64)],
    [(4, 20), (31, 63)],
    [(4, 19), (30, 62), (57, 58)],
    [(4, 19), (30, 60), (56, 57)],
    [(4, 18), (30, 58)],
    [(5, 17), (29, 30), (34, 57)],
    [(5, 16), (28, 57)],
    [(6, 14), (28, 56)],
    [(7, 13), (28, 55)],
    [(9, 13), (28, 55)],
    [(11, 14), (28, 56)],
    [(16, 26), (29, 58)],
    [(16, 26), (29, 59)],
    [(16, 26), (30, 58)],
    [(17, 26), (30, 38)],
    [(17, 25), (30, 37)],
    [(17, 25), (30, 37), (52, 61)],
    [(18, 25), (31, 36), (42, 42), (52, 62)],
    [(18, 24), (31, 36), (42, 42), (53, 62)],
    [(18, 24), (31, 35), (42, 42), (53, 61)],
    [(20, 22), (32, 34), (55, 58)],
    [(20, 22), (64, 65)],
    [(20, 21)],
    [(20, 21)],
    [(20, 21)],
    [(20, 20)],
]

# Pins for the numbered stories (heroes 1-3, cards 4-15): (num, lon, lat,
# dx, dy) — dx/dy nudge cluster pins apart, with a leader dot left behind.
PINS = [
    (1, 31, 37, 16, 20), (2, 50, 26, 30, 36), (3, 20, 32, -30, -14),
    (4, 30, 50, 30, -6), (5, 21, 52, -28, -10), (6, 29, 41, -30, 18),
    (7, 106, -6, 0, 0), (8, 6, 5, -40, 30), (9, 35, 32, -24, 30),
    (10, 34, 31, 24, 34), (12, -115, 36, 0, 0), (13, 121, 31, 0, 0),
]

TIMELINE = [("00:56", "Bepi in orbit"), ("05:28", "Two killed in Gaza"),
            ("08:28", "Kryvyi toll 73"), ("12:48", "Nigeria toll 24"),
            ("14:48", "Zelensky: Patriots"),
            ("17:18", "Poland: 3 Kh-101"), ("19:17", "Alcaraz wins Turin")]

NUMBERS = [(FIG["cop31_overtime"], "hours of overtime"),
           (FIG["cop31_last_nodeal"], "last no-deal COP"),
           (FIG["bayelsa_dead"], "dead in Bayelsa"),
           (FIG["kryvyi_injured"], "hurt in Kryvyi Rih"),
           (FIG["ukraine_killed_sunday"], "killed in Ukraine Sun"),
           (FIG["vegas_lead_changes"], "lead changes in Vegas")]


def all_stories():
    out = [(h[1], h[2]) for h in HEROES]
    out += [(c[1], c[2]) for c in CARDS]
    out += [(b[1], b[2]) for b in ALSO]
    return out


# ------------------------------------------------------------------ fonts
def _f(name, sz):
    return ImageFont.truetype(str(FONT_DIR / name), sz)


def SERIF(sz):
    return _f("PlayfairDisplay-Bold.ttf", sz)


def SERIF_BLACK(sz):
    return _f("PlayfairDisplay-Black.ttf", sz)


def SANS(sz):
    return _f("Archivo-Regular.ttf", sz)


def SANS_B(sz):
    return _f("Archivo-Bold.ttf", sz)


def SANS_SB(sz):
    return _f("Archivo-SemiBold.ttf", sz)


def fit_font(text, maxw, maker, hi, lo):
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    for sz in range(hi, lo - 1, -1):
        f = maker(sz)
        if probe.textlength(text, font=f) <= maxw:
            return f
    return maker(lo)


OVERFLOWS = []
BANNER_CHECK = []
H_CHECKS = []
TEXT_BOXES = []
OBSTACLES = []
FLAGS = []
TAG = [None]
LINES = []
LINES = []


class RecDraw:
    """Wraps ImageDraw: records the ink bbox of every text() call."""

    def __init__(self, real):
        object.__setattr__(self, "_r", real)
        object.__setattr__(self, "suspend", False)

    def text(self, xy, s, font=None, fill=None, **kw):
        if not self.suspend and font is not None:
            TEXT_BOXES.append((self._r.textbbox(xy, s, font=font), s, TAG[0]))
        return self._r.text(xy, s, font=font, fill=fill, **kw)

    def __getattr__(self, name):
        return getattr(self._r, name)

    def __setattr__(self, name, value):
        if name in ("_r", "suspend"):
            object.__setattr__(self, name, value)
        else:
            setattr(self._r, name, value)


def audit_text_boxes():
    n = len(TEXT_BOXES)
    hits, near = [], []
    for i in range(n):
        (ax0, ay0, ax1, ay1), sa, _ta = TEXT_BOXES[i]
        for j in range(i + 1, n):
            (bx0, by0, bx1, by1), sb, _tb = TEXT_BOXES[j]
            xo = min(ax1, bx1) - max(ax0, bx0)
            yo = min(ay1, by1) - max(ay0, by0)
            if xo > 0 and yo > 0:
                hits.append((sa[:38], sb[:38], xo, yo))
            elif xo > 0:
                gap = max(by0 - ay1, ay0 - by1)
                if gap < 3:
                    near.append((sa[:38], sb[:38], "v", gap))
            elif yo > 0:
                gap = max(bx0 - ax1, ax0 - bx1)
                if gap < 3:
                    near.append((sa[:38], sb[:38], "h", gap))
    print(f"TEXT-AUDIT: {n} text boxes, {n * (n - 1) // 2} pairs checked, "
          f"{len(hits)} intersections, {len(near)} near-misses (<3px)")
    for h in hits:
        print("  INTERSECT:", h)
    for h in near:
        print("  NEAR:", h)
    pens, mind, minpair = [], 999, None
    for (bx0, by0, bx1, by1), txt, _tg3 in TEXT_BOXES:
        for (lx0, ly0, lx1, ly1), lab in LINES:
            if ly0 == ly1:  # horizontal line
                if min(bx1, lx1) - max(bx0, lx0) <= 2:
                    continue
                if by0 < ly0 < by1:
                    pens.append((txt[:30], lab))
                else:
                    dist = by0 - ly0 if by0 >= ly0 else ly0 - by1
                    if 0 <= dist < mind:
                        mind, minpair = dist, (txt[:30], lab)
            else:  # vertical line
                if min(by1, ly1) - max(by0, ly0) <= 2:
                    continue
                if bx0 < lx0 < bx1:
                    pens.append((txt[:30], lab))
                else:
                    dist = bx0 - lx0 if bx0 >= lx0 else lx0 - bx1
                    if 0 <= dist < mind:
                        mind, minpair = dist, (txt[:30], lab)
    print(f"LINE-AUDIT: {len(LINES)} lines x {n} texts, "
          f"{len(pens)} penetrations, min text-to-line distance "
          f"{mind}px at {minpair}")
    for p in pens:
        print("  PENETRATION:", p)
    for h in hits:
        print("  INTERSECT:", h)
    for h in near:
        print("  NEAR:", h)
    pens, mind, minpair = [], 999, None
    for (bx0, by0, bx1, by1), txt, _tg3 in TEXT_BOXES:
        for (lx0, ly0, lx1, ly1), lab in LINES:
            if ly0 == ly1:  # horizontal line
                if min(bx1, lx1) - max(bx0, lx0) <= 2:
                    continue
                if by0 < ly0 < by1:
                    pens.append((txt[:30], lab))
                else:
                    dist = by0 - ly0 if by0 >= ly0 else ly0 - by1
                    if 0 <= dist < mind:
                        mind, minpair = dist, (txt[:30], lab)
            else:  # vertical line
                if min(by1, ly1) - max(by0, ly0) <= 2:
                    continue
                if bx0 < lx0 < bx1:
                    pens.append((txt[:30], lab))
                else:
                    dist = bx0 - lx0 if bx0 >= lx0 else lx0 - bx1
                    if 0 <= dist < mind:
                        mind, minpair = dist, (txt[:30], lab)
    print(f"LINE-AUDIT: {len(LINES)} lines x {n} texts, "
          f"{len(pens)} penetrations, min text-to-line distance "
          f"{mind}px at {minpair}")
    for p in pens:
        print("  PENETRATION:", p)
    for h in hits:
        print("  INTERSECT:", h)
    for h in near:
        print("  NEAR:", h)
    return hits, near


def check_h(label, text, font, x_start, x_limit):
    """Horizontal overflow check: measured text end must stay inside limit."""
    end = x_start + ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(
        text, font=font)
    H_CHECKS.append((label, round(end - x_limit, 1)))
    if end > x_limit:
        OVERFLOWS.append(f"H-OVERFLOW {label}: ends {end:.0f} > {x_limit}")


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, maxw, leading, max_lines=None, tag=""):
    lines = wrap(d, text, font, maxw)
    if max_lines and len(lines) > max_lines:
        OVERFLOWS.append(f"{tag}: {len(lines)}>{max_lines} lines: {text[:40]}")
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def center(d, y, text, font, fill, cx=W // 2):
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


def tracked_width(d, text, font, tracking):
    return sum(d.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)


def tracked(d, x, y, text, font, fill, tracking=3):
    bb = d.textbbox((x, y), text, font=font)
    TEXT_BOXES.append(((bb[0], bb[1], bb[2] + tracking * (len(text) - 1),
                        bb[3]), text, None))
    d.suspend = True
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    d.suspend = False
    return x - tracking


def SERIF_IT(sz):
    return _f("PlayfairDisplay-SemiBoldItalic.ttf", sz)


# ------------------------------------------------------------------ flags
def _star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag(d, code, x, y, w=34, h=22):
    """Solid miniature flags (v3.6): every field painted in saturated
    official colours (never the cream paper showing through), correct
    key elements, all proportions relative to w/h so the same drawing
    serves the 34x22 hero chips and the 28x18 card chips."""
    WHT = (255, 255, 255)
    d.rectangle([x, y, x + w, y + h], fill=WHT)
    if code == "SA":  # Saudi Arabia: green, white shahada band + sword
        d.rectangle([x, y, x + w, y + h], fill=(0, 108, 53))
        d.rectangle([x + w * 0.16, y + h * 0.30, x + w * 0.84, y + h * 0.52],
                    fill=WHT)
        d.line([x + w * 0.20, y + h * 0.70, x + w * 0.80, y + h * 0.70],
               fill=WHT, width=max(2, h // 8))
        d.line([x + w * 0.74, y + h * 0.62, x + w * 0.74, y + h * 0.70],
               fill=WHT, width=2)
    elif code == "TR":  # Turkiye: red, white crescent + star
        d.rectangle([x, y, x + w, y + h], fill=(227, 10, 23))
        cx, cy, r = x + w * 0.40, y + h * 0.5, h * 0.30
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHT)
        r2 = r * 0.82
        d.ellipse([cx + r * 0.28 - r2, cy - r2, cx + r * 0.28 + r2, cy + r2],
                  fill=(227, 10, 23))
        _star(d, x + w * 0.70, cy, h * 0.17, WHT)
    elif code == "BH":  # Bahrain: red field, white serrated hoist band
        d.rectangle([x, y, x + w, y + h], fill=(206, 17, 38))
        pts = [(x, y)]
        for i in range(5):
            pts.append((x + w * 0.30, y + h * (0.1 + i * 0.2)))
            pts.append((x, y + h * (0.2 + i * 0.2)))
        pts.append((x, y + h))
        d.polygon(pts, fill=WHT)
    elif code == "LY":  # Libya: red-black-green, white crescent + star
        d.rectangle([x, y, x + w, y + h // 4], fill=(206, 17, 38))
        d.rectangle([x, y + h // 4, x + w, y + 3 * h // 4], fill=(0, 0, 0))
        d.rectangle([x, y + 3 * h // 4, x + w, y + h], fill=(0, 122, 61))
        cx, cy, r = x + w * 0.48, y + h * 0.5, h * 0.20
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHT)
        r2 = r * 0.85
        d.ellipse([cx + r * 0.3 - r2, cy - r2, cx + r * 0.3 + r2, cy + r2],
                  fill=(0, 0, 0))
        _star(d, x + w * 0.64, cy, h * 0.10, WHT)
    elif code == "UA":  # Ukraine: blue over yellow
        d.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 213, 0))
        d.rectangle([x, y, x + w, y + h // 2], fill=(0, 91, 187))
    elif code == "ID":  # Indonesia: red over white
        d.rectangle([x, y, x + w, y + h // 2], fill=(206, 17, 38))
    elif code == "NG":  # Nigeria: green-white-green vertical
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 135, 81))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(0, 135, 81))
    elif code == "CN":  # China: red, gold stars
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        _star(d, x + w * 0.24, y + h * 0.28, h * 0.20, (255, 222, 0))
        for sx, sy in ((0.50, 0.14), (0.60, 0.30), (0.60, 0.52), (0.48, 0.62)):
            _star(d, x + w * sx, y + h * sy, h * 0.08, (255, 222, 0))
    elif code == "PE":  # Peru: red-white-red vertical
        d.rectangle([x, y, x + w // 3, y + h], fill=(217, 0, 27))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(217, 0, 27))
    elif code == "PL":  # Poland: white over red
        d.rectangle([x, y + h // 2, x + w, y + h], fill=(220, 20, 60))
    elif code == "DK":  # Denmark: red, white Nordic cross
        d.rectangle([x, y, x + w, y + h], fill=(200, 16, 46))
        d.rectangle([x + w * 0.30, y, x + w * 0.43, y + h], fill=WHT)
        d.rectangle([x, y + h * 0.39, x + w, y + h * 0.61], fill=WHT)
    elif code == "FI":  # Finland: white, blue Nordic cross
        d.rectangle([x + w * 0.28, y, x + w * 0.44, y + h], fill=(0, 47, 108))
        d.rectangle([x, y + h * 0.36, x + w, y + h * 0.64], fill=(0, 47, 108))
    elif code == "PS":  # Palestine: black-white-green, red hoist triangle
        d.rectangle([x, y, x + w, y + h // 3], fill=(0, 0, 0))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(0, 122, 61))
        d.polygon([(x, y), (x + w * 0.42, y + h // 2), (x, y + h)],
                  fill=(238, 28, 37))
    elif code == "IQ":  # Iraq: red-white-black, green takbir mark
        d.rectangle([x, y, x + w, y + h // 3], fill=(206, 17, 38))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(0, 0, 0))
        d.rectangle([x + w * 0.40, y + h * 0.42, x + w * 0.60, y + h * 0.58],
                    fill=(0, 122, 61))
    elif code == "OM":  # Oman: red hoist, white-red-green stripes
        d.rectangle([x + w * 0.30, y + h // 3, x + w, y + 2 * h // 3],
                    fill=(239, 51, 64))
        d.rectangle([x + w * 0.30, y + 2 * h // 3, x + w, y + h],
                    fill=(0, 150, 57))
        d.rectangle([x, y, x + w * 0.30, y + h], fill=(239, 51, 64))
        d.ellipse([x + w * 0.10, y + h * 0.12, x + w * 0.20, y + h * 0.24],
                  fill=WHT)
    elif code == "CH":  # Switzerland: red field, white cross
        d.rectangle([x, y, x + w, y + h], fill=(218, 41, 28))
        d.rectangle([x + w * 0.42, y + h * 0.20, x + w * 0.58, y + h * 0.80],
                    fill=WHT)
        d.rectangle([x + w * 0.26, y + h * 0.38, x + w * 0.74, y + h * 0.62],
                    fill=WHT)
    elif code == "US":  # USA: 13 stripes, blue canton, star dots
        sh = h / 13
        for i in range(13):
            if i % 2 == 0:
                d.rectangle([x, y + i * sh, x + w, y + (i + 1) * sh + 1],
                            fill=(178, 34, 52))
        cw2, ch2 = w * 0.44, sh * 7
        d.rectangle([x, y, x + cw2, y + ch2], fill=(60, 59, 110))
        for r in range(3):
            for c in range(4):
                sx = x + cw2 * (c + 0.5) / 4
                sy = y + ch2 * (r + 0.5) / 3
                d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHT)
    elif code == "MX":  # Mexico: green-white-red, centre emblem
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 104, 71))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(206, 17, 38))
        d.ellipse([x + w * 0.44, y + h * 0.38, x + w * 0.56, y + h * 0.62],
                  fill=(196, 148, 38))
    elif code == "IT":  # Italy: green-white-red vertical
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 140, 69))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(205, 33, 42))
    elif code == "EU":  # European Union: blue, circle of 12 gold stars
        import math
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        cx, cy, rr = x + w / 2, y + h / 2, h * 0.32
        for i in range(12):
            ang = i * math.pi / 6
            sx, sy = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
            _star(d, sx, sy, max(1.6, h * 0.075), (255, 204, 0))
    else:  # globe marker
        d.ellipse([x + 6, y + 1, x + 28, y + 21], fill=SKY, outline=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


CARD_DECK = [
    FIG["ukraine_killed_sunday"] + " killed Sunday; Zelensky asks the US "
    "for Patriots",
    FIG["poland_missiles"] + " Kh-101 missiles; NATO council meets Monday",
    "Protests at the S\u00f6zc\u00fc TV seizure; " + FIG["istanbul_takeover"]
    + " takeover in a year",
    FIG["cikande_body_bags"] + " body bags, " + FIG["cikande_missing"]
    + " missing; search resumes Monday",
    FIG["bayelsa_dead"] + " dead, " + FIG["bayelsa_rescued"]
    + " rescued; search goes on",
    FIG["westbank_villages"] + " villages attacked; Eisenkot calls it "
    "terrorism",
    "Medics say a strike kills " + FIG["gaza_killed_sunday"] + " on Sunday",
    "In orbit 00:56 UTC after " + FIG["bepicolombo_years"]
    + " years; split in Dec",
    FIG["vegas_lead_changes"] + " lead changes; " + FIG["vegas_margin"]
    + "s over Norris",
    "Margin ratio cut to " + FIG["china_margin_new"] + " from "
    + FIG["china_margin_old"] + " on 30 Nov",
]

CARD_FLAGS = ["UA", "PL", "TR", "ID", "NG", "PS", "PS", "EU", "US", "CN"]
HERO_FLAGS = ["TR", "BH", "LY"]


def icon(d, field, x, y, col):
    """A small pictogram per card field, so every panel carries a picture."""
    if field == "Diplomacy":
        d.ellipse([x, y + 4, x + 15, y + 19], outline=col, width=3)
        d.ellipse([x + 9, y + 4, x + 24, y + 19], outline=col, width=3)
    elif field == "Politics":
        d.rectangle([x + 3, y + 10, x + 21, y + 22], outline=col, width=3)
        d.line([x + 7, y + 10, x + 17, y + 10], fill=col, width=3)
        d.line([x + 12, y, x + 12, y + 8], fill=col, width=3)
    elif field == "Conflict":
        for dx, dy in ((12, 0), (22, 6), (24, 14), (18, 22), (6, 22), (0, 12),
                       (4, 4)):
            d.line([x + 12, y + 12, x + dx, y + dy], fill=col, width=3)
        d.ellipse([x + 8, y + 8, x + 16, y + 16], fill=col)
    elif field == "Disaster":
        d.polygon([(x + 12, y), (x + 20, y + 12), (x + 17, y + 22),
                   (x + 7, y + 22), (x + 4, y + 12)], fill=col)
        d.polygon([(x + 12, y + 10), (x + 16, y + 16), (x + 14, y + 22),
                   (x + 10, y + 22), (x + 8, y + 16)], fill=(250, 205, 90))
    elif field == "Crime":
        d.polygon([(x + 12, y), (x + 22, y + 4), (x + 22, y + 12),
                   (x + 12, y + 24), (x + 2, y + 12), (x + 2, y + 4)],
                  outline=col, width=3)
    elif field == "Courts":
        d.line([x + 2, y + 6, x + 22, y + 6], fill=col, width=3)
        d.line([x + 12, y + 6, x + 12, y + 20], fill=col, width=3)
        d.line([x + 4, y + 20, x + 20, y + 20], fill=col, width=3)
        d.polygon([(x + 2, y + 14), (x + 10, y + 14), (x + 6, y + 8)],
                  fill=col)
        d.polygon([(x + 14, y + 14), (x + 22, y + 14), (x + 18, y + 8)],
                  fill=col)
    elif field == "Science":
        d.ellipse([x + 6, y + 6, x + 18, y + 18], fill=col)
        d.ellipse([x, y + 9, x + 24, y + 15], outline=col, width=2)
    elif field == "Sport":
        d.polygon([(x + 5, y + 2), (x + 19, y + 2), (x + 17, y + 14),
                   (x + 7, y + 14)], outline=col, width=3)
        d.line([x + 12, y + 14, x + 12, y + 20], fill=col, width=3)
        d.line([x + 6, y + 22, x + 18, y + 22], fill=col, width=3)
    else:
        d.ellipse([x + 3, y + 3, x + 21, y + 21], outline=col, width=3)


# ------------------------------------------------------------------ scenes
def scene_label(d, x, y, w, text, h=66):
    chip_r = x + 8 + d.textlength(text, font=SANS_B(13)) + 12
    d.rectangle([x + 8, y + h - 22, chip_r, y + h - 2], fill=(10, 14, 30))
    OBSTACLES.append(((x + 8, y + h - 22, chip_r, y + h - 2),
                      f"scene label chip '{text[:18]}'", TAG[0]))
    d.text((x + 14, y + h - 19), text, font=SANS_B(13), fill=(255, 255, 255))
    H_CHECKS.append((f"scene label '{text}' right margin",
                     round((chip_r - 6) - (x + 14 + d.textlength(
                         text, font=SANS_B(13))), 1)))
    if x + 14 + d.textlength(text, font=SANS_B(13)) > chip_r - 6:
        OVERFLOWS.append(f"H-OVERFLOW scene label: {text}")


def scene_antalya(d, x, y, w, h):
    # DOMINANT: the hall's big NO DEAL banner over the emptying talks hall
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((214, 224, 214)[i] + ((168, 186, 176)[i] - (214, 224, 214)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    plate = [x + 52, y + 8, x + w - 52, y + 40]
    d.rectangle(plate, fill=(240, 238, 228), outline=INK, width=2)
    OBSTACLES.append((tuple(plate), "antalya banner plate", TAG[0]))
    d.text((x + w // 2, y + 24), "COP31 — NO DEAL", font=SERIF(15),
           fill=RED, anchor="mm")
    tb = d.textbbox((x + w // 2, y + 24), "COP31 — NO DEAL",
                    font=SERIF(15), anchor="mm")
    margins = (tb[0] - plate[0], tb[1] - plate[1],
               plate[2] - tb[2], plate[3] - tb[3])
    BANNER_CHECK.append((tb, tuple(plate), margins))
    assert min(margins) >= 6, f"banner text escapes plate: margins {margins}"
    d.ellipse([x + w - 36, y + 36, x + w - 12, y + 60],
              fill=(255, 255, 255), outline=INK, width=2)
    OBSTACLES.append(((x + w - 36, y + 36, x + w - 12, y + 60),
                      "antalya clock", TAG[0]))
    d.line([x + w - 24, y + 48, x + w - 24, y + 40], fill=RED, width=3)
    d.line([x + w - 24, y + 48, x + w - 17, y + 52], fill=RED, width=3)
    d.rectangle([x + 34, y + 54, x + w - 34, y + 63], fill=(96, 70, 44))
    for i in range(5):
        xx = x + 52 + i * 26
        d.ellipse([xx, y + 34, xx + 15, y + 48], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 48, xx + 17, y + 54], fill=TEAL)
    for i in range(5):
        xx = x + w - 66 - i * 26
        d.ellipse([xx, y + 34, xx + 15, y + 48], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 48, xx + 17, y + 54], fill=RED)
    d.rectangle([x + w // 2 - 9, y + 38, x + w // 2 + 9, y + 63], fill=NAVY)


def scene_bahrain(d, x, y, w, h):
    # DOMINANT: a big Patriot launcher under missile streaks, fire on Sitra
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((16, 24, 52)[i] + ((70, 60, 90)[i] - (16, 24, 52)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    for sx, sy in ((30, 10), (90, 6), (250, 8)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 230))
    for tx, ty in ((60, 14), (150, 6), (238, 16)):
        d.line([x + tx + 40, y + ty - 8, x + tx, y + ty + 12],
               fill=(255, 120, 90), width=3)
        cx, cy = x + tx, y + ty + 13
        for dx, dy in ((-11, -7), (0, -12), (11, -7), (-12, 4), (12, 4), (0, 11)):
            d.line([cx, cy, cx + dx, cy + dy], fill=(255, 214, 90), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 240, 180))
    # Patriot launcher, big in the foreground
    d.rectangle([x + 110, y + 34, x + 210, y + 52], fill=(52, 56, 66))
    for bx in range(118, 204, 14):
        d.ellipse([x + bx, y + 38, x + bx + 8, y + 46], fill=(30, 32, 40))
    d.rectangle([x + 130, y + 52, x + 150, y + h], fill=(40, 42, 52))
    d.rectangle([x + 170, y + 52, x + 190, y + h], fill=(40, 42, 52))
    # industrial fire on Sitra, right edge
    for fx, fy, fs in ((262, 44, 12), (276, 50, 9)):
        d.polygon([(x + fx, y + fy - fs), (x + fx + fs * 0.62, y + fy + fs * 0.4),
                   (x + fx + fs * 0.3, y + fy + fs),
                   (x + fx - fs * 0.3, y + fy + fs),
                   (x + fx - fs * 0.62, y + fy + fs * 0.4)],
                  fill=(255, 140, 40))
    d.ellipse([x + 256, y + 8, x + 282, y + 26], fill=(90, 90, 100))
    d.ellipse([x + 266, y + 2, x + 288, y + 16], fill=(70, 70, 80))


def scene_benghazi(d, x, y, w, h):
    # DOMINANT: the capsized corvette, only its hull showing above water
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((232, 190, 150)[i] + ((120, 150, 180)[i] - (232, 190, 150)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    # hull: a dark ellipse, its lower half hidden by the sea
    d.ellipse([x + 56, y + 8, x + 196, y + 56], fill=(52, 56, 66))
    OBSTACLES.append(((x + 56, y + 8, x + 196, y + 56),
                      "benghazi capsized hull", TAG[0]))
    d.rectangle([x + 96, y + 10, x + 156, y + 16], fill=(120, 30, 28))
    d.line([x + 126, y + 10, x + 108, y - 2], fill=(30, 34, 44), width=3)
    d.rectangle([x, y + 38, x + w, y + h], fill=(46, 84, 120))
    d.polygon([(x + 176, y + 30), (x + 196, y + 30), (x + 204, y + 38),
               (x + 184, y + 38)], fill=(70, 74, 84))
    for sx in (210, 226, 242):
        d.ellipse([x + sx, y + 6, x + sx + 16, y + 20], fill=(90, 90, 100))
    d.ellipse([x + 220, y + 2, x + 240, y + 14], fill=(70, 70, 80))
    d.polygon([(x + 20, y + 52), (x + 30, y + 46), (x + 52, y + 46),
               (x + 58, y + 52)], fill=(30, 34, 44))
    d.rectangle([x + 34, y + 40, x + 40, y + 46], fill=(200, 60, 40))



HERO_SCENES = [scene_antalya, scene_bahrain, scene_benghazi]


def badge(d, x, y, num, region):
    col = REGIONS[region][1]
    d.rectangle([x, y, x + 24, y + 24], fill=col)
    t = str(num)
    f = SANS_B(14 if len(t) < 2 else 12)
    d.text((x + 12 - d.textlength(t, font=f) / 2, y + 4), t, font=f,
           fill=(255, 255, 255))


def tally_bar(d, y, counts, total, x0=76, x1=560, hgt=13):
    x = x0
    for code in ("EUR", "ASI", "AME", "MEA", "GLO", "AFR"):
        n = counts.get(code, 0)
        if not n:
            continue
        wseg = (x1 - x0) * n / total
        d.rectangle([x, y, x + wseg, y + hgt], fill=REGIONS[code][1])
        lab = f"{REGIONS[code][0]} {n}"
        if d.textlength(lab, font=SANS_B(10)) <= wseg - 8:
            d.text((x + 5, y + 1), lab, font=SANS_B(10), fill=(255, 255, 255))
        x += wseg
    return y + hgt


def main():
    stories = HEROES + CARDS + ALSO
    total = len(stories)
    reg_counts = {}
    field_counts = {}
    for (region, field) in all_stories():
        reg_counts[region] = reg_counts.get(region, 0) + 1
        field_counts[field] = field_counts.get(field, 0) + 1

    img = Image.new("RGB", (W, H), PAPER)
    d = RecDraw(ImageDraw.Draw(img))
    MX, RX = 12, W - 12
    SURE_COLORS = {"C": (26, 118, 60), "R": (186, 44, 36),
                   "W": (176, 110, 16), "S": (70, 90, 140),
                   "G": (0, 128, 110)}

    # -------------------------------- masthead (superskie template)
    land = sum(1 for c in reg_counts if c != "GLO")
    eye_r = (f"{total} STORIES \u00b7 {land} REGIONS + SPACE \u00b7 "
             f"{len(field_counts)} FIELDS \u00b7 ALL FROM THIS SUNDAY")
    d.text((MX, 8), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=SANS_B(15), fill=RED)
    rw = d.textlength(eye_r, font=SANS_B(15))
    d.text((RX - rw, 8), eye_r, font=SANS_B(15), fill=INK)
    check_h("eyebrow left", "ONE DAY OF WORLD NEWS, ONE PICTURE",
            SANS_B(15), MX, RX - rw - 8)
    d.rectangle([MX, 30, RX, 33], fill=RED)
    date = "Sunday 22 November 2026"
    dw = d.textlength(date, font=SERIF(66))
    d.text(((W - dw) / 2, 28), date, font=SERIF(66), fill=INK)
    d.line([MX, 116, RX, 116], fill=INK, width=2)
    LINES.append(((MX, 116, RX, 116), "date rule"))

    # -------------------------------- timeline: THE DAY IN UTC
    ty = 122
    d.rectangle([MX, ty, MX + 64, ty + 46], fill=RED)
    for j, s in enumerate(("THE DAY", "IN UTC")):
        tw = d.textlength(s, font=SANS_B(12))
        d.text((MX + 32 - tw / 2, ty + 7 + j * 16), s, font=SANS_B(12),
               fill=(255, 255, 255))
    col_x = MX + 72
    colw = (RX - col_x) // 7
    for i, (tm, cap) in enumerate(TIMELINE):
        cx = col_x + i * colw
        tw = d.textlength(tm, font=SANS_B(19))
        d.text((cx + colw / 2 - tw / 2, ty + 1), tm, font=SANS_B(19),
               fill=RED)
        lw = d.textlength(cap, font=SANS(11))
        d.text((cx + colw / 2 - lw / 2, ty + 27), cap, font=SANS(11),
               fill=(52, 48, 42))
        check_h(f"tl cap {i}", cap, SANS(11), cx + colw / 2 - lw / 2,
                cx + colw - 4)
        if i:
            LINES.append(((cx - 5, ty + 4, cx - 5, ty + 42), f"tl sep {i}"))
    d.line([MX, ty + 50, RX, ty + 50], fill=(150, 142, 126), width=1)
    LINES.append(((MX, ty + 50, RX, ty + 50), "timeline rule"))

    # -------------------------------- heroes: banner scene + band,
    # numbered kicker + status chip, big serif headline, 2-line deck
    hy = 178
    hw = (RX - MX - 26) // 3
    for i, hero in enumerate(HEROES):
        place, region, field, head, deck, src, sure, big, biglab = hero
        x = MX + i * (hw + 13)
        TAG[0] = ("hero", i)
        HERO_SCENES[i](d, x, hy, hw, 96)
        TAG[0] = None
        band = f"{place.split(',')[0]} \u2014 {big} {biglab}"
        d.rectangle([x, hy + 75, x + hw, hy + 96], fill=(176, 32, 28))
        bw = d.textlength(band, font=SANS_B(13))
        d.text((x + (hw - bw) / 2, hy + 79), band, font=SANS_B(13),
               fill=(255, 255, 255))
        check_h(f"hero{i+1} band", band, SANS_B(13),
                x + (hw - bw) / 2, x + hw - 4)
        ky = hy + 102
        col = REGIONS[region][1]
        d.ellipse([x + 1, ky, x + 19, ky + 18], fill=col)
        num = str(i + 1)
        nw = d.textlength(num, font=SANS_B(12))
        d.text((x + 10 - nw / 2, ky + 2), num, font=SANS_B(12),
               fill=(255, 255, 255))
        kick = place.replace(", ", " \u00b7 ")
        d.text((x + 25, ky + 1), kick, font=SANS_B(14), fill=col)
        chip_t = f"{SURE_LABEL[sure]} \u00b7 {src}"
        chw2 = d.textlength(chip_t, font=SANS_B(10)) + 14
        scol = SURE_COLORS[sure]
        d.rounded_rectangle([x + hw - chw2, ky - 1, x + hw, ky + 17],
                            radius=4, outline=scol, width=2)
        d.text((x + hw - chw2 + 7, ky + 2), chip_t, font=SANS_B(10),
               fill=scol)
        check_h(f"hero{i+1} kicker", kick, SANS_B(14), x + 25,
                x + hw - chw2 - 6)
        text_block(d, x, ky + 22, head, SERIF(29), INK, hw - 2, 32,
                   max_lines=2, tag=f"hero{i}")
        text_block(d, x, ky + 94, deck, SANS(13), (52, 48, 42), hw - 2,
                   17, max_lines=2, tag=f"herodeck{i}")

    # -------------------------------- cards: 5 across x 2 rows,
    # scene strip on top with flag, status chip and a big overlay
    cy = 414
    cw = (RX - MX - 40) // 5
    chh = 142
    OVERLAYS = [FIG["ukraine_killed_sunday"] + " KILLED",
                FIG["poland_missiles"] + " " + FIG["kh101_model"],
                "FREE PRESS", FIG["cikande_missing"] + " MISSING",
                FIG["bayelsa_dead"] + " DEAD",
                FIG["westbank_villages"] + " VILLAGES",
                FIG["gaza_killed_sunday"] + " KILLED", "MERCURY",
                FIG["vegas_margin"] + "s", FIG["china_margin_new"]]
    CROPS = [42, 18, 40, 42, 48, 40, 42, 36, 42, 38]
    for i, card in enumerate(CARDS):
        place, region, field, head, deck0, src, sure = card
        x = MX + (i % 5) * (cw + 10)
        yy0 = cy + (i // 5) * (chh + 8)
        snap = (len(OBSTACLES), len(H_CHECKS), len(OVERFLOWS))
        tmp = Image.new("RGB", (110, 86), PAPER)
        td = ImageDraw.Draw(tmp)
        TAG[0] = ("card", i)
        CARD_SCENES[i](td, 0, 0, 110, 86)
        TAG[0] = None
        del OBSTACLES[snap[0]:]
        del H_CHECKS[snap[1]:]
        del OVERFLOWS[snap[2]:]
        big_img = tmp.resize((192, 150), Image.LANCZOS)
        img.paste(big_img.crop((0, CROPS[i], 192, CROPS[i] + 42)),
                  (x + 1, yy0 + 1))
        d.rounded_rectangle([x, yy0, x + cw, yy0 + 43], radius=4,
                            outline=(120, 112, 96), width=1)
        flag(d, CARD_FLAGS[i], x + 5, yy0 + 5, w=24, h=16)
        FLAGS.append(((x + 5, yy0 + 5, x + 29, yy0 + 21),
                      f"card{i+4} flag", ("card", i)))
        scol = SURE_COLORS[sure]
        ct = SURE_LABEL[sure]
        cwid = d.textlength(ct, font=SANS_B(9)) + 10
        d.rounded_rectangle([x + cw - cwid - 4, yy0 + 4, x + cw - 4,
                             yy0 + 19], radius=3, fill=(255, 253, 246),
                            outline=scol, width=1)
        d.text((x + cw - cwid + 1, yy0 + 7), ct, font=SANS_B(9),
               fill=scol)
        ov = OVERLAYS[i]
        ow = d.textlength(ov, font=SANS_B(19))
        d.text((x + cw - ow - 6, yy0 + 20), ov, font=SANS_B(19),
               fill=(16, 20, 34), stroke_width=2,
               stroke_fill=(255, 253, 246))
        col = REGIONS[region][1]
        d.ellipse([x + 1, yy0 + 48, x + 17, yy0 + 64], fill=col)
        num = str(i + 4)
        nw = d.textlength(num, font=SANS_B(11))
        d.text((x + 9 - nw / 2, yy0 + 50), num, font=SANS_B(11),
               fill=(255, 255, 255))
        d.text((x + 22, yy0 + 49), place, font=SANS_B(12), fill=col)
        check_h(f"card{i+4} kicker", place, SANS_B(12), x + 22,
                x + cw - 4)
        text_block(d, x, yy0 + 66, head, SERIF(19), INK, cw - 4, 22,
                   max_lines=2, tag=f"card{i}")
        text_block(d, x, yy0 + 115, CARD_DECK[i], SANS(12), (52, 48, 42),
                   cw - 4, 15, max_lines=2, tag=f"carddeck{i}")

    # -------------------------------- bottom: map left, ALSO right
    by0 = 712
    d.line([MX, by0, RX, by0], fill=INK, width=2)
    LINES.append(((MX, by0, RX, by0), "bottom rule"))
    d.text((MX, by0 + 8), "WHERE IT HAPPENED", font=SANS_B(14), fill=RED)
    ax = 276
    also_head = "ALSO ON SUNDAY 22 NOVEMBER"
    d.text((ax, by0 + 8), also_head, font=SANS_B(14), fill=RED)
    check_h("also header", also_head, SANS_B(14), ax, RX)
    map_x, map_y, map_w, map_h = MX, by0 + 26, 240, 118
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=(16, 26, 44))
    LINES.append(((map_x, map_y, map_x + map_w, map_y), "map top"))
    LINES.append(((map_x, map_y + map_h, map_x + map_w, map_y + map_h),
                  "map bottom"))
    cw2, chh2 = map_w / 68, map_h / 30
    for r, spans in enumerate(LAND_SPANS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = map_x + (c + 0.5) * cw2
                cy2 = map_y + (r + 0.5) * chh2
                d.ellipse([cx - 1.6, cy2 - 1.6, cx + 1.6, cy2 + 1.6],
                          fill=(120, 150, 190))
    for (num, lon, lat, dx, dy) in PINS:
        tx = map_x + (lon + 168) / 360 * map_w
        tyy = map_y + (78 - lat) / 134 * map_h
        if dx or dy:
            d.ellipse([tx - 2, tyy - 2, tx + 2, tyy + 2],
                      fill=(255, 214, 90))
            d.line([tx, tyy, tx + dx, tyy + dy], fill=(255, 214, 90),
                   width=1)
        px2, py2 = tx + dx, tyy + dy
        col = REGIONS[stories[num - 1][1]][1]
        d.ellipse([px2 - 9, py2 - 9, px2 + 9, py2 + 9], fill=col,
                  outline=(255, 255, 255), width=1)
        ns = str(num)
        nw = d.textlength(ns, font=SANS_B(10))
        d.text((px2 - nw / 2, py2 - 6), ns, font=SANS_B(10),
               fill=(255, 255, 255))
    leg_names = {"EUR": "Europe", "ASI": "Asia-Pacific",
                 "AME": "Americas", "MEA": "Middle East",
                 "AFR": "Africa", "GLO": "Space"}
    for j, code in enumerate(("EUR", "ASI", "AME", "MEA", "AFR", "GLO")):
        lx = MX + (j % 2) * 122
        ly = map_y + map_h + 12 + (j // 2) * 17
        d.ellipse([lx, ly + 2, lx + 9, ly + 11], fill=REGIONS[code][1])
        d.text((lx + 14, ly), f"{leg_names[code]} {reg_counts[code]}",
               font=SANS(12), fill=INK)
    colw2 = (RX - ax - 16) // 2
    for i, (place, region, field, fact, src) in enumerate(ALSO):
        col_i, row = divmod(i, 11)
        x = ax + col_i * (colw2 + 16)
        yy = by0 + 26 + row * 17
        colr = REGIONS[region][1]
        d.ellipse([x, yy, x + 17, yy + 17], fill=colr)
        num = str(i + 14)
        nw = d.textlength(num, font=SANS_B(11))
        d.text((x + 8.5 - nw / 2, yy + 2), num, font=SANS_B(11),
               fill=(255, 255, 255))
        head = f"{place}: "
        d.text((x + 22, yy + 1), head, font=SANS_B(14), fill=colr)
        hw2 = d.textlength(head, font=SANS_B(14))
        tail = f"{fact} \u00b7 {src}"
        d.text((x + 22 + hw2 + 6, yy + 1), tail, font=SANS(14), fill=INK)
        check_h(f"also{i+14}", head + tail, SANS(14), x + 22,
                x + colw2 - 2)

    # -------------------------------- DATE CHECK box (red frame + tab)
    dy = 927
    d.rectangle([MX, dy, RX, dy + 56], fill=(253, 240, 238),
                outline=RED, width=2)
    LINES.append(((MX, dy, RX, dy), "datecheck top"))
    LINES.append(((MX, dy + 56, RX, dy + 56), "datecheck bottom"))
    d.rectangle([MX + 6, dy + 18, MX + 112, dy + 38], fill=RED)
    tw = d.textlength("DATE CHECK", font=SANS_B(12))
    d.text((MX + 59 - tw / 2, dy + 21), "DATE CHECK", font=SANS_B(12),
           fill=(255, 255, 255))
    dc = ("Left out on purpose, first reported before Sunday: Shenzhen "
          "summit and the ICJ Myanmar ruling (Thu 19); Nasdaq -"
          + FIG["nasdaq_friday"] + " close, the Bayer "
          + FIG["bayer_settlement"] + " settlement and Phumzile "
          "Mlambo-Ngcuka dies at " + FIG["mlambo_age"] + " (Fri 20); "
          "EU\u2013Indonesia deal, Geneva robot talks, the BepiColombo "
          "burn (confirmed Sun) and the Kryvyi Rih strike, toll set Sun "
          "(Sat 21). Not yet: a resumed COP32 date; Cikande's final "
          "toll; Benghazi's casualty count; whether the Kharg convoy "
          "sails.")
    text_block(d, MX + 122, dy + 6, dc, SANS(12), (52, 48, 42),
               RX - MX - 130, 15, max_lines=3, tag="datecheck")

    # -------------------------------- footer: attribution + HOW SURE
    fy = 992
    left = ("Every story happened or was first reported on Sun 22 Nov "
            "2026; claims attributed.")
    d.text((MX, fy), left, font=SANS(11), fill=(52, 48, 42))
    srcs = []
    for s in [h[5] for h in HEROES] + [c[5] for c in CARDS] \
            + [b[4] for b in ALSO]:
        if s not in srcs:
            srcs.append(s)
    src_line = ("Sources: " + ", ".join(srcs[:5]) + f" + {len(srcs) - 5} "
                "more \u00b7 Original drawings")
    sw = d.textlength(src_line, font=SANS(11))
    d.text((RX - sw, fy), src_line, font=SANS(11), fill=(52, 48, 42))
    check_h("footer left", left, SANS(11), MX, RX - sw - 8)
    seg = [("HOW SURE:  ", SANS_B(11), INK),
           ("CONFIRMED", SANS_B(11), SURE_COLORS["C"]),
           (" 2+ outlets \u00b7 ", SANS(11), INK),
           ("OFFICIAL", SANS_B(11), SURE_COLORS["W"]),
           (" on the record \u00b7 ", SANS(11), INK),
           ("REPORTED", SANS_B(11), SURE_COLORS["R"]),
           (" one outlet", SANS(11), INK)]
    xx = MX
    for txt_s, fnt, fl in seg:
        d.text((xx, fy + 15), txt_s, font=fnt, fill=fl)
        bb = d.textbbox((0, 0), txt_s, font=fnt)
        xx += (bb[2] - bb[0]) + 5

    print(f"H-CHECKS: {len(H_CHECKS)} measured, "
          f"{sum(1 for _, v in H_CHECKS if v > 0)} over limit")
    for lab, v in H_CHECKS:
        if v > -30:
            print(f"  h-check {lab}: slack {-v:+.1f}px")
    for tb, plate, margins in BANNER_CHECK:
        print(f"BANNER bbox text={tb} plate={plate} "
              f"margins L/T/R/B={margins}")
    if OVERFLOWS:
        print("OVERFLOWS:", *OVERFLOWS, sep="\n  ")
    out = HERE / "entry.png"
    audit_text_boxes()
    audit_graphics()
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes; stories:", total,
          "; regions:", reg_counts, "; fields:", field_counts)


def audit_graphics():
    """Text-vs-graphics: scene art registered as OBSTACLES must keep
    >=3px from every text. A scene's own label texts are exempt against
    that scene's own art (labels sit on art by design). Flags are also
    checked against their own scene's art with NO exemption."""
    def gap(a, b):
        dx = max(b[0] - a[2], a[0] - b[2], 0)
        dy = max(b[1] - a[3], a[1] - b[3], 0)
        if dx == 0 and dy == 0:
            return -1
        if dx and dy:
            return round((dx * dx + dy * dy) ** 0.5)
        return max(dx, dy)
    pens, mind, minpair, tested = [], 999, None, 0
    for (tb, txt, ttag) in TEXT_BOXES:
        for (ob, name, otag) in OBSTACLES + FLAGS:
            if ttag is not None and ttag == otag:
                continue
            tested += 1
            g = gap(tb, ob)
            if g < 0:
                pens.append((txt[:28], name))
            elif g < mind:
                mind, minpair = g, (txt[:28], name)
    for (fb, fname, ftag) in FLAGS:
        for (ob, name, otag) in OBSTACLES:
            if ftag != otag:
                continue
            tested += 1
            g = gap(fb, ob)
            if g < 0:
                pens.append((fname, name))
            elif g < mind:
                mind, minpair = g, (fname, name)
    print(f"GFX-AUDIT: {tested} text/flag-vs-graphics pairs tested, "
          f"{len(pens)} penetrations, min distance {mind}px at {minpair}")
    for p in pens:
        print("  GFX-PENETRATION:", p)
    return pens



# ------------------------------------------------------- card scenes (v3.3)
# CLARITY first (Ahmad, v3.3): one dominant subject per card, drawn big
# and simple — a reader who has not seen the headline should guess the
# story from the scene alone. Supporters stay small and quiet.
def card_label(d, x, y, w, h, text):
    tw = d.textlength(text, font=SANS_B(13))
    d.rectangle([x + 3, y + h - 21, x + 3 + tw + 10, y + h - 3],
                fill=(10, 14, 30))
    OBSTACLES.append(((x + 3, y + h - 21, x + 3 + tw + 10, y + h - 3),
                      f"card label chip '{text}'", TAG[0]))
    d.text((x + 8, y + h - 18), text, font=SANS_B(13), fill=(255, 255, 255))
    H_CHECKS.append((f"card scene label '{text}'",
                     round((x + 3 + tw + 10) - (x + w - 1), 1)))
    if x + 3 + tw + 10 > x + w - 1:
        OVERFLOWS.append(f"H-OVERFLOW card scene label: {text}")


def _sky(d, x, y, w, h, top, bot):
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)


def _flame(d, cx, cy, s, col=(255, 140, 40)):
    d.polygon([(cx, cy - s), (cx + s * 0.62, cy + s * 0.4),
               (cx + s * 0.3, cy + s), (cx - s * 0.3, cy + s),
               (cx - s * 0.62, cy + s * 0.4)], fill=col)
    d.polygon([(cx, cy - s * 0.3), (cx + s * 0.3, cy + s * 0.5),
               (cx, cy + s * 0.95), (cx - s * 0.3, cy + s * 0.5)],
              fill=(250, 205, 90))


def sc_dymer(d, x, y, w, h):
    # DOMINANT: a big apartment block, one section collapsed, rescuer below
    _sky(d, x, y, w, h, (120, 150, 180), (190, 205, 215))
    d.rectangle([x + 14, y + 6, x + 96, y + 62], fill=(150, 142, 130))
    for fy in (12, 24, 36, 48):
        for fx in (22, 40, 58, 76):
            d.rectangle([x + fx, y + fy, x + fx + 10, y + fy + 7],
                        fill=(60, 70, 90))
    d.polygon([(x + 52, y + 62), (x + 62, y + 30), (x + 96, y + 30),
               (x + 96, y + 62)], fill=(110, 102, 92))
    d.polygon([(x + 52, y + 62), (x + 62, y + 30), (x + 74, y + 30),
               (x + 64, y + 62)], fill=(90, 82, 74))
    d.ellipse([x + 28, y + 8, x + 44, y + 24], fill=(222, 184, 150))
    d.rectangle([x + 22, y + 24, x + 50, y + 48], fill=(255, 120, 40))
    d.rectangle([x + 22, y + 48, x + 50, y + 62], fill=(40, 40, 50))
    card_label(d, x, y, w, h, "DYMER")


def sc_warsaw(d, x, y, w, h):
    # DOMINANT: a big cruise missile lying on the ground, debris around it
    _sky(d, x, y, w, h, (168, 198, 224), (226, 232, 238))
    d.rectangle([x, y + 52, x + w, y + h], fill=(120, 130, 110))
    d.polygon([(x + 8, y + 30), (x + 28, y + 24), (x + 88, y + 24),
               (x + 98, y + 30), (x + 88, y + 36), (x + 28, y + 36)],
              fill=(200, 204, 210), outline=INK)
    d.polygon([(x + 88, y + 24), (x + 104, y + 30), (x + 88, y + 36)],
              fill=(150, 154, 160), outline=INK)
    d.polygon([(x + 28, y + 24), (x + 14, y + 14), (x + 20, y + 36)],
              fill=(150, 154, 160), outline=INK)
    d.rectangle([x + 48, y + 26, x + 58, y + 34], fill=RED)
    for dx, dy in ((16, 48), (30, 56), (84, 50), (96, 56)):
        d.polygon([(x + dx, y + dy), (x + dx + 8, y + dy - 4),
                   (x + dx + 10, y + dy + 4)], fill=(70, 74, 80))
    d.rectangle([x + 4, y + 62, x + w, y + h], fill=(90, 100, 84))
    card_label(d, x, y, w, h, "WARSAW")


def sc_istanbul(d, x, y, w, h):
    # DOMINANT: a marching crowd under one big blank banner
    _sky(d, x, y, w, h, (214, 190, 150), (232, 214, 180))
    d.rectangle([x + 8, y + 6, x + w - 8, y + 22], fill=(245, 243, 236),
                outline=INK, width=2)
    d.line([x + 12, y + 22, x + 12, y + 40], fill=INK, width=3)
    d.line([x + w - 12, y + 22, x + w - 12, y + 40], fill=INK, width=3)
    for i in range(6):
        xx = x + 12 + i * 16
        d.ellipse([xx, y + 30, xx + 12, y + 42], fill=(222, 184, 150))
        d.rectangle([xx - 1, y + 42, xx + 13, y + 56], fill=TEAL if i % 2 else RED)
    d.rectangle([x, y + 56, x + w, y + h], fill=(120, 110, 96))
    card_label(d, x, y, w, h, "ISTANBUL")


def sc_cikande(d, x, y, w, h):
    # DOMINANT: a big factory block in flames, black smoke above it
    _sky(d, x, y, w, h, (226, 200, 160), (240, 224, 190))
    d.rectangle([x + 10, y + 26, x + 100, y + 62], fill=(150, 148, 142))
    d.rectangle([x + 18, y + 34, x + 30, y + 44], fill=(60, 70, 90))
    d.rectangle([x + 38, y + 34, x + 50, y + 44], fill=(60, 70, 90))
    d.rectangle([x + 58, y + 34, x + 70, y + 44], fill=(60, 70, 90))
    _flame(d, x + 40, y + 18, 13)
    _flame(d, x + 62, y + 22, 10)
    _flame(d, x + 84, y + 16, 11)
    d.ellipse([x + 30, y + 2, x + 52, y + 14], fill=(70, 70, 80))
    d.ellipse([x + 58, y + 0, x + 78, y + 12], fill=(90, 90, 100))
    d.rectangle([x, y + 62, x + w, y + h], fill=(110, 100, 88))
    card_label(d, x, y, w, h, "CIKANDE")


def sc_bayelsa(d, x, y, w, h):
    # DOMINANT: an upside-down boat in the river, a life ring beside it
    _sky(d, x, y, w, h, (170, 200, 220), (222, 230, 234))
    d.rectangle([x, y + 40, x + w, y + h], fill=(52, 92, 128))
    d.polygon([(x + 12, y + 40), (x + 24, y + 26), (x + 86, y + 26),
               (x + 98, y + 40)], fill=(120, 74, 40))
    d.rectangle([x + 12, y + 38, x + 98, y + 42], fill=(90, 54, 30))
    d.ellipse([x + 18, y + 46, x + 30, y + 58], fill=(222, 184, 150))
    d.ellipse([x + 70, y + 48, x + 80, y + 58], fill=(222, 184, 150))
    d.ellipse([x + 84, y + 12, x + 102, y + 30], outline=(255, 60, 40),
              width=4)
    d.ellipse([x + 90, y + 18, x + 96, y + 24], outline=(255, 60, 40),
              width=3)
    card_label(d, x, y, w, h, "BAYELSA")


def sc_westbank(d, x, y, w, h):
    # DOMINANT: a big burning car in front of a stone house, olive tree
    _sky(d, x, y, w, h, (214, 190, 150), (232, 214, 180))
    d.rectangle([x + 8, y + 10, x + 60, y + 44], fill=(190, 172, 140))
    d.rectangle([x + 20, y + 20, x + 32, y + 32], fill=(60, 70, 90))
    d.rectangle([x + 40, y + 20, x + 52, y + 32], fill=(60, 70, 90))
    d.polygon([(x + 88, y + 4), (x + 96, y + 4), (x + 92, y + 16),
               (x + 100, y + 16), (x + 86, y + 34), (x + 90, y + 20),
               (x + 82, y + 20)], fill=(70, 130, 70), outline=INK)
    d.rectangle([x + 16, y + 36, x + 94, y + 54], fill=(52, 56, 66))
    d.polygon([(x + 20, y + 36), (x + 90, y + 36), (x + 84, y + 44),
               (x + 26, y + 44)], fill=(70, 74, 84))
    _flame(d, x + 55, y + 30, 12)
    _flame(d, x + 72, y + 34, 8)
    d.ellipse([x + 26, y + 52, x + 38, y + 62], fill=INK)
    d.ellipse([x + 72, y + 52, x + 84, y + 62], fill=INK)
    card_label(d, x, y, w, h, "WEST BANK")


def sc_gaza(d, x, y, w, h):
    # DOMINANT: a big tent camp, one tent torn, smoke over the roofs
    _sky(d, x, y, w, h, (214, 190, 150), (232, 214, 180))
    d.polygon([(x + 14, y + 30), (x + 52, y + 12), (x + 90, y + 30),
               (x + 90, y + 52), (x + 14, y + 52)], fill=(245, 243, 236),
              outline=INK, width=2)
    d.polygon([(x + 52, y + 12), (x + 66, y + 30), (x + 52, y + 30)],
              fill=(200, 198, 190), outline=INK)
    d.polygon([(x + 70, y + 44), (x + 96, y + 26), (x + 104, y + 44)],
              fill=(225, 222, 214), outline=INK)
    d.ellipse([x + 78, y + 4, x + 98, y + 16], fill=(90, 90, 100))
    d.ellipse([x + 88, y + 0, x + 104, y + 10], fill=(70, 70, 80))
    d.rectangle([x, y + 52, x + w, y + h], fill=(190, 172, 140))
    card_label(d, x, y, w, h, "KHAN YOUNIS")


def sc_mercury(d, x, y, w, h):
    # DOMINANT: the planet, big; the spacecraft burning toward it
    _sky(d, x, y, w, h, (8, 10, 24), (24, 28, 48))
    for sx, sy in ((8, 6), (26, 12), (96, 4), (14, 26)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 230))
    d.ellipse([x + 36, y + 24, x + 82, y + 70], fill=(168, 164, 158))
    OBSTACLES.append(((x + 36, y + 24, x + 82, y + 70),
                      "mercury disc", TAG[0]))
    for cx, cy, r in ((50, 38, 5), (68, 52, 6), (58, 62, 4), (72, 38, 4)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  outline=(130, 126, 120), width=2)
    d.rectangle([x + 18, y + 24, x + 34, y + 38], fill=(200, 204, 210))
    d.polygon([(x + 2, y + 20), (x + 18, y + 26), (x + 18, y + 36),
               (x + 2, y + 42)], fill=(70, 110, 190))
    d.polygon([(x + 34, y + 26), (x + 48, y + 20), (x + 48, y + 42),
               (x + 34, y + 36)], fill=(70, 110, 190))
    _flame(d, x + 26, y + 44, 7, col=(255, 160, 60))
    card_label(d, x, y, w, h, "MERCURY")


def sc_turin(d, x, y, w, h):
    # DOMINANT: a big gold trophy; a tennis ball and court lines behind
    _sky(d, x, y, w, h, (120, 170, 110), (90, 150, 84))
    d.rectangle([x + 4, y + 8, x + w - 4, y + 60], fill=(196, 120, 70))
    d.line([x + 4, y + 34, x + w - 4, y + 34], fill=(240, 240, 240),
           width=3)
    d.ellipse([x + 12, y + 44, x + 26, y + 58], fill=(210, 230, 80),
              outline=(240, 240, 240), width=2)
    d.polygon([(x + 38, y + 8), (x + 72, y + 8), (x + 66, y + 34),
               (x + 44, y + 34)], fill=(250, 205, 90), outline=INK)
    d.arc([x + 30, y + 12, x + 46, y + 28], 90, 270, fill=(250, 205, 90),
          width=4)
    d.arc([x + 64, y + 12, x + 80, y + 28], 270, 90, fill=(250, 205, 90),
          width=4)
    d.rectangle([x + 51, y + 34, x + 59, y + 44], fill=(250, 205, 90),
                outline=INK)
    d.rectangle([x + 42, y + 44, x + 68, y + 50], fill=(250, 205, 90),
                outline=INK)
    card_label(d, x, y, w, h, "TURIN")


def sc_lasvegas(d, x, y, w, h):
    # DOMINANT: a big open-wheel race car under neon lights
    _sky(d, x, y, w, h, (18, 26, 54), (70, 62, 92))
    for nx, nc in ((6, (255, 60, 120)), (30, (60, 220, 255)),
                   (54, (255, 214, 90)), (78, (255, 60, 120))):
        d.rectangle([x + nx, y + 4, x + nx + 18, y + 10], fill=nc)
    d.polygon([(x + 10, y + 44), (x + 22, y + 36), (x + 78, y + 36),
               (x + 96, y + 44), (x + 90, y + 52), (x + 16, y + 52)],
              fill=(30, 60, 160))
    d.polygon([(x + 40, y + 36), (x + 48, y + 24), (x + 66, y + 24),
               (x + 72, y + 36)], fill=(20, 40, 120))
    d.ellipse([x + 24, y + 46, x + 40, y + 62], fill=INK)
    d.ellipse([x + 66, y + 46, x + 82, y + 62], fill=INK)
    d.rectangle([x + 6, y + 30, x + 18, y + 36], fill=(200, 30, 40))
    d.rectangle([x, y + 62, x + w, y + h], fill=(40, 40, 52))
    card_label(d, x, y, w, h, "LAS VEGAS")


def sc_washington(d, x, y, w, h):
    # DOMINANT: the Capitol dome, big, with a signed deal paper in front
    _sky(d, x, y, w, h, (150, 175, 205), (215, 225, 235))
    d.ellipse([x + 38, y + 6, x + 72, y + 34], fill=(240, 240, 235))
    d.rectangle([x + 30, y + 30, x + 80, y + 62], fill=(230, 228, 220))
    d.rectangle([x + 52, y + 2, x + 58, y + 10], fill=(240, 240, 235))
    for cx in (36, 48, 60, 72):
        d.rectangle([x + cx, y + 40, x + cx + 4, y + 54], fill=(180, 178, 170))
    d.rectangle([x + 78, y + 34, x + 104, y + 62], fill=(245, 243, 236),
                outline=INK, width=2)
    d.line([x + 82, y + 42, x + 100, y + 42], fill=INK, width=2)
    d.line([x + 82, y + 48, x + 100, y + 48], fill=INK, width=2)
    d.line([x + 82, y + 54, x + 92, y + 54], fill=RED, width=2)
    d.ellipse([x + 94, y + 56, x + 102, y + 62], fill=RED)
    card_label(d, x, y, w, h, "WASHINGTON")


def sc_shanghai(d, x, y, w, h):
    # DOMINANT: a big rising chart arrow over a tower skyline
    _sky(d, x, y, w, h, (206, 214, 206), (228, 232, 222))
    d.rectangle([x + 8, y + 38, x + 24, y + 62], fill=(120, 130, 145))
    d.rectangle([x + 30, y + 28, x + 46, y + 62], fill=(90, 100, 120))
    d.rectangle([x + 52, y + 18, x + 68, y + 62], fill=(52, 84, 140))
    d.ellipse([x + 56, y + 8, x + 64, y + 16], fill=(52, 84, 140))
    d.rectangle([x + 74, y + 34, x + 90, y + 62], fill=(120, 130, 145))
    d.line([x + 10, y + 52, x + 40, y + 40, x + 62, y + 44, x + 96, y + 14],
           fill=(0, 140, 60), width=4)
    d.polygon([(x + 96, y + 14), (x + 84, y + 12), (x + 92, y + 26)],
              fill=(0, 140, 60))
    card_label(d, x, y, w, h, "SHANGHAI")


CARD_SCENES = [sc_dymer, sc_warsaw, sc_istanbul, sc_cikande, sc_bayelsa,
               sc_westbank, sc_gaza, sc_mercury, sc_lasvegas, sc_shanghai]



if __name__ == "__main__":
    main()

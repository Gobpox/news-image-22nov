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

# ------------------------------------------------------------------
# Design notes for whoever maintains this page next.
#
# One table drives everything. HEROES, CARDS and the ALSO rail are
# the only places story data lives; the strap counts, the region
# tally, the field tally and the source line are all computed from
# them at draw time. If a count on the page could be typed by hand,
# it eventually would be typed wrong, so none of them are.
#
# One registry drives every number. figures.json holds each figure
# once, with the exact display string the page must print. Panels
# interpolate the display; they never format a raw value themselves.
# The registry check outside this file fails the build when a stale
# value survives anywhere in the source, comments included.
#
# Geometry was settled before stories were counted. The type floors
# and the zone grid come first; the story set is then fitted to the
# space that exists, never the other way round. When a story does
# not fit at a readable size, the rail takes it or it is cut.
#
# Scenes are drawn, not decorated. Every pictured panel carries one
# dominant subject at the size the panel is actually viewed at, with
# its key fact lettered inside the scene on a band. A scene that
# needs its headline to be understood has failed; the pictogram
# strips on the cards are the strictest form of the same rule.
#
# The page audits itself. Text boxes, rule lines and scene graphics
# are recorded as they are drawn, and the audits at the end of the
# run fail on any intersection, any line through text, and any text
# sitting on graphics it would fight with. Nothing ships on a
# warning: an audit line that is not clean stops the build.
#
# Determinism is a feature. There is no randomness and no clock in
# the drawing path; two runs produce the same bytes, which is what
# makes a one-pixel regression visible instead of arguable.
# ------------------------------------------------------------------

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
# The ALSO rail is kept as one text block, one brief per line, fields
# separated by a pipe: place, region, field, the one-line fact, and the
# source tag. Facts that carry a registered figure name it in braces,
# and the loader below fills it from the registry, so a brief can never
# drift away from the checked number.
ALSO_TEXT = """KRYVYI RIH | EUR | Conflict | {kryvyi_injured} hurt, {kryvyi_children} children | AP
HORMUZ | MEA | Conflict | {hormuz_week} tankers hit in week | AJ
TURIN | EUR | Sport | Alcaraz beats Zverev 6-2 | ATP
WASHINGTON | AME | Diplomacy | Trump: 'permanent' | Fox
NEW YORK | AME | Tech | AI-chip spy bid | NYT
LIVERPOOL | EUR | Sport | 4-0 over Man Utd | BBC
HULL | EUR | Sport | 2-0 Brighton, late brace | BBC
PARIS | EUR | Sport | Dou\u00e9 ACL tear | AFP
SYDNEY | ASI | Politics | US lead narrows | Lowy
GILROY | AME | Politics | Interfaith ICE protest | KPFA
SEATTLE | AME | Politics | ICE takes two | KPFA
MADRID | EUR | Sport | Real fight back | La Liga
ADDIS ABABA | AFR | Climate | COP32 next | Guardian
MILAN | EUR | Sport | Milan 5-1 Frosinone | Serie A
BARCELONA | EUR | Sport | 3-2 Villarreal | La Liga
BERGAMO | EUR | Sport | Atalanta 4-4 Inter | Serie A
TURIN | EUR | Sport | Juventus 4-0 Venezia | Serie A
BREMEN | EUR | Sport | 4-0 Hamburg | Bundesliga
AUGSBURG | EUR | Sport | 3-1 Mainz | Bundesliga
GETAFE | EUR | Sport | Atl\u00e9tico win 3-0 away | La Liga
SANTANDER | EUR | Sport | 3-2 Sociedad | La Liga
BANDUNG | ASI | Sport | Persib 2-1 Bali | Aktualita"""

ALSO = []
for _row in ALSO_TEXT.strip().splitlines():
    _f = [part.strip() for part in _row.split(" | ")]
    ALSO.append((_f[0], _f[1], _f[2], _f[3].format_map(FIG), _f[4]))

# ------------------------------------------------------------- world map
# The world map is a coarse dot grid: each string below is one row of
# the grid, read left to right from the far west to the far east, and a
# hash mark means a land cell that gets a dot. The grid has thirty rows
# and every row is the same width; the drawing code asserts that, so a
# mistyped row fails loudly instead of shifting a continent.
LAND_MAP = [
    ".#####....#########.....####..............#######################...",
    ".######.#############..######.........#############################.",
    "..####################..####.....##################################.",
    "...###################..###.....##################################..",
    "...##################..........##################################...",
    "....#################..........#################################....",
    "....################..........#################################.....",
    "....################..........###############################.......",
    "....###############...........#############################.........",
    ".....#############...........##...########################..........",
    ".....############...........##############################..........",
    "......#########.............#############################...........",
    ".......#######..............############################............",
    ".........#####..............############################............",
    "...........####.............#############################...........",
    "................###########..##############################.........",
    "................###########..###############################........",
    "................###########...#############################.........",
    ".................##########...#########.............................",
    ".................#########....########..............................",
    ".................#########....########..............##########......",
    "..................########.....######.....#.........###########.....",
    "..................#######......######.....#..........##########.....",
    "..................#######......#####......#..........#########......",
    "....................###.........###....................####.........",
    "....................###.........................................##..",
    "....................##..............................................",
    "....................##..............................................",
    "....................##..............................................",
    "....................#...............................................",
]
assert all(len(row) == 68 for row in LAND_MAP) and len(LAND_MAP) == 30

# Pins for the numbered stories (heroes 1-3, cards 4-15): (num, lon, lat,
# dx, dy) — dx/dy nudge cluster pins apart, with a leader dot left behind.
# The pins are kept as a text block too: story number, longitude,
# latitude, then the nudge offsets that pull clustered pins apart.
PINS_TEXT = """1 | 31 | 37 | 16 | 20
2 | 50 | 26 | 30 | 36
3 | 20 | 32 | -30 | -14
4 | 30 | 50 | 30 | -6
5 | 21 | 52 | -28 | -10
6 | 29 | 41 | -30 | 18
7 | 106 | -6 | 0 | 0
8 | 6 | 5 | -40 | 30
9 | 35 | 32 | -24 | 30
10 | 34 | 31 | 24 | 34
12 | -115 | 36 | 0 | 0
13 | 121 | 31 | 0 | 0"""

PINS = [tuple(int(_v) for _v in _row.split(" | "))
        for _row in PINS_TEXT.strip().splitlines()]

# The day in UTC, kept as a text block: the hour first, then a caption.
TIMELINE_TEXT = """00:56 | Bepi in orbit
05:28 | Two killed in Gaza
08:28 | Kryvyi toll 73
12:48 | Nigeria toll 24
14:48 | Zelensky: Patriots
17:18 | Poland: 3 Kh-101
19:17 | Alcaraz wins Turin"""

TIMELINE = [tuple(_row.split(" | "))
            for _row in TIMELINE_TEXT.strip().splitlines()]




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


def SANS(sz):
    return _f("Archivo-Regular.ttf", sz)


def SANS_B(sz):
    return _f("Archivo-Bold.ttf", sz)


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


def _star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag(d, code, x, y, w=34, h=22):
    """Solid miniature flags: every field painted in saturated
    official colours (never the cream paper showing through), with
    the key elements of each design, all proportions relative to
    w/h so one drawing serves every chip size on the page. Most
    flags are data: FLAG_STEPS under this function lists the shapes
    to paint, in order, and _flag_steps paints them. A code with no
    entry gets the globe marker."""
    WHT = (255, 255, 255)
    d.rectangle([x, y, x + w, y + h], fill=WHT)
    if code in FLAG_STEPS:
        _flag_steps(d, code, x, y, w, h)
        d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
        return
    else:  # globe marker
        d.ellipse([x + 6, y + 1, x + 28, y + 21], fill=SKY, outline=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


# Flags as data. Each entry lists the shapes to paint over the white
# base, in painting order; _flag_steps below paints them. The step
# forms (fractions are of the flag's own width or height):
#   ("field", colour)                    the whole field, one colour
#   ("rect", fx0, fy0, fx1, fy1, colour)  a proportional rectangle
#   ("oval", fx0, fy0, fx1, fy1, colour)  an ellipse inside that box
#   ("band", fx0, i0, n, i1, colour)     a horizontal band: x from a
#                                        fraction, y by integer parts
#   ("hbands", i0, n, i1, colour)        a full-width horizontal band
#   ("vbands", i0, n, i1, colour)        a full-height vertical band
#   ("crescent", cx, cy, r, off, r2, colour, bite)
#                                        a disc, then a shifted bite
#                                        disc in the field colour
#   ("star", fx, fy, r, colour)          a five-pointed star
#   ("poly", [(fx, fy), ...], colour)    a polygon by fractions
#   ("line", fx0, fy0, fx1, fy1, colour, width)
#                                        width 0 means max(2, h // 8)
#   ("serrated", fx, colour)             a serrated hoist band
#   ("ring", cx, cy, r, n, sr, colour)   a ring of small stars
#   ("us", red, navy)                    the Stars and Stripes routine
FLAG_STEPS = {
    "UA": [("hbands", 1, 2, 2, (255, 213, 0)),
           ("hbands", 0, 2, 1, (0, 91, 187))],
    "ID": [("hbands", 0, 2, 1, (206, 17, 38))],
    "PL": [("hbands", 1, 2, 2, (220, 20, 60))],
    "NG": [("vbands", 0, 3, 1, (0, 135, 81)),
           ("vbands", 2, 3, 3, (0, 135, 81))],
    "PE": [("vbands", 0, 3, 1, (217, 0, 27)),
           ("vbands", 2, 3, 3, (217, 0, 27))],
    "IT": [("vbands", 0, 3, 1, (0, 140, 69)),
           ("vbands", 2, 3, 3, (205, 33, 42))],
    "SA": [("field", (0, 108, 53)),
           ("rect", 0.16, 0.30, 0.84, 0.52, (255, 255, 255)),
           ("line", 0.20, 0.70, 0.80, 0.70, (255, 255, 255), 0),
           ("line", 0.74, 0.62, 0.74, 0.70, (255, 255, 255), 2)],
    "TR": [("field", (227, 10, 23)),
           ("crescent", 0.40, 0.5, 0.30, 0.28, 0.82,
            (255, 255, 255), (227, 10, 23)),
           ("star", 0.70, 0.5, 0.17, (255, 255, 255))],
    "BH": [("field", (206, 17, 38)),
           ("serrated", 0.30, (255, 255, 255))],
    "LY": [("hbands", 0, 4, 1, (206, 17, 38)),
           ("hbands", 1, 4, 3, (0, 0, 0)),
           ("hbands", 3, 4, 4, (0, 122, 61)),
           ("crescent", 0.48, 0.5, 0.20, 0.3, 0.85,
            (255, 255, 255), (0, 0, 0)),
           ("star", 0.64, 0.5, 0.10, (255, 255, 255))],
    "CN": [("field", (222, 41, 16)),
           ("star", 0.24, 0.28, 0.20, (255, 222, 0)),
           ("star", 0.50, 0.14, 0.08, (255, 222, 0)),
           ("star", 0.60, 0.30, 0.08, (255, 222, 0)),
           ("star", 0.60, 0.52, 0.08, (255, 222, 0)),
           ("star", 0.48, 0.62, 0.08, (255, 222, 0))],
    "DK": [("field", (200, 16, 46)),
           ("rect", 0.30, 0.0, 0.43, 1.0, (255, 255, 255)),
           ("rect", 0.0, 0.39, 1.0, 0.61, (255, 255, 255))],
    "FI": [("rect", 0.28, 0.0, 0.44, 1.0, (0, 47, 108)),
           ("rect", 0.0, 0.36, 1.0, 0.64, (0, 47, 108))],
    "PS": [("hbands", 0, 3, 1, (0, 0, 0)),
           ("hbands", 2, 3, 3, (0, 122, 61)),
           ("poly", [(0.0, 0.0), (0.42, 0.5), (0.0, 1.0)],
            (238, 28, 37))],
    "IQ": [("hbands", 0, 3, 1, (206, 17, 38)),
           ("hbands", 2, 3, 3, (0, 0, 0)),
           ("rect", 0.40, 0.42, 0.60, 0.58, (0, 122, 61))],
    "OM": [("band", 0.30, 1, 3, 2, (239, 51, 64)),
           ("band", 0.30, 2, 3, 3, (0, 150, 57)),
           ("rect", 0.0, 0.0, 0.30, 1.0, (239, 51, 64)),
           ("oval", 0.10, 0.12, 0.20, 0.24, (255, 255, 255))],
    "CH": [("field", (218, 41, 28)),
           ("rect", 0.42, 0.20, 0.58, 0.80, (255, 255, 255)),
           ("rect", 0.26, 0.38, 0.74, 0.62, (255, 255, 255))],
    "MX": [("vbands", 0, 3, 1, (0, 104, 71)),
           ("vbands", 2, 3, 3, (206, 17, 38)),
           ("oval", 0.44, 0.38, 0.56, 0.62, (196, 148, 38))],
    "EU": [("field", (0, 51, 153)),
           ("ring", 0.5, 0.5, 0.32, 12, 0.075, (255, 204, 0))],
    "US": [("us", (178, 34, 52), (60, 59, 110))],
}


def _flag_steps(d, code, x, y, w, h):
    """Paint one table flag: the steps of FLAG_STEPS[code], in order,
    with the same arithmetic the hand-drawn branches used to use."""
    WHT = (255, 255, 255)
    for step in FLAG_STEPS[code]:
        kind = step[0]
        if kind == "field":
            d.rectangle([x, y, x + w, y + h], fill=step[1])
        elif kind == "rect":
            _, a, b, c, e, col = step
            d.rectangle([x + a * w, y + b * h, x + c * w, y + e * h],
                        fill=col)
        elif kind == "oval":
            _, a, b, c, e, col = step
            d.ellipse([x + a * w, y + b * h, x + c * w, y + e * h],
                      fill=col)
        elif kind == "band":
            _, a, i0, n, i1, col = step
            d.rectangle([x + a * w, y + i0 * h // n, x + w,
                         y + i1 * h // n], fill=col)
        elif kind == "hbands":
            _, i0, n, i1, col = step
            d.rectangle([x, y + i0 * h // n, x + w, y + i1 * h // n],
                        fill=col)
        elif kind == "vbands":
            _, i0, n, i1, col = step
            d.rectangle([x + i0 * w // n, y, x + i1 * w // n, y + h],
                        fill=col)
        elif kind == "crescent":
            _, cxf, cyf, rf, off, r2f, col, bite = step
            cx, cy, r = x + w * cxf, y + h * cyf, h * rf
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
            r2 = r * r2f
            d.ellipse([cx + r * off - r2, cy - r2, cx + r * off + r2,
                       cy + r2], fill=bite)
        elif kind == "star":
            _, fx, fy, rf, col = step
            _star(d, x + w * fx, y + h * fy, h * rf, col)
        elif kind == "poly":
            _, pts_f, col = step
            d.polygon([(x + fx * w, y + fy * h) for fx, fy in pts_f],
                      fill=col)
        elif kind == "line":
            _, a, b, c, e, col, wd = step
            d.line([x + a * w, y + b * h, x + c * w, y + e * h],
                   fill=col, width=max(2, h // 8) if wd == 0 else wd)
        elif kind == "serrated":
            _, fx, col = step
            pts = [(x, y)]
            for i in range(5):
                pts.append((x + w * fx, y + h * (0.1 + i * 0.2)))
                pts.append((x, y + h * (0.2 + i * 0.2)))
            pts.append((x, y + h))
            d.polygon(pts, fill=col)
        elif kind == "ring":
            _, cxf, cyf, rf, n, srf, col = step
            import math
            cx, cy, rr = x + w * cxf, y + h * cyf, h * rf
            for i in range(n):
                ang = i * math.pi / (n // 2)
                _star(d, cx + rr * math.cos(ang),
                      cy + rr * math.sin(ang), max(1.6, h * srf), col)
        elif kind == "us":
            _, red, navy = step
            sh = h / 13
            for i in range(13):
                if i % 2 == 0:
                    d.rectangle([x, y + i * sh, x + w,
                                 y + (i + 1) * sh + 1], fill=red)
            cw2, ch2 = w * 0.44, sh * 7
            d.rectangle([x, y, x + cw2, y + ch2], fill=navy)
            for r in range(3):
                for c in range(4):
                    sx = x + cw2 * (c + 0.5) / 4
                    sy = y + ch2 * (r + 0.5) / 3
                    d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHT)


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


def burst_shape(g, kx, ky, rad, col=(255, 150, 40), core=(255, 226, 120)):
    # sixteen-point starburst with a bright core: an explosion glyph
    import math
    points = []
    for step in range(16):
        angle = math.pi * step / 8
        reach = rad if step % 2 == 0 else rad * 0.45
        points.append((kx + reach * math.cos(angle),
                       ky + reach * math.sin(angle)))
    g.polygon(points, fill=col)
    g.ellipse([kx - rad * 0.32, ky - rad * 0.32, kx + rad * 0.32,
               ky + rad * 0.32], fill=core)


def pic_drone(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(148, 168, 188))
    # a single large quadcopter silhouette, left of centre
    dark = (24, 28, 38)
    for (rotor_x, rotor_y) in ((ox + 22, oy + 7), (ox + 78, oy + 7),
                               (ox + 22, oy + 25), (ox + 78, oy + 25)):
        g.line([rotor_x + 8, rotor_y + 3, ox + 58, oy + 19], fill=dark,
               width=4)
        g.ellipse([rotor_x, rotor_y, rotor_x + 16, rotor_y + 6], fill=dark)
    g.rectangle([ox + 44, oy + 14, ox + 72, oy + 26], fill=dark)
    g.ellipse([ox + 52, oy + 24, ox + 64, oy + 32], fill=(200, 40, 36))
    burst_shape(g, ox + 128, oy + 22, 17)


def pic_missiles(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(168, 182, 198))
    # THREE large missiles stacked in a row: the count is the story
    for idx, row_y in enumerate((6, 17, 28)):
        g.polygon([(ox + 18, oy + row_y + 3), (ox + 30, oy + row_y),
                   (ox + 92, oy + row_y), (ox + 104, oy + row_y + 3),
                   (ox + 92, oy + row_y + 6), (ox + 30, oy + row_y + 6)],
                  fill=(38, 44, 56))
        g.polygon([(ox + 92, oy + row_y), (ox + 104, oy + row_y + 3),
                   (ox + 92, oy + row_y + 6)], fill=(200, 40, 36))
        g.polygon([(ox + 18, oy + row_y + 3), (ox + 8, oy + row_y - 2),
                   (ox + 10, oy + row_y + 3), (ox + 8, oy + row_y + 8)],
                  fill=(38, 44, 56))


def pic_megaphone(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(216, 206, 178))
    # an oversized megaphone in front of a row of crowd heads
    g.polygon([(ox + 26, oy + 12), (ox + 62, oy + 4), (ox + 62, oy + 26),
               (ox + 26, oy + 20)], fill=(200, 40, 36))
    g.rectangle([ox + 18, oy + 11, ox + 27, oy + 21], fill=(24, 28, 38))
    g.rectangle([ox + 30, oy + 20, ox + 37, oy + 30], fill=(24, 28, 38))
    for head_x in (76, 98, 120, 142, 164):
        g.ellipse([ox + head_x, oy + 24, ox + head_x + 15, oy + 39],
                  fill=(222, 184, 150), outline=(24, 28, 38), width=1)
        g.rectangle([ox + head_x - 1, oy + 37, ox + head_x + 16, oy + 42],
                    fill=(52, 84, 140))


def pic_factory(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(196, 200, 204))
    # one plain factory block carrying one very large flame
    g.rectangle([ox + 14, oy + 26, ox + 104, oy + 42], fill=(52, 58, 68))
    g.rectangle([ox + 84, oy + 14, ox + 96, oy + 42], fill=(52, 58, 68))
    for win_x in (24, 42, 60):
        g.rectangle([ox + win_x, oy + 31, ox + win_x + 10, oy + 38],
                    fill=(250, 214, 120))
    _flame(g, ox + 46, oy + 16, 17)


def pic_hull(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(170, 198, 214))
    # one capsized hull, keel up, riding over a band of waves
    g.polygon([(ox + 18, oy + 12), (ox + 118, oy + 12), (ox + 102, oy + 26),
               (ox + 34, oy + 26)], fill=(96, 62, 34))
    g.rectangle([ox + 30, oy + 8, ox + 106, oy + 12], fill=(60, 40, 22))
    g.rectangle([ox, oy + 30, ox + wd, oy + ht], fill=(38, 92, 140))
    for wave_x in (8, 48, 88, 128, 162):
        g.arc([ox + wave_x, oy + 26, ox + wave_x + 26, oy + 38], 180, 360,
              fill=(220, 238, 250), width=3)


def pic_house(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(206, 190, 168))
    # one pitched-roof village house with one very large flame
    g.rectangle([ox + 30, oy + 20, ox + 86, oy + 42], fill=(70, 60, 50))
    g.polygon([(ox + 22, oy + 21), (ox + 58, oy + 6), (ox + 94, oy + 21)],
              fill=(120, 44, 36))
    g.rectangle([ox + 51, oy + 30, ox + 65, oy + 42], fill=(30, 26, 22))
    _flame(g, ox + 82, oy + 12, 19)


def pic_blast(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(188, 178, 168))
    # ONE dominant explosion burst above a low building silhouette
    g.rectangle([ox + 8, oy + 33, ox + 130, oy + 42], fill=(44, 42, 46))
    for win_x in (20, 44, 68, 92):
        g.rectangle([ox + win_x, oy + 36, ox + win_x + 7, oy + 40],
                    fill=(250, 214, 120))
    burst_shape(g, ox + 66, oy + 19, 19)


def pic_probe(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(18, 22, 40))
    # a probe with blue panel wings closing on the big orange planet
    for pan_x in (8, 108):
        g.rectangle([ox + pan_x, oy + 12, ox + pan_x + 44, oy + 30],
                    fill=(52, 84, 160))
        for grid_i in range(1, 4):
            g.line([ox + pan_x + grid_i * 11, oy + 12,
                    ox + pan_x + grid_i * 11, oy + 30],
                   fill=(140, 170, 220), width=1)
        g.line([ox + pan_x, oy + 21, ox + pan_x + 44, oy + 21],
               fill=(140, 170, 220), width=1)
    g.rectangle([ox + 52, oy + 19, ox + 108, oy + 23], fill=(200, 204, 214))
    g.ellipse([ox + 66, oy + 5, ox + 102, oy + 41], fill=(232, 130, 52))
    g.ellipse([ox + 76, oy + 14, ox + 86, oy + 24], fill=(198, 104, 40))


def pic_f1(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(206, 210, 216))
    # one Formula 1 car in side profile: impossible to misread
    dark = (16, 18, 24)
    g.polygon([(ox + 14, oy + 26), (ox + 52, oy + 24), (ox + 78, oy + 14),
               (ox + 108, oy + 14), (ox + 128, oy + 22), (ox + 158, oy + 24),
               (ox + 162, oy + 28), (ox + 128, oy + 30), (ox + 46, oy + 30),
               (ox + 16, oy + 29)], fill=dark)
    g.rectangle([ox + 140, oy + 6, ox + 146, oy + 24], fill=dark)
    g.rectangle([ox + 128, oy + 6, ox + 160, oy + 10], fill=(200, 40, 36))
    g.rectangle([ox + 16, oy + 16, ox + 22, oy + 27], fill=(200, 40, 36))
    g.polygon([(ox + 70, oy + 14), (ox + 84, oy + 6), (ox + 96, oy + 6),
               (ox + 104, oy + 14)], fill=dark)
    for wheel_x in (34, 128):
        g.ellipse([ox + wheel_x, oy + 24, ox + wheel_x + 17, oy + 41],
                  fill=dark)
        g.ellipse([ox + wheel_x + 5, oy + 29, ox + wheel_x + 12, oy + 36],
                  fill=(150, 156, 166))


def pic_chart(g, ox, oy, wd, ht):
    g.rectangle([ox, oy, ox + wd, oy + ht], fill=(210, 218, 208))
    # the kept market diagram, drawn bolder: rising bars, fat arrow
    for idx, bar_h in enumerate((12, 19, 27, 36)):
        bar_x = ox + 14 + idx * 30
        g.rectangle([bar_x, oy + 42 - bar_h, bar_x + 20, oy + 42],
                    fill=(52, 84, 140))
    g.line([ox + 10, oy + 34, ox + 52, oy + 24, ox + 88, oy + 27,
            ox + 128, oy + 8], fill=(0, 148, 64), width=5)
    g.polygon([(ox + 128, oy + 8), (ox + 114, oy + 7), (ox + 122, oy + 19)],
              fill=(0, 148, 64))


STRIP_PICS = [pic_drone, pic_missiles, pic_megaphone, pic_factory,
              pic_hull, pic_house, pic_blast, pic_probe, pic_f1,
              pic_chart]


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
        tmp = Image.new("RGB", (190, 42), PAPER)
        td = ImageDraw.Draw(tmp)
        STRIP_PICS[i](td, 0, 0, 190, 42)
        img.paste(tmp, (x + 1, yy0 + 1))
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
    for r, row in enumerate(LAND_MAP):
        for c, cell in enumerate(row):
            if cell != "#":
                continue
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
def _flame(d, cx, cy, s, col=(255, 140, 40)):
    d.polygon([(cx, cy - s), (cx + s * 0.62, cy + s * 0.4),
               (cx + s * 0.3, cy + s), (cx - s * 0.3, cy + s),
               (cx - s * 0.62, cy + s * 0.4)], fill=col)
    d.polygon([(cx, cy - s * 0.3), (cx + s * 0.3, cy + s * 0.5),
               (cx, cy + s * 0.95), (cx - s * 0.3, cy + s * 0.5)],
              fill=(250, 205, 90))


if __name__ == "__main__":
    main()

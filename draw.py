"""One-page newspaper front page for Wednesday 25 November 2026.

Assembles 29 stories across 7 regions into a single 1024x1024 PNG:
top bar, masthead, kicker, region strip, UTC timeline, three hero
cards plus the day-in-numbers box, ten small cards, the also-list
with a world map, a date check and a footer.
"""

import json
import os

from PIL import Image, ImageDraw

from art import art
from gfx import (
    ASH, AZURE, BG, BLACK, EDGE, GILT, ISSUES, LEAF, MIDNIGHT, NOTO,
    PANEL, PILL, SCARLET, SEA, TANGERINE, TY, box, disc, draw_segs,
    flag, fresh, load_font, seg, txt, wrap,
)

HERE = os.path.dirname(os.path.abspath(__file__))

MX = 12
RX = 1012
HY = 200
HH = 252
HW = 260
NW = 196
HA = 105
SY = 460
SR = 154
SW = 196
SA = 60
SH = 146
MY = 768
CY = 942
FY = 996

WHITE = (255, 255, 255)
GREY60 = (60, 60, 60)
NUMLAB = (200, 210, 230)
NUMLINE = (80, 100, 140)

# ---------------------------------------------------------------- data

# num, place, topic, source, status, headline, deck, big label,
# small label, art key, pill
FRONT = [
    (1, "WASHINGTON", "TRADE", "REUTERS", "REPORTED",
     "Trump set to unveil new tariffs",
     "Section 301 probe into 16 trading partners nears release; "
     "Asian stocks tumble as tariff fears return.",
     "NEW TARIFFS", "16 PARTNERS", "sanctions", "REPORTED"),
    (2, "GULF OF OMAN", "WAR", "SHIP DATA · PARALLAX", "REPORTED",
     "Iranian tankers cross the blockade",
     "Three tankers carrying 3.8m barrels slip past the US blockade "
     "line; a ceasefire deal is set for Friday in Switzerland.",
     "3 TANKERS", "3.8M BARRELS", "gulfwar", "REPORTED"),
    (3, "MOSCOW", "WAR", "AP · INDEPENDENT", "REPORTED",
     "Putin vows retaliation on oil plants",
     "Putin calls retaliation 'inevitable' as Ukraine keeps hitting "
     "Russian refineries; a strike on Zaporizhzhia kills 2.",
     "RETALIATION", "OIL PLANTS HIT", "oil", "REPORTED"),
    (4, "SANTA CLARA", "TECH", "REUTERS", "REPORTED",
     "Nvidia slides on Huang doubts",
     "Shares fall 6% on Huang doubts.",
     "–6%", "HUANG PROBE", "chip", "REPORTED"),
    (5, "CIKANDE", "DISASTER", "XINHUA · AP", "REPORTED",
     "Cikande search for 8 missing",
     "Toll at 26 as 600 rescuers comb the wreckage.",
     "26 DEAD", "8 MISSING", "factoryfire", "REPORTED"),
    (6, "ANTALYA", "CLIMATE", "REUTERS · UN", "REPORTED",
     "COP31 flop: focus shifts to COP32",
     "Focus moves to COP32 in Addis Ababa.",
     "NO DEAL", "COP32 NEXT", "copcollapse", "REPORTED"),
    (7, "WASHINGTON", "POLITICS", "H.UA · REUTERS", "REPORTED",
     "Zelenskyy turns to new Congress",
     "Kyiv will ask the new House for aid if talks fail.",
     "NEW CONGRESS", "AID IF NO DEAL", "house258", "REPORTED"),
    (8, "BAGHDAD", "POLITICS", "REUTERS", "REPORTED",
     "Baghdad seizes Kurdish oilfields",
     "Baghdad moves on Kurdish oilfields; Erbil warns.",
     "SEIZE FIELDS", "KURD OIL ROW", "kurdoil", "REPORTED"),
    (9, "CANBERRA", "POLITICS", "REUTERS", "REPORTED",
     "Australia apologises to veterans",
     "Formal apology for decades of discrimination.",
     "SORRY", "LGBTQ VETERANS", "apology", "REPORTED"),
    (10, "MADRID", "SPORT", "REUTERS · AP", "REPORTED",
     "Real Madrid rout PSV 5-1",
     "Bellingham stunner, Mbappé brace in 5-1 rout.",
     "5-1", "BELLINGHAM + MBAPPÉ", "football", "REPORTED"),
    (11, "WASHINGTON", "ECONOMY", "REUTERS · AP", "REPORTED",
     "Consumer confidence hits 103.3",
     "Highest in nearly two years after the midterms.",
     "103.3", "HIGHEST SINCE 2025", "chart", "REPORTED"),
    (12, "CARTAGENA", "CRIME", "AP · REUTERS", "REPORTED",
     "25 held hostage in supermarket",
     "Gunmen flee into a store after a failed robbery.",
     "25 HELD", "CARTAGENA STANDOFF", "hostage", "REPORTED"),
    (13, "GAZA", "WAR", "AL JAZEERA", "REPORTED",
     "Top Hamas security figure killed",
     "Senior official, police and siblings killed.",
     "SENIOR FIGURE", "DRONE STRIKES", "gaza", "REPORTED"),
]

# num, city, headline, outlet
ALSO = [
    (14, "Seoul", "Asian stocks tumble", "REUTERS"),
    (15, "Riyadh", "PIF building hit again", "REUTERS"),
    (16, "Tehran", "Drug shortage bites", "DW"),
    (17, "Washington", "Turkey pardons", "AP"),
    (18, "Kyiv", "Zelenskyy presses NATO", "AP"),
    (19, "London", "GPS jamming", "REUTERS"),
    (20, "New York", "$1.1B seized", "AP"),
    (21, "Beijing", "50 Boeing jets ordered", "REUTERS"),
    (22, "Dhaka", "Guangzhou office", "REUTERS"),
    (23, "Sydney", "Inflation runs hotter", "REUTERS"),
    (24, "Kinshasa", "Rebels pull back", "REUTERS"),
    (25, "Lubumbashi", "Cobalt ban", "REUTERS"),
    (26, "Warsaw", "Drone incursion", "AP"),
    (27, "Yangon", "Landmine toll peaks", "REUTERS"),
    (28, "Berlin", "Merz backs Kyiv", "AP"),
    (29, "Brussels", "EU sets gas exit dates", "REUTERS"),
]

ALSO_SUB = {
    14: "Korea -5.3%, Taiwan -5.1% on tariff fears.",
    15: "Second attack on PIF tower in a week.",
    16: "Pharmacies shut as supplies halt.",
    17: "Thanksgiving pardon at the White House.",
    18: "Seeks Patriot batteries, membership.",
    19: "Russian ship blamed for interference.",
    20: "North Korean hackers stole from Binance.",
    21: "China Southern unit buys 737-8s.",
    22: "Bangladesh woos investors in China.",
    23: "Core inflation stays stubbornly high.",
    24: "Rebels pull back after clashes.",
    25: "Export ban returns as prices fall.",
    26: "Drone crossed near Dorohusk.",
    27: "6,929 casualties in 2025.",
    28: "Membership could have prevented war.",
    29: "Final deadlines to end Russian gas.",
}

FLAG_OF = {
    14: "KR", 15: "SA", 16: "IR", 17: "US", 18: "UA", 19: "GB",
    20: "US", 21: "CN", 22: "BD", 23: "AU", 24: "CD", 25: "CD",
    26: "PL", 27: "MM", 28: "DE", 29: "BE",
}

ALSO_REGION = {
    14: "ASIA-PACIFIC", 15: "MIDDLE EAST", 16: "MIDDLE EAST",
    17: "AMERICAS", 18: "EUROPE", 19: "EUROPE", 20: "AMERICAS",
    21: "ASIA-PACIFIC", 22: "ASIA-PACIFIC", 23: "OCEANIA",
    24: "AFRICA", 25: "AFRICA", 26: "EUROPE", 27: "ASIA-PACIFIC",
    28: "EUROPE", 29: "EUROPE",
}

# big number, label, region, number colour
STATS = [
    ("3", "tankers cross blockade", "MIDDLE EAST", (90, 130, 230)),
    ("26", "dead in Cikande fire", "ASIA-PACIFIC", (240, 90, 90)),
    ("97%", "chance of Fed Dec hike", "AMERICAS", (235, 90, 40)),
    ("+11", "consumer confidence jump", "AMERICAS", (80, 200, 120)),
    ("62%", "back repealing tariffs", "AMERICAS", (230, 150, 0)),
    ("€115BN", "Ukraine needs for 2027", "EUROPE", (108, 158, 210)),
]

# name, count, fill, text colour
REGIONS = [
    ("EUROPE", 7, (36, 100, 198), WHITE),
    ("MIDDLE EAST", 5, (198, 52, 38), WHITE),
    ("AFRICA", 2, (39, 136, 63), WHITE),
    ("ASIA-PACIFIC", 5, (225, 118, 23), WHITE),
    ("AMERICAS", 7, (116, 82, 189), WHITE),
    ("OCEANIA", 2, (20, 136, 140), WHITE),
    ("WORLD", 1, (72, 72, 84), WHITE),
]

REGION_OF = {
    1: "AMERICAS", 2: "MIDDLE EAST", 3: "EUROPE", 4: "AMERICAS",
    5: "ASIA-PACIFIC", 6: "WORLD", 7: "AMERICAS", 8: "MIDDLE EAST",
    9: "OCEANIA", 10: "EUROPE", 11: "AMERICAS", 12: "AMERICAS",
    13: "MIDDLE EAST",
}

COUNTRY_OF = {
    1: "USA", 2: None, 3: "RUSSIA", 4: "USA", 5: "INDONESIA",
    6: "TÜRKIYE", 7: "USA", 8: "IRAQ", 9: "AUSTRALIA", 10: "SPAIN",
    11: "USA", 12: "COLOMBIA", 13: "PALESTINE",
}

REGION_COLOUR = {name: fill for name, _count, fill, _text in REGIONS}

REGION_SHORT = {"ASIA-PACIFIC": "ASIA"}


def region_label(name):
    return REGION_SHORT.get(name, name)


# numbered red pins for the 13 front stories: lon, lat
PINS = {
    1: (-77.0, 38.9), 2: (57.5, 25.0), 3: (37.6, 55.8),
    4: (-121.9, 37.4), 5: (106.1, -6.0), 6: (30.7, 36.9),
    7: (-77.0, 38.9), 8: (44.4, 33.3), 9: (149.1, -35.3),
    10: (-3.7, 40.4), 11: (-77.0, 38.9), 12: (-75.5, 10.4),
    13: (34.5, 31.5),
}

# dark dots for the 16 also stories: lon, lat
DOTS = {
    14: (127.0, 37.5), 15: (46.7, 24.7), 16: (51.4, 35.7),
    17: (-77.0, 38.9), 18: (30.5, 50.4), 19: (-0.1, 51.5),
    20: (-74.0, 40.7), 21: (116.4, 39.9), 22: (90.4, 23.8),
    23: (151.2, -33.9), 24: (15.3, -4.3), 25: (27.5, -11.7),
    26: (21.0, 52.2), 27: (96.2, 16.8), 28: (13.4, 52.5),
    29: (4.4, 50.8),
}

# pixel nudges for colliding pins / dots: dx, dy
PIN_OFF = {7: (15, -9), 11: (-15, 9)}
DOT_OFF = {
    17: (15, 11), 18: (12, -2), 19: (-12, -6), 22: (0, -10),
    26: (-10, -10), 27: (10, 8), 28: (10, 8), 29: (-14, 6),
}

# ---------------------------------------------------------------- pictures


def heropic(key, w):
    return art(key, w, 105)


def minipic(key):
    return art(key, 196, 80).resize((196, 60), Image.LANCZOS)


# ---------------------------------------------------------------- pieces


def topbar(d, x, y, w, num, place, country, region, vtag, font, boxh,
           discr, pad):
    label = place
    if country:
        label = label + ", " + country
    size = font.size
    f = font
    while d.textlength(label, font=f) > w - 40 and size > 8:
        size -= 1
        f = load_font("NotoSans-Bold.ttf", size, NOTO)
    tw = d.textlength(label, font=f)
    bw = pad + discr * 2 + 4 + tw + pad
    bx = x + pad
    by = y + pad
    d.rectangle([bx, by, bx + bw, by + boxh], fill=WHITE,
                outline=BLACK, width=1)
    disc(d, bx + pad + discr, by + boxh // 2, discr, REGION_COLOUR[region])
    txt(d, (bx + pad + discr, by + boxh // 2), str(num), TY["tag"], WHITE,
        anchor="mm")
    txt(d, (bx + pad + discr * 2 + 4, by + boxh // 2), label, f, BLACK,
        anchor="lm")


def pill_br(d, x, y, w, h, vtag):
    pw = int(d.textlength(vtag, font=TY["tag"])) + 10
    x1 = x + w - 4
    y1 = y + h - 3
    d.rounded_rectangle([x1 - pw, y1 - 12, x1, y1], radius=2,
                        fill=PILL[vtag])
    txt(d, (x1 - pw + 5, y1 - 6), vtag, TY["tag"], WHITE, anchor="lm")


def hero_card(img, d, story, x, y, w):
    num, place, topic, src, _status, head, deck, _big, _small, key, vtag = story
    region = REGION_OF[num]
    box(d, x, y, x + w, y + HH, PANEL)
    img.paste(heropic(key, w), (x, y))
    d2 = ImageDraw.Draw(img)
    topbar(d2, x, y, w, num, place, COUNTRY_OF[num], region, vtag,
           TY["slab"], 18, 7, 4)
    pill_br(d2, x, y, w, HA, vtag)
    y0 = y + HA + 6
    txt(d2, (x + 8, y0), region_label(region) + " · " + topic,
        TY["topic"], REGION_COLOUR[region])
    heads = wrap(d2, head, TY["hhead"], w - 16, cap=3)
    decks = wrap(d2, deck, TY["hdeck"], w - 16, cap=3)
    hy = y0 + 16
    for j, line in enumerate(heads):
        txt(d2, (x + 8, hy + j * 29), line, TY["hhead"], BLACK)
    dy = hy + len(heads) * 29 + 2
    for j, line in enumerate(decks):
        txt(d2, (x + 8, dy + j * 14), line, TY["hdeck"], GREY60)
    txt(d2, (x + 8, y + HH - 14), src, TY["src"], ASH)
    d.rectangle([x, y, x + w, y + HH], outline=BLACK, width=1)


def small_card(img, d, story, x, y):
    num, place, topic, src, _status, head, deck, _big, _small, key, vtag = story
    region = REGION_OF[num]
    box(d, x, y, x + SW, y + SH, PANEL)
    img.paste(minipic(key), (x, y))
    d2 = ImageDraw.Draw(img)
    topbar(d2, x, y, SW, num, place, COUNTRY_OF[num], region, vtag,
           TY["slab10"], 15, 6, 3)
    pill_br(d2, x, y, SW, SA, vtag)
    y0 = y + SA + 5
    txt(d2, (x + 8, y0), region_label(region) + " · " + topic,
        TY["topicsm"], REGION_COLOUR[region])
    heads = wrap(d2, head, TY["shead"], SW - 16, cap=2)
    for j, line in enumerate(heads):
        txt(d2, (x + 8, y0 + 14 + j * 20), line, TY["shead"], BLACK)
    decks = wrap(d2, deck + " — " + src, TY["sdeck"], SW - 16, cap=2)
    for j, line in enumerate(decks):
        txt(d2, (x + 8, y0 + 15 + len(heads) * 20 + j * 12), line,
            TY["sdeck"], GREY60)
    d.rectangle([x, y, x + SW, y + SH], outline=BLACK, width=1)


def numbers_box(d, x, y):
    box(d, x, y, x + NW, y + HH, MIDNIGHT)
    txt(d, (x + 10, y + 8), "THE DAY IN NUMBERS", TY["numtitle"], WHITE)
    seg(d, [(x + 10, y + 26), (x + NW - 10, y + 26)], NUMLINE, width=1)
    ey = y + 30
    for big, label, _region, colour in STATS:
        size = TY["numbig"].size
        f = TY["numbig"]
        while d.textlength(big, font=f) > NW - 20 and size > 18:
            size -= 1
            f = load_font("NotoSans-Black.ttf", size, NOTO)
        txt(d, (x + 10, ey), big, f, colour)
        txt(d, (x + 10, ey + 26), label, TY["numlab"], NUMLAB)
        ey += 36
    d.rectangle([x, y, x + NW, y + HH], outline=BLACK, width=1)


# ---------------------------------------------------------------- map


def _inside(lon, lat, polys):
    for ring, bbox in polys:
        lon0, lon1, lat0, lat1 = bbox
        if lon < lon0 or lon > lon1 or lat < lat0 or lat > lat1:
            continue
        inside = False
        n = len(ring)
        for i in range(n):
            x0, y0 = ring[i]
            x1, y1 = ring[(i + 1) % n]
            if (y0 > lat) != (y1 > lat):
                xin = x0 + (lat - y0) * (x1 - x0) / (y1 - y0)
                if xin > lon:
                    inside = not inside
        if inside:
            return True
    return False


def draw_map(d, x0, y0, w, h):
    with open(os.path.join(HERE, "world.geo.json")) as fh:
        data = json.load(fh)
    polys = []
    for feat in data["features"]:
        geom = feat["geometry"]
        if geom is None:
            continue
        if geom["type"] == "Polygon":
            rings = [geom["coordinates"][0]]
        elif geom["type"] == "MultiPolygon":
            rings = [poly[0] for poly in geom["coordinates"]]
        else:
            continue
        for ring in rings:
            lons = [pt[0] for pt in ring]
            lats = [pt[1] for pt in ring]
            polys.append((ring, (min(lons), max(lons), min(lats), max(lats))))

    def px(lon):
        return x0 + (lon + 180) / 360 * w

    def py(lat):
        return y0 + (90 - lat) / 180 * h

    box(d, x0, y0, x0 + w, y0 + h, SEA)
    gy = 2
    while gy < h:
        lat = 90 - (gy / h) * 180
        gx = 2
        while gx < w:
            lon = (gx / w) * 360 - 180
            if _inside(lon, lat, polys):
                disc(d, x0 + gx, y0 + gy, 1.2, (150, 150, 150))
            gx += 3
        gy += 3
    for num, (lon, lat) in DOTS.items():
        tx = px(lon)
        ty = py(lat)
        if num in DOT_OFF:
            dx, dy = DOT_OFF[num]
            seg(d, [(tx, ty), (tx + dx, ty + dy)], BLACK, width=1)
            tx += dx
            ty += dy
        disc(d, tx, ty, 2, MIDNIGHT)
    for num, (lon, lat) in PINS.items():
        tx = px(lon)
        ty = py(lat)
        region = REGION_OF[num]
        if num in PIN_OFF:
            dx, dy = PIN_OFF[num]
            seg(d, [(tx, ty), (tx + dx, ty + dy)], REGION_COLOUR[region],
                width=1)
            tx += dx
            ty += dy
        disc(d, tx, ty, 7, REGION_COLOUR[region], outline=WHITE, width=1)
        txt(d, (tx, ty), str(num),
            TY["pin"] if num < 10 else TY["pinsm"], WHITE, anchor="mm")


# ---------------------------------------------------------------- page


def build():
    img, d = fresh(1024, 1024)
    box(d, 0, 0, 1023, 1023, BG)

    # top bar
    box(d, 0, 0, 1024, 18, MIDNIGHT)
    txt(d, (12, 9), "THE WORLD IN ONE DAY", TY["kick"], WHITE, anchor="lm")
    txt(d, (1012, 9), "29 STORIES · 7 REGIONS · ALL FROM THIS ONE DAY",
        TY["kick"], (238, 198, 110), anchor="rm")

    # masthead, scaled to the full width
    title = "Wednesday 25 November 2026"
    lw = d.textlength(title, font=TY["mastbold"]) + 12
    layer = Image.new("RGBA", (int(lw), 150), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((4, 0), title, font=TY["mastbold"], fill=BLACK + (255,),
            stroke_width=1, stroke_fill=BLACK + (255,))
    ink_top = layer.getbbox()[1]
    layer = layer.resize((996, 150), Image.LANCZOS)
    img.paste(layer, (12, 24 - ink_top), layer)

    # kicker, scaled to 1000 wide
    kick = ("Trump set to unveil new tariffs · Iranian tankers cross the "
            "blockade · Putin vows retaliation")
    klayer = Image.new("RGBA", (1100, 60), (0, 0, 0, 0))
    kd = ImageDraw.Draw(klayer)
    kd.text((0, 0), kick, font=TY["kickbold"], fill=SCARLET + (255,))
    kb = klayer.getbbox()
    klayer = klayer.crop(kb)
    klayer = klayer.resize((1000, kb[3] - kb[1]), Image.LANCZOS)
    img.paste(klayer, (12, 119), klayer)

    # region strip
    widths = []
    for name, count, _fill, _text in REGIONS:
        widths.append(int(d.textlength("%s %d" % (name, count),
                                       font=TY["strip"])) + 20)
    total = sum(widths) + 7 * 6
    sx = (1024 - total) // 2
    for (name, count, fill, text), w in zip(REGIONS, widths):
        box(d, sx, 150, sx + w, 168, fill)
        txt(d, (sx + w / 2, 159), "%s %d" % (name, count), TY["strip"],
            text, anchor="mm")
        sx += w + 7

    # UTC timeline
    box(d, 12, 172, 1012, 192, MIDNIGHT)
    box(d, 12, 175, 38, 189, SCARLET)
    txt(d, (25, 182), "UTC", TY["src"], WHITE, anchor="mm")
    events = [
        ("01:30", "Asian stocks tumble"),
        ("06:00", "Tankers cross blockade"),
        ("09:00", "Putin vows retaliation"),
        ("11:00", "Cikande search goes on"),
        ("14:30", "Nvidia slides 6%"),
        ("19:00", "Confidence hits 103.3"),
    ]
    sep = "  ·  "
    sepw = int(d.textlength(sep, font=TY["tl"]))
    natural = 0
    for time, event in events:
        natural += int(d.textlength(time, font=TY["tl"]))
        natural += int(d.textlength(" " + event, font=TY["tlev"]))
    natural += sepw * 5
    extra = (1012 - (12 + 34)) - natural
    gap = extra // 5
    rem = extra % 5
    tx = 46
    for i, (time, event) in enumerate(events):
        txt(d, (tx, 182), time, TY["tl"], GILT, anchor="lm")
        tx += int(d.textlength(time, font=TY["tl"]))
        txt(d, (tx, 182), " " + event, TY["tlev"], WHITE, anchor="lm")
        tx += int(d.textlength(" " + event, font=TY["tlev"]))
        if i < len(events) - 1:
            txt(d, (tx, 182), sep, TY["tl"], GILT, anchor="lm")
            tx += sepw + gap + (1 if i < rem else 0)

    # heroes + numbers box
    hx = 12
    for story in FRONT[:3]:
        hero_card(img, d, story, hx, HY, HW)
        hx += 268
    numbers_box(d, hx, HY)

    # small cards, two rows of five
    for r in range(2):
        for c in range(5):
            story = FRONT[3 + r * 5 + c]
            small_card(img, d, story, 12 + c * 204, SY + r * SR)

    # also list
    txt(d, (12, MY), "ALSO ON WEDNESDAY 25 NOVEMBER", TY["sect"], BLACK)
    _px = 652
    for name, colour in [("ONGOING", AZURE), ("CLAIM", TANGERINE),
                         ("REPORTED", LEAF)]:
        pw = int(d.textlength(name, font=TY["tag"])) + 12
        x0 = _px - pw
        d.rounded_rectangle([x0, 767, _px, 781], radius=2, fill=colour)
        txt(d, (x0 + pw / 2, 774), name, TY["tag"], WHITE, anchor="mm")
        _px = x0 - 6
    txt(d, (_px - 6, MY), "16 MORE STORIES", TY["sect"], BLACK, anchor="ra")
    seg(d, [(12, 784), (652, 784)], BLACK, width=1)
    for num, city, head, media in ALSO:
        if num <= 19:
            col, row = 0, num - 14
        elif num <= 24:
            col, row = 1, num - 20
        else:
            col, row = 2, num - 25
        x = 12 + col * 220
        y = MY + 18 + row * 24
        txt(d, (x, y), "%d." % num, TY["alsonum"],
            REGION_COLOUR[ALSO_REGION[num]])
        flag(d, FLAG_OF[num], x + 20, y, 16, 11)
        lines = wrap(d, "%s: %s" % (city, head), TY["also10"], 160, cap=1)
        if lines:
            txt(d, (x + 40, y), lines[0], TY["also10"], BLACK)
        txt(d, (x + 40, y + 11), "%s · %s" % (ALSO_SUB[num].removesuffix("."),
                                              media),
            TY["alsosub7"], ASH)

    # map panel
    box(d, 680, MY, 1012, 938, SEA)
    d.rectangle([680, MY, 1012, 938], outline=EDGE, width=1)
    draw_map(d, 680, 790, 332, 148)
    txt(d, (688, 776), "WHERE IT HAPPENED", TY["sect"], BLACK)
    txt(d, (1004, 776), "pins = story numbers", TY["src"], ASH, anchor="ra")

    # date check
    d.rectangle([12, CY, 1012, 992], outline=SCARLET, width=2)
    box(d, 20, 945, 115, 959, SCARLET)
    txt(d, (67, 952), "DATE CHECK", TY["src"], WHITE, anchor="mm")
    draw_segs(d, 123, 946, [
        ("Every story here happened or was first reported on Wednesday "
         "25 November 2026 (UTC). ", BLACK),
        ("Left out because they happened on an earlier day:", SCARLET),
    ], TY["chk"])
    draw_segs(d, 20, 960, [
        ("COP31 collapse · Libya sinking — ", BLACK),
        ("Sun 22 Nov", SCARLET),
        (" · House 258 seats — ", BLACK),
        ("Mon 23 Nov", SCARLET),
        (" · Nepal PM visit — ", BLACK),
        ("22–23 Nov", SCARLET),
        (" · Shenzhou-24 crew — ", BLACK),
        ("Mon 23 Nov", SCARLET),
        (".", BLACK),
    ], TY["chk"])
    draw_segs(d, 20, 974, [
        ("Not yet confirmed: ", SCARLET),
        ("Iran tanker-crossing claim · Cikande missing count · "
         "GPS-jamming culprit.", BLACK),
    ], TY["chk"])

    # footer
    txt(d, (512, FY), "Sources: Reuters · AP · AFP · SCMP · Al Jazeera · "
        "BBC · Guardian · Detik · Xinhua · IANS · Yonhap · ABC · ESPN · "
        "UKMTO · WHO · Corrections: none", TY["foot"], ASH, anchor="ma")
    txt(d, (20, 1007), "HOW SURE: ", TY["foot"], SCARLET)
    x2 = 20 + int(d.textlength("HOW SURE: ", font=TY["foot"]))
    txt(d, (x2, 1007), "REPORTED = carried by the day's wires or "
        "officials · CLAIM = one side's account, labelled as such · "
        "ONGOING = still unfolding · Scenes are drawn illustrations, "
        "not photographs.", TY["foot"], BLACK)

    return img


def main():
    img = build()
    path = os.path.join(HERE, "entry.png")
    img.save(path)
    print("saved", path, os.path.getsize(path), "bytes")
    if ISSUES:
        print("ISSUES:")
        for note in ISSUES:
            print(" -", note)
    else:
        print("no truncation")


if __name__ == "__main__":
    main()

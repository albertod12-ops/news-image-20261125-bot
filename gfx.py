"""Shared drawing helpers for the front-page renderer and the scene art.

Colours, the font table, small shape/text helpers, the greedy text
wrapper, the ten-point star, tiny flat flags, and the blank-canvas
factory all live here so draw.py and art.py can import them.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

NOTO = "/usr/share/fonts/truetype/noto"
LIBER = "/usr/share/fonts/truetype/liberation"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

BG = (247, 242, 231)
PANEL = (253, 250, 242)
BLACK = (17, 17, 17)
BLUE = (16, 62, 150)
MIDNIGHT = (12, 28, 58)
SCARLET = (220, 28, 60)
WINE = (179, 34, 44)
GILT = (232, 178, 36)
ASH = (90, 90, 90)
EDGE = (180, 170, 150)
SEA = (235, 240, 243)
SHORE = (238, 220, 165)
LEAF = (16, 165, 90)
TANGERINE = (230, 150, 0)
AZURE = (20, 110, 230)
TEAL = (0, 110, 160)
DOTGREY = (70, 70, 70)

WHITE = (255, 255, 255)

PILL = {
    "CONFIRMED": LEAF,
    "REPORTED": LEAF,
    "FORECAST": AZURE,
    "CLAIM": TANGERINE,
    "OFFICIAL": TEAL,
    "ONGOING": TANGERINE,
}

ISSUES = []


def load_font(name, size, folder):
    return ImageFont.truetype(os.path.join(folder, name), size)


load = load_font


def _faces():
    spec = [
        ("mast", "NotoSerifDisplay-Black.ttf", 88, NOTO),
        ("mastbold", "NotoSerifDisplay-Bold.ttf", 88, NOTO),
        ("kick", "NotoSans-Black.ttf", 10, NOTO),
        ("kickbold", "LiberationSerif-BoldItalic.ttf", 23, LIBER),
        ("clock", "NotoSans-Bold.ttf", 12, NOTO),
        ("clocksm", "NotoSans-Bold.ttf", 11, NOTO),
        ("tl", "NotoSans-Bold.ttf", 11, NOTO),
        ("tlev", "NotoSans-Regular.ttf", 11, NOTO),
        ("strip", "NotoSans-Bold.ttf", 12, NOTO),
        ("stripsm", "NotoSans-Bold.ttf", 9, NOTO),
        ("striptn", "NotoSans-Bold.ttf", 8, NOTO),
        ("tag", "NotoSans-Bold.ttf", 8, NOTO),
        ("src", "NotoSans-Bold.ttf", 9, NOTO),
        ("hhead", "LiberationSerif-Bold.ttf", 25, LIBER),
        ("shead", "LiberationSerif-Bold.ttf", 17, LIBER),
        ("hdeck", "LiberationSerif-Regular.ttf", 12, LIBER),
        ("sdeck", "LiberationSerif-Regular.ttf", 11, LIBER),
        ("pin", "NotoSans-Bold.ttf", 11, NOTO),
        ("pinsm", "NotoSans-Bold.ttf", 9, NOTO),
        ("abig", "NotoSans-Black.ttf", 24, NOTO),
        ("asmall", "NotoSans-Bold.ttf", 12, NOTO),
        ("amid", "NotoSans-Black.ttf", 17, NOTO),
        ("amidsm", "NotoSans-Bold.ttf", 11, NOTO),
        ("hlab", "NotoSans-Black.ttf", 16, NOTO),
        ("hlabsm", "NotoSans-Bold.ttf", 9, NOTO),
        ("slab", "NotoSans-Bold.ttf", 12, NOTO),
        ("slab10", "NotoSans-Bold.ttf", 10, NOTO),
        ("slabssm", "NotoSans-Bold.ttf", 8, NOTO),
        ("also", "NotoSans-Bold.ttf", 11, NOTO),
        ("also10", "NotoSans-Bold.ttf", 10, NOTO),
        ("alsosub", "NotoSans-Regular.ttf", 8, NOTO),
        ("alsosub7", "NotoSans-Regular.ttf", 7, NOTO),
        ("alsonum", "NotoSans-Bold.ttf", 11, NOTO),
        ("sect", "NotoSans-Black.ttf", 13, NOTO),
        ("chk", "NotoSans-Bold.ttf", 12, NOTO),
        ("foot", "NotoSans-Bold.ttf", 10, NOTO),
        ("numbig", "NotoSans-Black.ttf", 26, NOTO),
        ("numlab", "NotoSans-Bold.ttf", 10, NOTO),
        ("numtitle", "NotoSans-Black.ttf", 12, NOTO),
        ("topic", "NotoSans-Bold.ttf", 11, NOTO),
        ("topicsm", "NotoSans-Bold.ttf", 9, NOTO),
        ("bignum", "NotoSans-Black.ttf", 30, NOTO),
    ]
    return {key: load_font(name, size, folder) for key, name, size, folder in spec}


class _FontTable:
    """Font faces reachable both as attributes and as items.

    art.py reads faces as attributes (TY.slabssm) while draw.py
    reads them as items (TY["slab"]), so the table supports both.
    """

    def __init__(self, faces):
        self.__dict__.update(faces)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__


TY = _FontTable(_faces())


def box(d, x0, y0, x1, y1, fill):
    d.rectangle([x0, y0, x1, y1], fill=fill)


def disc(d, cx, cy, r, fill, outline=None, width=1):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def ring(d, x0, y0, x1, y1, outline, width=1):
    d.ellipse([x0, y0, x1, y1], outline=outline, width=width)


def seg(d, pts, fill, width=1):
    d.line(pts, fill=fill, width=width)


def poly(d, pts, fill, outline=None):
    d.polygon(pts, fill=fill, outline=outline)


def txt(d, xy, s, font, fill, anchor=None, stroke=0, stroke_fill=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=stroke_fill)


def draw_segs(d, x, y, segs, font):
    for s, col in segs:
        txt(d, (x, y), s, font, col)
        x += int(d.textlength(s, font=font))
    return x


def wrap(d, text, font, width, cap=None):
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if cap is not None and len(lines) > cap:
        ISSUES.append("TRUNCATED (%d lines): %s" % (len(lines), text))
        lines = lines[:cap]
    return lines


def burst(d, cx, cy, outer, inner, fill):
    pts = []
    for k in range(10):
        r = outer if k % 2 == 0 else inner
        ang = math.radians(-90 + k * 36)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    poly(d, pts, fill)


def fresh(w, h):
    img = Image.new("RGB", (w, h))
    return img, ImageDraw.Draw(img)


def flag(d, code, x, y, w=16, h=11):
    def hband(y0, y1, col):
        box(d, x, y + y0, x + w, y + y1, col)

    def vband(x0, x1, col):
        box(d, x + x0, y, x + x1, y + h, col)

    if code == "TR":
        red = (227, 10, 23)
        box(d, x, y, x + w, y + h, red)
        disc(d, x + 6, y + h // 2, 3, WHITE)
        disc(d, x + 7, y + h // 2, 2, red)
        star = [(x + 11, y + 3), (x + 12, y + 5), (x + 14, y + 5),
                (x + 12, y + 6), (x + 13, y + 8), (x + 11, y + 7),
                (x + 9, y + 8), (x + 10, y + 6), (x + 8, y + 5),
                (x + 10, y + 5)]
        poly(d, star, WHITE)
    elif code == "SA":
        box(d, x, y, x + w, y + h, (0, 106, 68))
        box(d, x + 2, y + 3, x + w - 2, y + 5, WHITE)
        box(d, x + 3, y + 7, x + w - 3, y + 8, WHITE)
    elif code == "IR":
        hband(0, h // 3, (0, 122, 61))
        hband(h // 3, 2 * h // 3, WHITE)
        hband(2 * h // 3, h, (218, 0, 0))
    elif code == "US":
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else WHITE
            hband(i * h // 7, (i + 1) * h // 7, col)
        box(d, x, y, x + w * 2 // 5, y + h * 4 // 7, (60, 59, 110))
        for dx, dy in [(2, 2), (6, 2), (10, 2), (2, 5), (6, 5), (10, 5)]:
            disc(d, x + dx, y + dy, 1, WHITE)
    elif code == "UA":
        hband(0, h // 2, (0, 91, 187))
        hband(h // 2, h, (255, 213, 0))
    elif code == "GB":
        box(d, x, y, x + w, y + h, (0, 36, 125))
        seg(d, [(x, y), (x + w, y + h)], WHITE, width=2)
        seg(d, [(x + w, y), (x, y + h)], WHITE, width=2)
        box(d, x + w // 2 - 1, y, x + w // 2 + 1, y + h, (200, 16, 46))
        box(d, x, y + h // 2 - 1, x + w, y + h // 2 + 1, (200, 16, 46))
    elif code == "BD":
        box(d, x, y, x + w, y + h, (0, 106, 78))
        disc(d, x + w // 2 - 1, y + h // 2, 4, (244, 42, 65))
    elif code == "AU":
        box(d, x, y, x + w, y + h, (0, 47, 108))
        box(d, x, y, x + w // 2, y + h // 2, (0, 36, 125))
        seg(d, [(x, y), (x + w // 2, y + h // 2)], WHITE, width=1)
        seg(d, [(x + w // 2, y), (x, y + h // 2)], WHITE, width=1)
        box(d, x + w // 4 - 1, y, x + w // 4 + 1, y + h // 2, (200, 16, 46))
        box(d, x, y + h // 4 - 1, x + w // 2, y + h // 4 + 1, (200, 16, 46))
        for dx, dy in [(w * 3 // 4, h // 4), (w * 3 // 4, h * 3 // 4),
                       (w * 7 // 8, h // 2)]:
            disc(d, x + dx, y + dy, 1, WHITE)
    elif code == "SS":
        hband(0, h // 3, (0, 0, 0))
        hband(h // 3, 2 * h // 3, (218, 41, 28))
        hband(2 * h // 3, h, (0, 122, 61))
        poly(d, [(x, y), (x, y + h), (x + w // 2, y + h // 2)], (0, 63, 135))
        disc(d, x + 4, y + h // 2, 1, (255, 210, 0))
    elif code == "CD":
        box(d, x, y, x + w, y + h, (0, 91, 187))
        seg(d, [(x, y + h), (x + w, y)], (206, 16, 33), width=3)
        disc(d, x + 4, y + 3, 1, (255, 210, 0))
    elif code == "PT":
        vband(0, w * 2 // 5, (0, 122, 61))
        vband(w * 2 // 5, w, (200, 16, 46))
    elif code == "MM":
        hband(0, h // 3, (254, 203, 0))
        hband(h // 3, 2 * h // 3, (52, 138, 71))
        hband(2 * h // 3, h, (234, 40, 42))
        disc(d, x + w // 2, y + h // 2, 2, WHITE)
    elif code == "PL":
        hband(0, h // 2, WHITE)
        hband(h // 2, h, (220, 20, 60))
    elif code == "BE":
        vband(0, w // 3, (0, 0, 0))
        vband(w // 3, 2 * w // 3, (253, 218, 0))
        vband(2 * w // 3, w, (237, 41, 57))
    elif code == "KR":
        box(d, x, y, x + w, y + h, WHITE)
        disc(d, x + w // 2, y + h // 2, 3, (205, 0, 0))
        disc(d, x + w // 2, y + h // 2 + 1, 2, (0, 50, 140))
        for tx, ty in [(1, 1), (w - 4, 1), (1, h - 3), (w - 4, h - 3)]:
            box(d, x + tx, y + ty, x + tx + 3, y + ty + 1, (0, 0, 0))
    elif code == "CN":
        box(d, x, y, x + w, y + h, (222, 0, 0))
        disc(d, x + 4, y + 3, 2, (255, 220, 0))
        for dx, dy in [(10, 2), (12, 4), (12, 6), (10, 8)]:
            disc(d, x + dx, y + dy, 1, (255, 220, 0))
    elif code == "DE":
        hband(0, h // 3, (0, 0, 0))
        hband(h // 3, 2 * h // 3, (220, 0, 0))
        hband(2 * h // 3, h, (255, 210, 0))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)

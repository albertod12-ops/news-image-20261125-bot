#!/usr/bin/env python3
"""Vector scene illustrations for the front page.

Kept from the v1.2 template: each scene is drawn from flat
vector shapes. The shared drawing helpers, colours and type
faces live in gfx.py; this module only defines the scenes.
"""
import math

from PIL import Image

from gfx import *


def art(key, w, h):
    """One picture, flat vector shapes drawn from scratch.
    Leads paint at h=105; smalls paint at h=80 then shrink to 60.
    A lead's bottom-left stays clear for its tag; a small's top
    18px stays clear for its number+place bar."""
    img, d = fresh(w, h)
    if key == "copcollapse":
        # Lead 1: the climate talks fail. Teal hall, round globe,
        # thermometer past the mark, a torn page, a NO DEAL band.
        # The compact place label now sits top-left inside the
        # picture, so the top is kept clear for it: the globe and
        # the thermometer sit lower (tops at y26+), and the wall
        # clock moved to the top-right, clear of the torn page.
        box(d, 0, 0, w, h, (11, 110, 110))
        disc(d, 51, 58, 31, (30, 120, 200), outline=(20, 20, 20), width=2)
        for a, b, c, e in ((30, 39, 52, 53), (52, 55, 74, 71),
                           (30, 59, 44, 71)):
            d.ellipse((a, b, c, e), fill=(60, 180, 90))
        seg(d, [(22, 58), (80, 58)], "white", 1)
        box(d, 132, 26, 142, 74, "white")
        d.rectangle((132, 26, 142, 74), outline=(20, 20, 20))
        box(d, 134, 28, 140, 74, (220, 30, 40))
        disc(d, 137, 78, 11, (220, 30, 40), outline=(20, 20, 20), width=2)
        for ty in (32, 40, 48, 56, 64):
            seg(d, [(142, ty), (147, ty)], (20, 20, 20))
        txt(d, (154, 28), "+1.5°C", TY.amid, "white")
        txt(d, (154, 50), "LIMIT", TY.amidsm, "white")
        txt(d, (154, 62), "PASSED", TY.amidsm, "white")
        box(d, 228, 22, 256, 78, "white")
        d.rectangle((228, 22, 256, 78), outline=(20, 20, 20), width=2)
        for ly in (32, 42, 52):
            seg(d, [(236, ly), (248, ly)], (60, 60, 60), 2)
        seg(d, [(228, 22), (222, 40), (230, 56), (224, 78)], SCARLET, 3)
        # NO DEAL band moved to the bottom-left so the bottom-right
        # stays clear for the REPORTED pill (bagarte).
        box(d, 8, 84, 108, 102, WINE)
        txt(d, (58, 93), "NO DEAL", TY.amid, "white", anchor="mm")
        # wall clock top-right and delegates lower-right: a scene
        # with people, not just icons. The delegates sit LOW (heads
        # y80, bodies y87-96) so they clear "PASSED" (ends y73),
        # the thermometer bulb (x126-148) and the NO DEAL band
        # (x<108); the rightmost body ends at x196, clear of the
        # REPORTED pill (x198+).
        disc(d, 205, 14, 9, "white", outline=(20, 20, 20), width=1)
        seg(d, [(205, 14), (205, 7)], (20, 20, 20), 1)
        seg(d, [(205, 14), (210, 16)], (20, 20, 20), 1)
        for fx, shirt in ((152, (200, 60, 40)), (168, (40, 90, 160)),
                          (184, (240, 200, 60))):
            disc(d, fx + 6, 80, 5, (220, 180, 140))
            poly(d, [(fx, 96), (fx + 12, 96), (fx + 10, 87),
                     (fx + 2, 87)], shirt)
    elif key == "gulfwar":
        # Lead 2: the Gulf at war, as a map. Iran coast on top,
        # Arabian coast below, Bahrain with two base bursts, dashed
        # missile arcs, a burning tanker, a 5th Fleet destroyer.
        box(d, 0, 0, w, h, (14, 48, 96))
        poly(d, [(0, 0), (w, 0), (w, 14), (240, 16), (180, 12),
                 (120, 16), (60, 14), (0, 18)], (214, 196, 150))
        # "IRAN" moved right so the compact place label (top-left
        # inside the picture) does not cover it.
        txt(d, (170, 4), "IRAN", TY.amidsm, BLACK)
        poly(d, [(0, h), (0, 82), (70, 74), (140, 82), (210, 76),
                 (260, 82), (w, 72), (w, h)], (214, 196, 150))
        # SAUDI ARABIA sits bottom-left now, so the bottom-right
        # stays clear for the REPORTED pill (bagarte).
        txt(d, (8, 90), "SAUDI ARABIA", TY.amidsm, BLACK, anchor="la")
        d.ellipse((120, 30, 152, 52), fill=(214, 196, 150))
        d.ellipse((176, 44, 196, 62), fill=(196, 176, 128))
        for ax0, ay0, ax1, ay1, hump in ((0, 22, 128, 38, 12),
                                         (0, 48, 136, 44, 14)):
            for ti in range(21):
                t = ti / 20
                qx = ax0 + (ax1 - ax0) * t
                qy = ay0 + (ay1 - ay0) * t - hump * math.sin(math.pi * t)
                if ti % 2 == 0:
                    disc(d, qx, qy, 2, "white")
        for bx, by in ((128, 36), (144, 46)):
            burst(d, bx, by, 10, 4, (255, 200, 60))
            burst(d, bx, by, 5, 2, (255, 140, 40))
            disc(d, bx, by, 3, "white")
            ring(d, bx - 8, by - 8, bx + 8, by + 8, "white", 1)
        # burning tanker, right of the island
        poly(d, [(180, 60), (232, 60), (224, 68), (188, 68)], (30, 30, 40))
        box(d, 188, 48, 202, 60, "white")
        burst(d, 212, 44, 9, 4, (255, 140, 40))
        burst(d, 212, 44, 5, 2, (255, 210, 31))
        for lx, ly, s, anch in ((136, 56, "BAHRAIN", "ma"),
                                (170, 28, "THE GULF", "ma")):
            txt(d, (lx, ly), s, TY.amidsm, "white", anchor=anch,
                stroke=1, stroke_fill=(0, 0, 0))
        poly(d, [(200, 34), (248, 34), (240, 42), (208, 42)],
             (120, 125, 135))
        box(d, 214, 26, 226, 34, (120, 125, 135))
        seg(d, [(220, 26), (220, 20)], (120, 125, 135), 2)
        seg(d, [(196, 44), (252, 44)], "white")
        txt(d, (224, 50), "5TH FLEET", TY.amidsm, "white", anchor="ma",
            stroke=1, stroke_fill=(0, 0, 0))
        # sea texture, a second vessel, a radar mast on Bahrain,
        # and smoke over the burning tanker.
        for wx in range(8, 168, 26):
            seg(d, [(wx, 68), (wx + 12, 68)], (180, 200, 220), 1)
        poly(d, [(28, 58), (58, 58), (52, 64), (34, 64)], (90, 95, 105))
        box(d, 38, 50, 48, 58, (120, 125, 135))
        seg(d, [(43, 50), (43, 44)], (120, 125, 135), 2)
        seg(d, [(136, 30), (136, 18)], (60, 60, 60), 2)
        seg(d, [(130, 18), (142, 14)], (60, 60, 60), 2)
        for sx, sy, sr in ((196, 36, 5), (190, 30, 6), (198, 26, 4)):
            disc(d, sx, sy, sr, (120, 120, 126))
    elif key == "house258":
        # Lead 3: the US House flips. Navy hall, white Capitol dome
        # with columns and a gold cupola, seat bar bottom-right:
        # 258 blue against 177 red. The dome assembly sits 20px
        # right of centre so the compact place label (top-left
        # inside the picture) does not cover the cupola; the flag
        # moved down so its top clears the label box.
        box(d, 0, 0, w, h, MIDNIGHT)
        for sx, sy in ((22, 30), (70, 30), (210, 30), (280, 30),
                       (340, 30), (378, 30)):
            disc(d, sx, sy, 1, "white")
        d.ellipse((119, 20, 215, 68), fill="white")
        box(d, 117, 48, 217, 66, "white")
        for cx in (132, 152, 172, 192, 212):
            seg(d, [(cx, 48), (cx, 66)], MIDNIGHT, 2)
        box(d, 107, 66, 227, 70, "white")
        box(d, 143, 12, 191, 26, "white")
        disc(d, 167, 11, 12, GILT)
        # Seat bar moved left and narrowed so the bottom-right stays
        # clear for the REPORTED pill (bagarte): blue 258, red 177.
        box(d, 85, 82, 157, 96, (40, 90, 200))
        box(d, 157, 82, 205, 96, (200, 40, 50))
        txt(d, (121, 89), "258", TY.amidsm, "white", anchor="mm")
        txt(d, (181, 89), "177", TY.amidsm, "white", anchor="mm")
        txt(d, (250, 8), "SINCE 1992", TY.amidsm, GILT, anchor="ra")
        # a flag on the left, steps under the dome, and windows on
        # the dome: a fuller scene.
        seg(d, [(30, 24), (30, 72)], (200, 200, 210), 2)
        box(d, 30, 24, 58, 36, (200, 40, 50))
        for sy in (28, 32):
            seg(d, [(30, sy), (58, sy)], "white", 1)
        box(d, 30, 24, 42, 30, (40, 60, 140))
        disc(d, 36, 27, 1, "white")
        for sy in (73, 77, 81):
            seg(d, [(105, sy), (230, sy)], (180, 180, 190), 2)
        for wx, wy in ((140, 40), (167, 35), (194, 40)):
            disc(d, wx, wy, 2, MIDNIGHT)
    elif key == "shipfire":
        # Sparta II ablaze off Finland: grey sea, dark cargo ship,
        # container stack, white bridge, deck fire, two drones.
        box(d, 0, 0, w, h, (30, 90, 140))
        seg(d, [(0, 56), (w, 56)], (140, 180, 210))
        poly(d, [(28, 56), (168, 56), (158, 68), (38, 68)], (30, 30, 40))
        box(d, 40, 40, 64, 56, "white")
        for cx, col in ((76, (200, 60, 40)), (100, (40, 140, 90)),
                        (124, (230, 180, 40))):
            box(d, cx, 44, cx + 20, 56, col)
        burst(d, 92, 40, 9, 4, (255, 140, 40))
        burst(d, 92, 40, 5, 2, (255, 210, 31))
        for dx, dy in ((60, 26), (140, 24)):
            d.ellipse((dx - 5, dy - 3, dx + 5, dy + 3), fill=(90, 95, 105))
            seg(d, [(dx - 8, dy - 5), (dx + 8, dy - 5)], (200, 200, 210), 2)
            seg(d, [(dx, dy + 3), (dx, dy + 8)], (200, 200, 210))
        seg(d, [(20, 72), (176, 72)], "white")
    elif key == "sinking":
        # Russian warship sinking off Libya: dark sea, grey warship
        # listing hard, bow under, smoke, a drone above.
        box(d, 0, 0, w, h, (20, 60, 110))
        seg(d, [(0, 58), (w, 58)], (140, 180, 210))
        poly(d, [(40, 58), (150, 58), (160, 46), (120, 52), (60, 52)],
             (90, 95, 105))
        box(d, 96, 38, 118, 52, (120, 125, 135))
        seg(d, [(107, 38), (107, 28)], (120, 125, 135), 2)
        for sx, sy, sr in ((128, 30, 8), (140, 22, 10), (152, 16, 7)):
            disc(d, sx, sy, sr, (120, 120, 126))
        burst(d, 84, 48, 8, 3, (255, 140, 40))
        for wx in range(0, w, 24):
            seg(d, [(wx, 66), (wx + 12, 66)], "white")
        # drone moved right so the compact place label (top-left
        # inside the picture) does not cover it.
        d.ellipse((150, 20, 160, 26), fill=(90, 95, 105))
        seg(d, [(142, 18), (158, 18)], (200, 200, 210), 2)
    elif key == "factoryfire":
        # Candy-factory fire in Cikande: sawtooth roof, fire bursting
        # through, smoke drifting right, one glowing window.
        box(d, 0, 0, w, h, (180, 190, 205))
        box(d, 0, 62, w, h, (120, 120, 126))
        box(d, 20, 44, 176, 62, (90, 90, 100))
        for sx in (20, 52, 84, 116, 148):
            poly(d, [(sx, 44), (sx + 16, 32), (sx + 32, 44)], (70, 70, 80))
        box(d, 168, 24, 176, 44, (70, 70, 80))
        disc(d, 98, 36, 20, (255, 140, 40))
        disc(d, 98, 40, 10, (255, 210, 31))
        disc(d, 99, 44, 5, (255, 120, 30))
        for sx, sy, sr in ((98, 16, 7), (112, 10, 9), (130, 8, 8),
                           (146, 12, 6)):
            disc(d, sx, sy, sr, (90, 90, 96))
        for wx in (30, 56, 130, 156):
            box(d, wx, 50, wx + 10, 58, (40, 40, 50))
        box(d, 82, 50, 92, 58, (255, 180, 60))
    elif key == "statevisit":
        # Nepal PM lands on a state visit: plane on the runway,
        # two flags on poles.
        box(d, 0, 0, w, h, (200, 220, 235))
        box(d, 0, 58, w, h, (90, 90, 98))
        for dx in range(6, w, 22):
            seg(d, [(dx, 66), (dx + 11, 66)], "white", 2)
        for fx, cols in ((24, ((255, 150, 0), "white", (0, 130, 60))),
                         (164, ((200, 30, 50), (20, 60, 140), None))):
            seg(d, [(fx, 24), (fx, 58)], (60, 60, 60), 2)
            box(d, fx, 24, fx + 22, 32, cols[0])
            box(d, fx, 32, fx + 22, 40, cols[1])
            if cols[2]:
                box(d, fx, 40, fx + 22, 48, cols[2])
        d.ellipse((70, 44, 132, 54), fill=(40, 90, 160))
        poly(d, [(124, 46), (132, 38), (136, 46)], (40, 90, 160))
        poly(d, [(84, 52), (94, 62), (98, 52)], (40, 90, 160))
        for wx in (84, 118):
            disc(d, wx, 58, 4, (20, 20, 20))
    elif key == "chip":
        # Nvidia pressed on chips diverted to China: dark board, big
        # green AI chip with gold pins, red arrow to a red flag.
        box(d, 0, 0, w, h, (16, 24, 44))
        for ty in range(24, h, 14):
            seg(d, [(0, ty), (w, ty)], (30, 40, 60))
        box(d, 30, 26, 78, 62, (16, 140, 80))
        d.rectangle((30, 26, 78, 62), outline=(60, 200, 120), width=2)
        for px in (36, 48, 60, 72):
            seg(d, [(px, 22), (px, 26)], GILT, 2)
            seg(d, [(px, 62), (px, 66)], GILT, 2)
        for py in (32, 44, 56):
            seg(d, [(26, py), (30, py)], GILT, 2)
            seg(d, [(78, py), (82, py)], GILT, 2)
        txt(d, (54, 44), "AI", TY.amid, "white", anchor="mm")
        seg(d, [(84, 44), (120, 30), (150, 36)], SCARLET, 3)
        poly(d, [(150, 36), (140, 30), (140, 42)], SCARLET)
        box(d, 156, 26, 186, 46, (200, 30, 40))
        burst(d, 171, 36, 6, 2, (255, 210, 31))
        txt(d, (54, 74), "WHERE DID THEY GO?", TY.slabssm, "white",
            anchor="ma")
    elif key == "sanctions":
        # US sanctions Iranian shadow banking: a ledger page, a red
        # stamp, a chain of blocked accounts.
        box(d, 0, 0, w, h, (220, 215, 200))
        box(d, 0, 62, w, h, (90, 85, 70))
        poly(d, [(60, 18), (136, 22), (132, 66), (56, 62)], "white",
             outline=(60, 60, 60))
        for ly in (30, 38, 46, 54):
            seg(d, [(66, ly), (126, ly + 1)], ASH)
        for xx in (120, 108):
            seg(d, [(xx - 4, 30 - 4), (xx + 4, 30 + 4)], SCARLET, 2)
            seg(d, [(xx + 4, 30 - 4), (xx - 4, 30 + 4)], SCARLET, 2)
        d.ellipse((140, 20, 184, 52), outline=SCARLET, width=3)
        txt(d, (162, 36), "TARIFFS", TY.slabssm, SCARLET, anchor="mm")
        for cx in (40, 100, 160):
            disc(d, cx, 56, 5, (40, 40, 50))
            box(d, cx - 3, 61, cx + 3, 74, (40, 40, 50))
        seg(d, [(45, 56), (95, 56)], (40, 40, 50), 2)
        seg(d, [(105, 56), (155, 56)], (40, 40, 50), 2)
    elif key == "oil":
        # Oil slides as Gulf attacks continue: a dark barrel, a red
        # falling arrow, a price line dropping.
        box(d, 0, 0, w, h, (20, 30, 50))
        for gy in range(14, h, 12):
            seg(d, [(0, gy), (w, gy)], (35, 45, 65))
        d.ellipse((24, 26, 76, 74), fill=(30, 35, 45),
                  outline=(120, 125, 135), width=2)
        seg(d, [(24, 38), (76, 38)], (120, 125, 135), 2)
        seg(d, [(24, 56), (76, 56)], (120, 125, 135), 2)
        txt(d, (50, 50), "OIL", TY.amid, "white", anchor="mm")
        seg(d, [(96, 22), (130, 40), (160, 34), (188, 58)], SCARLET, 3)
        poly(d, [(188, 58), (178, 56), (184, 66)], SCARLET)
    elif key == "resign":
        # Gomez to quit after an ethics report: an empty chair, a
        # closing door, a gavel on the desk.
        box(d, 0, 0, w, h, (200, 200, 210))
        box(d, 0, 60, w, h, (120, 110, 100))
        # door moved down so its top clears the compact place
        # label (top-left inside the picture).
        box(d, 30, 26, 90, 60, (90, 60, 40))
        d.rectangle((30, 26, 90, 60), outline=(60, 40, 20), width=2)
        disc(d, 78, 43, 4, GILT)
        box(d, 110, 26, 170, 60, (150, 140, 130))
        d.rectangle((110, 26, 170, 60), outline=(90, 80, 70), width=2)
        box(d, 118, 34, 140, 52, (200, 200, 210))
        seg(d, [(118, 43), (140, 43)], (60, 60, 60), 2)
        seg(d, [(150, 30), (150, 56)], (60, 60, 60), 2)
        poly(d, [(60, 62), (76, 62), (72, 76), (64, 76)], (60, 40, 20))
        box(d, 56, 76, 80, 79, (60, 40, 20))
    elif key == "space":
        # China names the Shenzhou-24 crew: night sky, a rocket
        # climbing, a station ring, stars.
        box(d, 0, 0, w, h, (8, 12, 30))
        for sx, sy in ((20, 14), (60, 10), (110, 16), (160, 12),
                       (185, 20), (40, 30), (140, 28)):
            disc(d, sx, sy, 1, "white")
        # rocket + station shifted down 6px so the rocket tip
        # clears the compact place label (top-left inside the
        # picture).
        poly(d, [(92, 26), (104, 26), (108, 54), (88, 54)], "white")
        poly(d, [(98, 14), (104, 26), (92, 26)], SCARLET)
        poly(d, [(88, 54), (80, 66), (88, 60)], (200, 200, 210))
        poly(d, [(108, 54), (116, 66), (108, 60)], (200, 200, 210))
        burst(d, 98, 68, 8, 3, (255, 180, 60))
        ring(d, 140, 36, 180, 68, GILT, 2)
        disc(d, 160, 52, 6, GILT)
        txt(d, (160, 52), "24", TY.slabssm, BLACK, anchor="mm")
    elif key == "handshake":
        # Kenya and DR Congo restore ties: two flags on poles, two
        # hands meeting in the middle.
        box(d, 0, 0, w, h, (200, 220, 235))
        box(d, 0, 58, w, h, (90, 90, 98))
        # flags moved down so their tops clear the compact place
        # label (top-left inside the picture).
        for fx, cols in ((20, ((0, 0, 0), (200, 30, 40), (0, 130, 60))),
                         (150, ((0, 60, 160), (255, 210, 31), (200, 30, 40)))):
            seg(d, [(fx, 26), (fx, 58)], (60, 60, 60), 2)
            box(d, fx, 26, fx + 24, 34, cols[0])
            box(d, fx, 34, fx + 24, 42, cols[1])
            box(d, fx, 42, fx + 24, 50, cols[2])
        poly(d, [(70, 40), (98, 34), (104, 40), (98, 46), (76, 48)],
             (200, 170, 140), outline=(120, 90, 60))
        poly(d, [(126, 40), (98, 34), (92, 40), (98, 46), (120, 48)],
             (220, 190, 160), outline=(120, 90, 60))
        seg(d, [(70, 40), (126, 40)], (120, 90, 60), 2)
    elif key == "kurdoil":
        # Baghdad moves on Kurdish oilfields: desert sky, a derrick
        # behind, a pumpjack nodding in front, sand below.
        box(d, 0, 0, w, h, (135, 206, 235))
        box(d, 0, 58, w, h, (214, 196, 150))
        disc(d, w - 28, 16, 10, (255, 220, 100))
        poly(d, [(28, 58), (36, 20), (44, 58)], (90, 80, 60))
        seg(d, [(32, 48), (40, 48)], (90, 80, 60), 2)
        seg(d, [(30, 36), (42, 36)], (90, 80, 60), 2)
        box(d, 96, 52, 168, 58, (40, 40, 50))
        seg(d, [(118, 52), (118, 26)], (40, 40, 50), 3)
        seg(d, [(118, 26), (150, 18)], (40, 40, 50), 3)
        disc(d, 152, 20, 5, (40, 40, 50))
        seg(d, [(118, 26), (96, 34)], (40, 40, 50), 3)
        disc(d, 96, 36, 4, (40, 40, 50))
        seg(d, [(118, 30), (118, 52)], (40, 40, 50), 2)
    elif key == "apology":
        # Canberra apologises to LGBTQ veterans: deep blue field,
        # the Southern Cross, and a rainbow band of reconciliation.
        box(d, 0, 0, w, h, (0, 47, 108))
        box(d, 0, 0, 60, 34, (0, 36, 125))
        d.line([(0, 0), (60, 34)], fill="white", width=2)
        d.line([(60, 0), (0, 34)], fill="white", width=2)
        d.rectangle((28, 0, 32, 34), fill=(200, 16, 46))
        d.rectangle((0, 15, 60, 19), fill=(200, 16, 46))
        for sx, sy in ((90, 20), (120, 12), (150, 24), (110, 40),
                       (140, 44)):
            disc(d, sx, sy, 2, "white")
        for i, col in enumerate(((220, 40, 50), (240, 140, 30),
                                 (240, 210, 40), (60, 180, 80),
                                 (40, 100, 200))):
            box(d, 0, 62 + i * 3, w, 62 + i * 3 + 3, col)
    elif key == "football":
        # Real Madrid rout PSV 5-1: green pitch, white markings,
        # a ball, and the score.
        box(d, 0, 0, w, h, (20, 140, 60))
        seg(d, [(0, 6), (w, 6)], "white", 2)
        seg(d, [(0, h - 6), (w, h - 6)], "white", 2)
        seg(d, [(w // 2, 6), (w // 2, h - 6)], "white", 2)
        ring(d, w // 2 - 14, h // 2 - 14, w // 2 + 14, h // 2 + 14,
             "white", 2)
        disc(d, 52, 58, 12, "white", outline=(20, 20, 20), width=2)
        disc(d, 52, 58, 4, (20, 20, 20))
        txt(d, (w - 60, 40), "5-1", TY.bignum, "white", anchor="mm")
    elif key == "chart":
        # Consumer confidence jumps to 103.3: rising bars and an
        # upward arrow on a paper background.
        box(d, 0, 0, w, h, (240, 235, 220))
        seg(d, [(16, h - 14), (w - 16, h - 14)], (60, 60, 60), 2)
        seg(d, [(16, h - 14), (16, 14)], (60, 60, 60), 2)
        for bx, frac in ((36, 0.28), (76, 0.42), (116, 0.56),
                         (156, 0.70)):
            bh = int((h - 14) * frac)
            box(d, bx, h - 14 - bh, bx + 28, h - 14, (40, 140, 90))
        seg(d, [(28, h - 24), (w - 28, 22)], SCARLET, 3)
        poly(d, [(w - 28, 22), (w - 42, 20), (w - 34, 32)], SCARLET)
        txt(d, (20, 16), "103.3", TY.amid, BLACK)
    elif key == "hostage":
        # Gunmen hold 25 hostage in a Cartagena supermarket: a
        # shopfront with a striped awning and police tape.
        box(d, 0, 0, w, h, (200, 190, 170))
        box(d, 0, 58, w, h, (120, 115, 105))
        sw = w // 8
        for i in range(8):
            box(d, i * sw, 22, (i + 1) * sw, 34,
                (200, 40, 50) if i % 2 == 0 else "white")
        box(d, 24, 38, 88, 58, (60, 90, 140))
        d.rectangle((24, 38, 88, 58), outline=(20, 20, 20), width=2)
        box(d, 112, 38, 176, 58, (60, 90, 140))
        d.rectangle((112, 38, 176, 58), outline=(20, 20, 20), width=2)
        box(d, 0, 66, w, 76, (255, 210, 40))
        for tx in range(0, w, 16):
            d.line([(tx, 76), (tx + 10, 66)], fill=(20, 20, 20),
                   width=3)
    elif key == "gaza":
        # Top Hamas security figure killed in Gaza drone strikes:
        # a dusk skyline, smoke, and a drone overhead.
        box(d, 0, 0, w, h, (70, 50, 80))
        disc(d, w - 40, 18, 12, (255, 180, 90))
        for bx, bw, bh in ((8, 30, 34), (44, 24, 48), (74, 36, 30),
                           (116, 28, 44), (150, 34, 36),
                           (190, 26, 40)):
            box(d, bx, h - bh, bx + bw, h, (30, 25, 35))
        for sx, sy, sr in ((58, 30, 8), (66, 22, 10), (76, 16, 7),
                           (130, 34, 7), (138, 26, 9)):
            disc(d, sx, sy, sr, (120, 115, 120))
        dx, dy = w - 70, 26
        d.ellipse((dx - 8, dy - 3, dx + 8, dy + 3), fill=(20, 20, 25))
        seg(d, [(dx - 14, dy - 5), (dx + 14, dy - 5)],
            (200, 200, 210), 2)
        seg(d, [(dx, dy + 3), (dx, dy + 9)], (200, 200, 210))
    else:
        raise ValueError("unknown art: %s" % key)
    return img.resize((w, h), Image.LANCZOS)

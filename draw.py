#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261121 (v2, tiered).

An original editorial front page, drawn entirely with Pillow:
no photographs, no copied artwork, no network. Every shape and
every word is produced by this script, so the PNG is deterministic.

Tiered like a real front page: the three biggest stories get
pictures, the next six get cards, and sixteen more run as a
text-only list -- 25 stories in all, every one dated Saturday
21 November 2026:

  HEROES  Iran strikes US bases in Bahrain; drones set the
          Russian cargo ship Sparta II ablaze off Finland;
          COP31 deadlocked over fossil fuels in overtime
  CARDS   FBI probes a suspected NCIC hack; AI sell-off erases
          the Nasdaq's 2026 gains; Mexico captures Chapo Isidro;
          UK & EU sign their biggest post-Brexit deal; a strong
          quake shakes Peru's Andes; an Anthropic mathematician
          claims an AI proof of the Riemann hypothesis
  ALSO    Kryvyi Rih missile; Geneva killer-robot talks; Houthi
          missiles at Riyadh intercepted; EU-Indonesia trade
          pact; BepiColombo enters Mercury orbit; M6.8 quake in
          Timor-Leste; Nigeria funeral boat toll 24; tainted
          alcohol kills 11 in Manipur; England 37-12 All Blacks;
          BTS take five MAMA awards; France cost-of-living
          marches; Basra power-station fire; ICJ ruling fallout;
          Trump defends Putin ties; Gaza food-vehicle strike;
          M5.5 quake in Qinghai

Layout (1024 x 1024): navy masthead with the date, a ticker of
the three top stories, three illustrated hero panels, six cards,
a world map with numbered pins, and a two-column list of sixteen
more stories, each in its own outlined box with a number on a
coloured background.
Run:  python3 draw.py   ->  writes entry.png beside this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (16, 22, 36)
NAVY = (24, 48, 88)
NAVY2 = (18, 38, 70)
RED = (178, 24, 24)
DARKRED = (140, 18, 18)
TEAL = (12, 110, 118)
GOLD = (212, 160, 32)
GREY = (88, 94, 106)
WHITE = (255, 255, 255)
CREAM = (255, 248, 220)
SKY = (178, 214, 235)
SEA = (168, 205, 225)
SAND = (226, 208, 170)

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def shrink(draw, text, size, width, bold=True):
    s = size
    while s > 9 and draw.textlength(text, font=load(s, bold)) > width:
        s -= 1
    return load(s, bold)


def wrap_lines(draw, text, fnt, width):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(draw, x, y, text, fnt, fill, width, gap=None):
    gap = gap if gap is not None else int(fnt.size * 1.3)
    for line in wrap_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += gap
    return y


def box(draw, xy, fill, edge=INK, w=3):
    draw.rectangle(xy, fill=fill, outline=edge, width=w)


def tag(draw, x, y, text, color=RED, size=15):
    draw.text((x, y), text, font=load(size, True), fill=color)


def headline2(draw, x, y, lines, size, width, fill=INK):
    for line in lines:
        fnt = shrink(draw, line, size, width)
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + 4
    return y


# ---------------------------------------------------------- pictures
def gulf_map(d, x, y, w, h):
    """The Gulf: Iran above, Bahrain pinned, arcs of attack."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    d.polygon([(x + 8, y + 8), (x + w - 8, y + 8), (x + w - 8, y + 26),
               (x + 150, y + 26), (x + 120, y + 52), (x + 8, y + 52)],
              fill=SAND, outline=INK)
    d.text((x + w - 66, y + 10), "IRAN", font=load(13, True), fill=INK)
    d.polygon([(x + 8, y + h - 8), (x + 120, y + h - 8),
               (x + 150, y + h - 34), (x + 8, y + h - 34)],
              fill=SAND, outline=INK)
    d.text((x + 16, y + h - 28), "SAUDI ARABIA", font=load(11, True),
           fill=INK)
    # Bahrain: red ring and dot on the Gulf coast
    bx, by = x + 118, y + 58
    d.ellipse([bx - 16, by - 16, bx + 16, by + 16], outline=RED, width=3)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=RED)
    d.text((bx + 20, by - 8), "BAHRAIN", font=load(13, True), fill=DARKRED)
    # missile arcs from the north
    d.arc([x + 60, y + 30, x + 190, y + 96], 200, 340, fill=RED, width=3)
    d.text((x + 168, y + h - 16), "HORMUZ", font=load(11, True),
           fill=GREY)


def burning_ship(d, x, y, w, h):
    """Sparta II ablaze in the Baltic: hull, smoke, flames."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    d.ellipse([x + w - 56, y + 8, x + w - 16, y + 48], fill=(255, 236, 160),
              outline=INK, width=2)
    # smoke
    for cx, cy, r in ((x + 70, y + 22, 13), (x + 92, y + 12, 16),
                      (x + 116, y + 24, 12)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=(120, 120, 120), outline=GREY)
    # hull
    d.polygon([(x + 14, y + 62), (x + w - 14, y + 62),
               (x + w - 34, y + h - 12), (x + 34, y + h - 12)],
              fill=(40, 40, 48), outline=INK)
    d.rectangle([x + 44, y + 40, x + 120, y + 62], fill=(150, 60, 40),
                outline=INK, width=2)
    # flames
    for fx, fw, fh in ((x + 56, 22, 26), (x + 84, 26, 32), (x + 112, 20, 24)):
        d.polygon([(fx, y + 44), (fx + fw // 2, y + 44 - fh),
                   (fx + fw, y + 44)], fill=(255, 140, 0), outline=RED)
    d.text((x + 130, y + 68), "SPARTA II", font=load(13, True), fill=WHITE)


def cop31_clock(d, x, y, w, h):
    """A globe beside a clock running past its deadline."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 232, 180),
                outline=INK, width=2)
    cx, cy = x + 62, y + h // 2
    d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], fill=TEAL,
              outline=INK, width=2)
    d.arc([cx - 44, cy - 44, cx + 44, cy + 44], 200, 340, fill=WHITE,
          width=4)
    d.arc([cx - 44, cy - 44, cx + 44, cy + 44], 20, 160, fill=WHITE,
          width=4)
    d.line([(cx - 44, cy), (cx + 44, cy)], fill=WHITE, width=3)
    # clock
    kx, ky = x + w - 62, y + h // 2 - 6
    d.ellipse([kx - 38, ky - 38, kx + 38, ky + 38], fill=WHITE,
              outline=INK, width=2)
    d.line([(kx, ky), (kx, ky - 26)], fill=INK, width=3)
    d.line([(kx, ky), (kx + 20, ky + 8)], fill=RED, width=3)
    d.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=INK)
    d.text((kx - 26, ky + 40), "OVERTIME", font=load(11, True), fill=RED)


# ---------------------------------------------------------- card icons
def icon_shield(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=NAVY2, outline=INK, width=2)
    d.polygon([(x + s // 2, y + 8), (x + s - 10, y + 16),
               (x + s - 12, y + s - 14), (x + s // 2, y + s - 8),
               (x + 12, y + s - 14), (x + 10, y + 16)],
              fill=(70, 110, 180), outline=WHITE, width=2)
    d.text((x + s // 2 - 11, y + s // 2 - 6), "FBI",
           font=load(12, True), fill=WHITE)


def icon_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=WHITE, outline=INK, width=2)
    pts = [(x + 8, y + 14), (x + 20, y + 20), (x + 32, y + 18),
           (x + 44, y + 32), (x + s - 8, y + 42)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=RED, width=3)
    d.text((x + 8, y + s - 16), "-3.7%", font=load(12, True), fill=RED)


def icon_star(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=CREAM, outline=INK, width=2)
    d.text((x + s // 2 - 10, y + 6), "*", font=load(30, True), fill=GOLD)


def icon_flags(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=WHITE, outline=INK, width=2)
    d.rectangle([x + 6, y + 8, x + s // 2, y + s - 20], fill=NAVY,
                outline=INK, width=1)
    d.line([(x + 6, y + 8), (x + s // 2, y + s - 20)], fill=WHITE, width=3)
    d.line([(x + s // 2, y + 8), (x + 6, y + s - 20)], fill=WHITE, width=3)
    d.rectangle([x + s // 2 + 2, y + 8, x + s - 6, y + s - 20],
                fill=(0, 51, 153), outline=INK, width=1)
    for k in range(6):
        a = math.radians(k * 60 - 90)
        sx = x + s // 2 + 2 + (s // 2 - 8) // 2 + 9 * math.cos(a)
        sy = y + 8 + (s - 28) // 2 + 9 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def icon_peaks(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=SKY, outline=INK, width=2)
    d.polygon([(x + 4, y + s - 6), (x + s // 3, y + 12),
               (x + 2 * s // 3, y + s - 6)], fill=(110, 90, 70),
              outline=INK)
    d.polygon([(x + s // 3, y + s - 6), (x + 2 * s // 3, y + 10),
               (x + s - 4, y + s - 6)], fill=(84, 66, 52), outline=INK)
    d.line([(x + s // 2 - 4, y + 22), (x + s // 2 + 4, y + 32),
            (x + s // 2 - 2, y + 42)], fill=INK, width=2)


def icon_pi(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=NAVY2, outline=INK, width=2)
    d.text((x + s // 2 - 12, y + 8), "π", font=load(30, True), fill=GOLD)
    d.text((x + 6, y + s - 16), "CLAUDE", font=load(10, True), fill=WHITE)


# ---------------------------------------------------------- world map
MAP_X, MAP_Y, MAP_W, MAP_H = 24, 658, 976, 130


def lonlat(lon, lat):
    """Map lon/lat onto the map panel (lon -170..190, lat 80..-60)."""
    x = MAP_X + (lon + 170) / 360 * MAP_W
    y = MAP_Y + (80 - lat) / 140 * MAP_H
    return x, y


CONTINENTS = [
    # North America (wavy Arctic coast, Hudson Bay dip)
    [(-168, 66), (-155, 70), (-140, 68), (-125, 70), (-115, 68),
     (-105, 68), (-95, 72), (-88, 66), (-82, 62), (-78, 66),
     (-75, 70), (-68, 64), (-60, 58), (-55, 52), (-60, 46),
     (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-95, 16),
     (-100, 15), (-105, 20), (-110, 24), (-115, 30), (-120, 35),
     (-125, 40), (-125, 49), (-135, 58), (-150, 60), (-165, 60)],
    # South America
    [(-80, 10), (-75, 7), (-65, 5), (-55, 5), (-50, 0), (-45, -5),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -35),
     (-62, -40), (-68, -50), (-70, -55), (-73, -45), (-73, -35),
     (-72, -20), (-75, -15), (-80, -5), (-82, 0)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
     (10, 59), (5, 60), (12, 56), (18, 56), (20, 54), (24, 58),
     (28, 60), (30, 62), (25, 65), (20, 68), (15, 70), (10, 68),
     (5, 60), (-5, 58), (-10, 54), (-10, 48), (-10, 40)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (15, 32), (20, 32), (25, 32), (30, 31), (32, 28), (35, 28),
     (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (50, 5),
     (48, 0), (42, -5), (40, -12), (36, -18), (33, -25), (30, -30),
     (25, -34), (20, -35), (17, -32), (15, -27), (12, -18), (12, -8),
     (9, -2), (9, 4), (0, 6), (-8, 5), (-13, 8), (-17, 12)],
    # Asia
    [(30, 36), (35, 36), (40, 40), (45, 42), (50, 45), (55, 50),
     (60, 55), (65, 60), (70, 65), (75, 70), (80, 72), (90, 75),
     (100, 76), (110, 74), (120, 72), (130, 72), (140, 72), (150, 70),
     (160, 68), (170, 66), (178, 65), (170, 60), (162, 58), (158, 52),
     (150, 48), (142, 45), (135, 43), (130, 40), (127, 35), (122, 32),
     (120, 28), (115, 22), (110, 20), (108, 15), (105, 10), (103, 5),
     (100, 8), (98, 12), (95, 16), (92, 20), (90, 22), (86, 20),
     (82, 16), (80, 12), (77, 8), (75, 12), (72, 20), (68, 23),
     (65, 25), (60, 25), (57, 28), (55, 30), (52, 32), (50, 35),
     (48, 38), (45, 40), (42, 42), (38, 40), (35, 38), (32, 36)],
    # Australia
    [(113, -22), (115, -20), (118, -16), (122, -14), (126, -12),
     (130, -12), (135, -12), (140, -10), (142, -11), (145, -14),
     (148, -18), (150, -22), (153, -26), (153, -30), (150, -35),
     (147, -38), (142, -38), (138, -35), (135, -32), (132, -32),
     (129, -32), (126, -32), (122, -34), (118, -35), (115, -32),
     (113, -26)],
]

# Numbered pins for the ALSO list (number, lon, lat), nudged by hand
# so neighbours in crowded Europe and the Gulf stay readable.
# 5 (Mercury) has no place on Earth, so it gets no pin.
PINS = [
    (1, 33.4, 47.9), (2, 6.1, 46.2), (3, 46.7, 24.6), (4, 106.8, -6.2),
    (6, 125.6, -8.6), (7, 7.5, 9.1), (8, 94.0, 24.5), (9, -0.3, 51.5),
    (10, 127.0, 37.5), (11, 2.35, 48.85), (12, 47.8, 30.5),
    (13, 4.3, 52.1), (14, 114.1, 22.5), (15, 34.5, 31.5), (16, 96.0, 36.0),
]
PIN_XY = {
    1: (575, 688), 2: (514, 692), 3: (604, 718), 4: (774, 738),
    6: (826, 740), 7: (505, 724), 8: (734, 710), 9: (476, 690),
    10: (829, 698), 11: (498, 700), 12: (620, 698), 13: (486, 680),
    14: (794, 711), 15: (582, 703), 16: (750, 699),
}
# Red dots for the three hero stories: Bahrain, Finland, Antalya.
HERO_DOTS = [(634, 714), (552, 677), (566, 698)]


def world_map(d, x, y, w, h):
    """A simplified world map: ocean, continents, pins."""
    d.rectangle([x, y, x + w, y + h], fill=(190, 215, 230),
                outline=INK, width=2)
    for lat in (60, 30, 0, -30):
        _, gy = lonlat(0, lat)
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=(220, 232, 240),
               width=1)
    for poly in CONTINENTS:
        pts = [lonlat(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=SAND, outline=INK)
    for name, lx, ly in (("ATLANTIC", 430, 752),
                         ("INDIAN OCEAN", 640, 752)):
        d.text((lx, ly), name, font=load(11, True), fill=(110, 130, 150))
    for num, lon, lat in PINS:
        px, py = PIN_XY[num]
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=GOLD,
                  outline=INK, width=1)
        d.text((px, py - 7), str(num), font=load(10, True), fill=INK,
               anchor="ma")
    for px, py in HERO_DOTS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=WHITE, width=2)
    d.text((x + 10, y + h - 18),
           "Red dots = top stories  ·  numbers = list below",
           font=load(12, True), fill=GREY)


# ---------------------------------------------------------- page
def hero(d, x, y, w, h, draw_fn, place, lines, sub):
    box(d, (x, y, x + w, y + h), WHITE)
    draw_fn(d, x + 10, y + 8, w - 20, 104)
    tag(d, x + 12, y + 120, place)
    headline2(d, x + 12, y + 140, lines, 23, w - 24)
    para(d, x + 12, y + 196, sub, load(15), INK, w - 24, gap=19)


def card(d, x, y, w, h, icon_fn, place, lines, sub):
    box(d, (x, y, x + w, y + h), WHITE)
    icon_fn(d, x + 10, y + 10, 56)
    tag(d, x + 76, y + 10, place, size=13)
    headline2(d, x + 76, y + 28, lines, 17, w - 86)
    para(d, x + 10, y + h - 34, sub, load(13), GREY, w - 20, gap=16)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # masthead
    d.rectangle([4, 4, W - 5, 96], fill=NAVY)
    d.text((W // 2, 12), "SATURDAY 21 NOVEMBER 2026",
           font=load(40, True), fill=WHITE, anchor="ma")
    d.text((W // 2, 62), "THE WORLD IN ONE IMAGE  ·  25 STORIES  ·  9 REGIONS",
           font=load(17, True), fill=(255, 214, 90), anchor="ma")

    # ticker: the three top stories
    d.rectangle([4, 100, W - 5, 128], fill=CREAM, outline=INK, width=2)
    d.text((W // 2, 106),
           "IRAN STRIKES BAHRAIN  ◆  RUSSIAN SHIP ABLAZE OFF FINLAND  ◆  COP31 DEADLOCKED",
           font=load(16, True), fill=DARKRED, anchor="ma")

    # heroes
    hero(d, 24, 136, 312, 236, gulf_map, "MIDDLE EAST · CONFLICT",
         ["IRAN STRIKES US BASES", "IN BAHRAIN"],
         "Iran says it hit two US bases; Bahrain reports "
         "a fire, no injuries.")
    hero(d, 356, 136, 312, 236, burning_ship, "EUROPE · GULF OF FINLAND",
         ["DRONES SET RUSSIAN", "CARGO SHIP ABLAZE"],
         "Sparta II catches fire off Finland and drifts "
         "into Finnish waters.")
    hero(d, 688, 136, 312, 236, cop31_clock, "GLOBAL · COP31, ANTALYA",
         ["COP31 DEADLOCKED", "OVER FOSSIL FUELS"],
         "A day past deadline, talks pause overnight; "
         "the draft is rejected.")

    # cards, two rows of three
    card(d, 24, 384, 312, 112, icon_shield, "USA · CYBERATTACK",
         ["FBI PROBES SUSPECTED", "HACK OF CRIME DATABASE"],
         "NCIC, the national police database, under investigation.")
    card(d, 356, 384, 312, 112, icon_chart, "MARKETS",
         ["AI SELL-OFF ERASES", "NASDAQ'S 2026 GAINS"],
         "S&P 500 -3.7%, in correction; Anthropic slides day two.")
    card(d, 688, 384, 312, 112, icon_star, "MEXICO · JUSTICE",
         ["MEXICO CAPTURES", "CARTEL BOSS CHAPO ISIDRO"],
         "FBI most-wanted boss seized; 11 dead in the backlash.")
    card(d, 24, 504, 312, 112, icon_flags, "EUROPE",
         ["UK & EU SIGN BIGGEST", "POST-BREXIT DEAL"],
         "Food trade, carbon markets and youth mobility.")
    card(d, 356, 504, 312, 112, icon_peaks, "PERU · DISASTER",
         ["STRONG QUAKE SHAKES", "PERU'S ANDES"],
         "Tremor felt in Lima; no major damage reported at first.")
    card(d, 688, 504, 312, 112, icon_pi, "SCIENCE",
         ["AI-ASSISTED PROOF OF", "RIEMANN HYPOTHESIS?"],
         "Anthropic mathematician claims a proof with Claude.")

    # also list: header, world map, then boxed numbered items
    d.rectangle([4, 628, W - 5, 654], fill=NAVY2)
    d.text((24, 634), "ALSO ON SATURDAY 21 NOVEMBER 2026 — WHERE IT HAPPENED",
           font=load(17, True), fill=(255, 214, 90))
    world_map(d, 24, 658, 976, 130)
    also_left = [
        ("Kryvyi Rih:", "Russian missile kills 2, wounds dozens"),
        ("Geneva:", "128 nations agree killer-robot talks to 2028"),
        ("Riyadh:", "3 Houthi missiles intercepted"),
        ("EU–Indonesia:", "trade pact cuts 98.5% of tariffs"),
        ("Mercury:", "BepiColombo enters orbit, 18:24 UTC"),
        ("Timor-Leste:", "M6.8 quake felt in Darwin"),
        ("Nigeria:", "funeral boat toll reaches 24"),
        ("Manipur:", "tainted alcohol kills 11"),
    ]
    also_right = [
        ("Twickenham:", "England beat All Blacks 37–12"),
        ("Seoul:", "BTS take five MAMA awards"),
        ("France:", "6th Saturday of cost-of-living marches"),
        ("Basra:", "power-station fire kills 4, injures 35"),
        ("The Hague:", "Myanmar, Beijing oppose ICJ ruling"),
        ("Shenzhen:", "Trump defends his Putin ties"),
        ("Gaza City:", "strike kills 3 in a food vehicle"),
        ("Qinghai:", "M5.5 quake in remote west China"),
    ]
    badge_cols = [RED, NAVY, TEAL, (176, 118, 0), (28, 110, 62),
                  (120, 60, 140), (200, 80, 0), (0, 120, 180)]
    num = 0
    for col, items in ((24, also_left), (524, also_right)):
        yy = 796
        for lead, rest in items:
            num += 1
            box(d, (col, yy, col + 476, yy + 23), WHITE, edge=INK, w=2)
            bc = badge_cols[(num - 1) % len(badge_cols)]
            d.rectangle([col + 2, yy + 2, col + 22, yy + 21], fill=bc)
            d.text((col + 12, yy + 4), str(num), font=load(13, True),
                   fill=WHITE, anchor="ma")
            d.text((col + 28, yy + 4), lead, font=load(13, True),
                   fill=INK)
            lw = d.textlength(lead, font=load(13, True))
            d.text((col + 28 + lw + 4, yy + 4), rest, font=load(13),
                   fill=INK)
            yy += 25

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()

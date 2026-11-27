#!/usr/bin/env python3
"""Render the news-image 20261126 v2 broadsheet (1024x1024, flat vector).

Local-only build helper: draws the whole front page with PIL primitives
and writes entry.png next to this file. The shipped entrypoint (main.py)
only copies that PNG; it does not use PIL and needs no network.
Deterministic: no randomness, no clock, fixed fonts.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 22                      # outer margin
CW = W - 2 * M              # content width = 980

PAPER = (247, 242, 231)
INK = (26, 42, 74)
INK_SOFT = (58, 66, 88)
RED = (178, 35, 42)
RED_DK = (140, 24, 30)
GOLD = (201, 148, 42)
SKY = (178, 205, 224)
SKY_DK = (120, 158, 190)
GREEN = (46, 110, 70)
GREY = (120, 116, 108)
LINE = (26, 42, 74)
BAND = (233, 226, 208)
CARD_BG = (255, 253, 247)
MAP_BG = (232, 236, 228)
DOT = (150, 158, 140)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines top-left anchored; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(draw, x, y, label, fill):
    """Small filled certainty tag; returns its right edge."""
    f = font(SANS_B, 9)
    w = int(draw.textlength(label, font=f) + 10)
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return x + w


TAG_FILL = {
    "CONFIRMED": (46, 110, 70),
    "OFFICIAL": (26, 42, 74),
    "REPORTED": (90, 110, 150),
    "CLAIM": (178, 35, 42),
    "ONGOING": (120, 90, 20),
}

STATS = [
    ("60 MPH", "nor'easter gusts\nover New York"),
    ("€45BN", "EU loan for Kyiv\nin 2027"),
    ("3.25%", "Bank of Korea\nkey rate"),
    ("18 YRS", "since the 26/11\nMumbai attacks"),
    ("+36%", "Bangladesh garment\nminimum wage"),
    ("166", "lives lost in the\n26/11 attacks"),
]

REGIONS = ("North America 6", "South Asia 6", "Europe 6", "Middle East 4",
           "Africa 4", "World 3", "East Asia 3", "Oceania 2",
           "South America 2")

UTC_SLOTS = [
    ("00:00", "Thanksgiving Day begins in US"),
    ("06:00", "Delhi wakes to Constitution Day"),
    ("13:30", "Parade was due to step off"),
    ("14:00", "Chess Game 3 begins in Geneva"),
    ("15:00", "High-wind warning in New York"),
    ("23:00", "36 stories filed"),
]

HEROES = [
    dict(num=1, kicker="NEW YORK · THANKSGIVING",
         head="Macy's 100th Thanksgiving parade postponed to Saturday",
         body=("A nor'easter brings 60 mph gusts to New York; the parade "
               "moves to Saturday, a first in 100 years."),
         src="SOURCE: AP", tag="REPORTED", scene="parade"),
    dict(num=2, kicker="INDIA · MUMBAI",
         head="India marks 18 years since the 26/11 Mumbai attacks",
         body=("Tributes for the 166 killed in the 2008 attacks; the nation "
               "also marks 77 years of its Constitution."),
         src="SOURCE: PTI / PIB", tag="CONFIRMED", scene="india"),
    dict(num=3, kicker="EUROPE · BRUSSELS",
         head="EU leaders meet on budget and Ukraine aid",
         body=("Two-day summit opens on the 2028–34 budget (€1.58tn) and "
               "Kyiv's 2027 loan (€45bn)."),
         src="SOURCE: EU COUNCIL", tag="OFFICIAL", scene="eu"),
]

CARDS = [
    dict(num=4, kicker="CHESS · GENEVA",
         head="Gukesh meets Sindarov in Game 3 of the title match",
         body="World title level 1–1.",
         src="FIDE", tag="ONGOING", scene="chess"),
    dict(num=5, kicker="UKRAINE WAR",
         head="Kyiv counts 4 hurt after mall strike",
         body="Overnight missiles; 2 serious.",
         src="KYIV POST", tag="REPORTED", scene="kyiv"),
    dict(num=6, kicker="MARKETS · SEOUL",
         head="Korea lifts key rate to 3.25% as chip stocks rally",
         body="BOK hikes 25 bps; Nikkei +1.4%.",
         src="BOK / YONHAP", tag="CONFIRMED", scene="korea"),
    dict(num=7, kicker="MIDDLE EAST",
         head="Saudi defences down two Houthi missiles over Riyadh",
         body="Interceptions shake the capital.",
         src="SAUDI COALITION", tag="REPORTED", scene="riyadh"),
    dict(num=8, kicker="THE GULF",
         head="Two tankers hit naval mines in the Strait of Hormuz",
         body="Reported in the strait.",
         src="REUTERS", tag="REPORTED", scene="hormuz"),
    dict(num=9, kicker="TRADE · WASHINGTON",
         head="US proposes new tariffs on 14 economies",
         body="Duties hit China, the EU and Japan.",
         src="USTR / REUTERS", tag="CONFIRMED", scene="tariff"),
    dict(num=10, kicker="BANGLADESH",
         head="Bangladesh lifts garment wage 36% to Tk17,000",
         body="Pay floor rises for garment workers.",
         src="AFP", tag="CONFIRMED", scene="wage"),
    dict(num=11, kicker="SPACE · CHINA",
         head="Shenzhou-24 docks; first Pakistani reaches orbit",
         body="First Pakistani aboard Tiangong.",
         src="XINHUA", tag="CONFIRMED", scene="space"),
    dict(num=12, kicker="PACIFIC",
         head="Solomon Islands signs pact with Australia",
         body="Canberra deepens Pacific ties.",
         src="AP", tag="CONFIRMED", scene="solomon"),
    dict(num=13, kicker="UKRAINE WAR",
         head="Russian strikes cut power in five regions",
         body="Grid attacks leave regions dark.",
         src="REUTERS", tag="REPORTED", scene="power"),
]

ALSO = [
    (14, "New Delhi", "India and Nepal sign Rs 15,000 crore package", "PTI"),
    (15, "Washington", "US jobless claims fall to 189,000", "Reuters"),
    (16, "New York", "Nvidia sell-off drags S&P and Nasdaq down", "Reuters"),
    (17, "Brussels", "EU imposes visa bans, quotas on Chinese cars", "Reuters"),
    (18, "Bogotá", "Colombia police free 29 supermarket hostages", "AP"),
    (19, "Khartoum", "Sudan drone strikes kill 19 in Blue Nile", "Reuters"),
    (20, "Niamey", "Saudi national kidnapped by IS men in Niger", "Reuters"),
    (21, "Cairo", "Cairo tanker crash fire kills at least 30", "AP"),
    (22, "London", "PLA shifts UK flights to own 777 fleet today", "Reuters"),
    (23, "Madrid", "Bellingham stunner as Real Madrid rout PSV", "UEFA"),
    (24, "Mumbai", "Sooryavanshi, 15, smashes 204 off 53 balls", "Cricinfo"),
    (25, "New York", "US stock and bond markets shut for Thanksgiving", "NYSE"),
    (26, "New Delhi", "IITs add 6,000 seats in robotics, AI, space", "Govt of India"),
    (27, "Chicago", "Tempus buys Personalis in $600m cash deal", "Investing.com"),
    (28, "Shanghai", "Xi probe hits Shanghai chief Chen Jining", "Reuters"),
    (29, "Darmstadt", "Hera reveals DART crater on asteroid Dimorphos", "ESA"),
    (30, "Rio de Janeiro", "Brazil mosquitoes cut viral infections 68%", "Study"),
    (31, "Sydney", "Palm Beach ferries strike shuts services", "NSW Govt"),
    (32, "Kuala Lumpur", "Malaysia sues Google for $146m over YouTube", "Reuters"),
    (33, "Yaoundé", "Swiss tourist killed by elephants in Cameroon", "AP"),
    (34, "Iowa", "Army blows up 5 tonnes of explosives in Iowa", "Al Jazeera"),
    (35, "Hodeidah", "Coalition hits Hodeidah after Houthi attacks", "Reuters"),
    (36, "Geneva", "UN: Gaza staff sacked on unproven claims", "The Guardian"),
]

DATE_CHECK = [
    ("Nvidia reinstates Jensen Huang", "24 Nov"),
    ("COP31 ends without a pact", "22 Nov"),
    ("Ukraine drones hit Russian ships off Libya", "22 Nov"),
    ("Belgium strike grounds flights", "23 Nov"),
    ("Israel kills Hamas chief Naeem Abu Nahal", "24 Nov"),
    ("Trump–Putin–Xi trilateral in Shenzhen", "17 Nov"),
    ("UNRWA worker killed in Gaza strike", "23 Nov"),
    ("US shelves Russia business-deal peace plan", "25 Nov"),
]


# ---------------------------------------------------------------- scenes
# Every scene is drawn from scratch with PIL primitives: flat vector
# shapes, no photographs, no copied pixels.

def _buildings(draw, x, y, w, h, base, lit):
    """Row of dark towers with lit windows, sitting on `base`."""
    n = max(3, w // 26)
    bw = w / n
    for i in range(n):
        bh = h * (0.45 + 0.13 * ((i * 37) % 4))
        bx = x + i * bw + 2
        draw.rectangle([bx, y + h - bh, bx + bw - 4, y + h], fill=base)
        for wy in range(int(y + h - bh + 5), int(y + h - 4), 9):
            for wx in range(int(bx + 3), int(bx + bw - 7), 8):
                if (i * 7 + int(wx) + int(wy)) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=lit)


def _rain(draw, x, y, w, h):
    for i in range(0, w, 16):
        x0 = x + i
        draw.line([x0, y + (i * 13) % 30, x0 - 6, y + 22 + (i * 13) % 30],
                  fill=(200, 215, 230), width=2)


def scene_parade(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 58, 96))
    _buildings(draw, x, y + h * 0.42, w, h * 0.58, (22, 34, 62), (240, 200, 90))
    # big red balloon
    cx, cy, rx, ry = x + w * 0.52, y + h * 0.34, w * 0.17, h * 0.24
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(198, 52, 52))
    draw.ellipse([cx - rx * 0.45, cy - ry * 0.55, cx - rx * 0.1, cy - ry * 0.1],
                 fill=(228, 120, 110))
    draw.line([cx, cy + ry, cx - 8, y + h * 0.72], fill=(220, 220, 220), width=2)
    draw.line([cx, cy + ry, cx + 10, y + h * 0.72], fill=(220, 220, 220), width=2)
    _rain(draw, x, y, w, h)
    # street banner
    draw.rectangle([x, y + h - 20, x + w, y + h], fill=RED)
    draw.text((x + 8, y + h - 17), "POSTPONED TO SATURDAY",
              font=font(SANS_B, 11), fill=(255, 255, 255))
    # 100 badge
    draw.ellipse([x + w - 34, y + 8, x + w - 6, y + 36], fill=GOLD)
    draw.text((x + w - 30, y + 15), "100", font=font(SANS_B, 12), fill=INK)


def scene_india(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 150, 60))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(214, 120, 44))
    # memorial arch
    ax, ay = x + w * 0.16, y + h * 0.14
    draw.rectangle([ax, ay + 26, ax + 14, y + h * 0.62], fill=(250, 235, 200))
    draw.rectangle([ax + w * 0.42, ay + 26, ax + w * 0.42 + 14, y + h * 0.62],
                   fill=(250, 235, 200))
    draw.rectangle([ax, ay, ax + w * 0.42 + 14, ay + 26], fill=(250, 235, 200))
    draw.ellipse([ax + w * 0.21 - 4, ay + 30, ax + w * 0.21 + 22, ay + 56],
                 outline=(250, 235, 200), width=5)
    # tricolour flag
    fx, fy = x + w * 0.66, y + h * 0.18
    draw.rectangle([fx, fy, fx + 62, fy + 12], fill=(255, 153, 51))
    draw.rectangle([fx, fy + 12, fx + 62, fy + 24], fill=(255, 255, 255))
    draw.rectangle([fx, fy + 24, fx + 62, fy + 36], fill=(19, 136, 8))
    draw.ellipse([fx + 25, fy + 13, fx + 37, fy + 25], outline=(0, 0, 128), width=1)
    draw.line([fx, fy, fx, y + h * 0.62], fill=(90, 60, 30), width=3)
    # row of candles
    for i in range(7):
        cx = x + 14 + i * 20
        draw.rectangle([cx, y + h - 22, cx + 6, y + h - 10], fill=(255, 244, 200))
        draw.ellipse([cx + 1, y + h - 28, cx + 5, y + h - 22], fill=GOLD)
    draw.rectangle([x, y + h - 16, x + w, y + h - 12], fill=(120, 60, 20))
    draw.text((x + w - 66, y + 6), "18 YEARS", font=font(SANS_B, 11),
              fill=(255, 255, 255))


def scene_eu(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 58, 110))
    # gold stars ring + blue disc
    cx, cy = x + w * 0.5, y + h * 0.46
    draw.ellipse([cx - 78, cy - 40, cx + 78, cy + 40], fill=(238, 226, 190))
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + 62 * math.cos(a), cy + 30 * math.sin(a)
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD)
    draw.ellipse([cx - 34, cy - 26, cx + 34, cy + 26], fill=(24, 48, 96))
    draw.text((cx - 24, cy - 9), "EU 27", font=font(SANS_B, 15),
              fill=(255, 255, 255))
    # budget bars (headline and body already carry the figures)
    for i, bh in enumerate((14, 22, 30)):
        bx = x + 16 + i * 20
        draw.rectangle([bx, y + h - 8 - bh, bx + 12, y + h - 8], fill=GOLD)


def scene_chess(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(44, 62, 44))
    s = min(w, h) / 4.6
    ox, oy = x + (w - 4 * s) / 2, y + (h - 4 * s) / 2
    for r in range(4):
        for c in range(4):
            fill = (240, 230, 210) if (r + c) % 2 == 0 else (60, 60, 60)
            draw.rectangle([ox + c * s, oy + r * s, ox + (c + 1) * s,
                            oy + (r + 1) * s], fill=fill)
    draw.ellipse([ox + 0.7 * s, oy + 0.5 * s, ox + 1.3 * s, oy + 1.1 * s],
                 fill=(250, 250, 250), outline=INK, width=1)
    draw.ellipse([ox + 2.7 * s, oy + 2.5 * s, ox + 3.3 * s, oy + 3.1 * s],
                 fill=(30, 30, 30), outline=(200, 200, 200), width=1)


def scene_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(120, 130, 145))
    draw.rectangle([x, y + h * 0.55, x + w * 0.7, y + h], fill=(70, 76, 90))
    draw.rectangle([x + w * 0.7, y + h * 0.4, x + w, y + h], fill=(88, 94, 108))
    for i in range(4):
        draw.rectangle([x + 8 + i * 16, y + h * 0.62, x + 18 + i * 16,
                        y + h * 0.72], fill=(240, 200, 90))
    draw.ellipse([x + w * 0.55, y + 6, x + w * 0.8, y + 26], fill=(90, 90, 95))
    draw.ellipse([x + w * 0.68, y + 2, x + w * 0.92, y + 20], fill=(70, 70, 75))
    draw.polygon([(x + w * 0.72, y + h * 0.4), (x + w * 0.86, y + h * 0.62),
                  (x + w * 0.6, y + h * 0.62)], fill=(200, 80, 40))


def scene_korea(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    draw.line([x + 8, y + h - 12, x + w - 8, y + h - 12], fill=GREY, width=1)
    pts = [(x + 10, y + h - 22), (x + w * 0.3, y + h - 30),
           (x + w * 0.5, y + h - 24), (x + w * 0.72, y + h - 38),
           (x + w - 10, y + 12)]
    draw.line(pts, fill=GREEN, width=3)
    draw.polygon([(x + w - 18, y + 10), (x + w - 6, y + 10),
                  (x + w - 10, y + 2)], fill=GREEN)
    draw.rectangle([x + 6, y + 6, x + 62, y + 20], fill=INK)
    draw.text((x + 10, y + 8), "3.25%", font=font(SANS_B, 10),
              fill=(255, 255, 255))


def scene_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(18, 24, 48))
    for i in range(8):
        px = x + 10 + (i * 23) % (w - 16)
        py = y + 6 + (i * 11) % 16
        draw.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
    draw.line([x + 8, y + h * 0.3, x + w * 0.55, y + h * 0.55],
              fill=(255, 220, 120), width=2)
    draw.line([x + w * 0.55, y + h * 0.55, x + w - 12, y + h * 0.35],
              fill=(255, 120, 90), width=2)
    draw.ellipse([x + w * 0.52, y + h * 0.5, x + w * 0.6, y + h * 0.62],
                 fill=(255, 190, 80))
    _buildings(draw, x, y + h * 0.55, w, h * 0.45, (10, 14, 30), (240, 200, 90))


def scene_hormuz(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(150, 190, 210))
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(40, 90, 130))
    for i in range(3):
        wy = y + h * (0.62 + i * 0.12)
        draw.arc([x + 6, wy - 4, x + w - 6, wy + 8], 0, 180, fill=(220, 240, 250),
                 width=2)
    # tanker
    draw.rectangle([x + w * 0.12, y + h * 0.42, x + w * 0.55, y + h * 0.58],
                   fill=(140, 40, 40))
    draw.rectangle([x + w * 0.48, y + h * 0.3, x + w * 0.55, y + h * 0.42],
                   fill=(200, 200, 200))
    # mine
    mx, my = x + w * 0.75, y + h * 0.68
    draw.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(30, 30, 30))
    for dx, dy in ((-9, 0), (9, 0), (0, -9), (0, 9)):
        draw.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=2)


def scene_tariff(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    cols = [(198, 52, 52), (240, 180, 60), (60, 110, 180), (46, 110, 70)]
    for r in range(2):
        for c in range(4):
            bx, by = x + 8 + c * 44, y + 8 + r * 18
            draw.rectangle([bx, by, bx + 40, by + 14], fill=cols[(r * 4 + c) % 4])
    draw.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 4], fill=INK)
    draw.text((x + 12, y + h - 15), "14 PARTNERS", font=font(SANS_B, 9),
              fill=(255, 255, 255))
    pct = "15–35%"
    draw.text((x + w - 12 - draw.textlength(pct, font=font(SANS_B, 9)),
               y + h - 15), pct, font=font(SANS_B, 9), fill=(255, 220, 120))


def scene_wage(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
    draw.rectangle([x + 10, y + h * 0.35, x + w - 10, y + h * 0.8],
                   fill=(150, 90, 50))
    draw.polygon([(x + 6, y + h * 0.35), (x + w * 0.5, y + 8),
                  (x + w - 6, y + h * 0.35)], fill=(120, 70, 40))
    draw.rectangle([x + w * 0.3, y + h * 0.55, x + w * 0.42, y + h * 0.8],
                   fill=(60, 40, 25))
    draw.text((x + 8, y + 6), "Tk 17,000  +36%", font=font(SANS_B, 11), fill=RED)
    draw.line([x + w - 34, y + 16, x + w - 10, y + 4], fill=GREEN, width=3)
    draw.polygon([(x + w - 18, y + 2), (x + w - 6, y + 2), (x + w - 10, y - 4)],
                 fill=GREEN)


def scene_space(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(14, 20, 44))
    for i in range(10):
        px = x + 8 + (i * 19) % (w - 14)
        py = y + 5 + (i * 13) % 20
        draw.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
    # rocket
    rx = x + w * 0.3
    draw.rectangle([rx, y + 10, rx + 12, y + h * 0.55], fill=(240, 240, 240))
    draw.polygon([(rx, y + 10), (rx + 12, y + 10), (rx + 6, y)], fill=RED)
    draw.polygon([(rx + 2, y + h * 0.55), (rx + 10, y + h * 0.55),
                  (rx + 6, y + h * 0.75)], fill=(255, 160, 40))
    # station ring
    sx, sy = x + w * 0.72, y + h * 0.42
    draw.ellipse([sx - 26, sy - 8, sx + 26, sy + 8], outline=(200, 210, 230),
                 width=3)
    draw.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(200, 210, 230))


def scene_solomon(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(140, 190, 220))
    draw.rectangle([x, y + h * 0.6, x + w, y + h], fill=(50, 110, 160))
    draw.ellipse([x + w * 0.18, y + h * 0.48, x + w * 0.82, y + h * 0.78],
                 fill=(90, 160, 90))
    for i in range(3):
        px = x + w * (0.3 + i * 0.2)
        draw.line([px, y + h * 0.5, px, y + h * 0.32], fill=(90, 60, 30), width=2)
        draw.ellipse([px - 9, y + h * 0.44, px + 9, y + h * 0.5], fill=(40, 110, 50))
    draw.rectangle([x + w - 52, y + 6, x + w - 6, y + 20], fill=(255, 255, 255))
    draw.text((x + w - 48, y + 8), "PACT", font=font(SANS_B, 10), fill=INK)


def scene_power(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 32, 44))
    # dark grid blocks, one lit window strip
    for r in range(2):
        for c in range(4):
            bx, by = x + 8 + c * 44, y + 8 + r * 20
            draw.rectangle([bx, by, bx + 38, by + 16], fill=(55, 58, 74))
    draw.rectangle([x + 8, y + 8, x + 46, y + 24], fill=(240, 200, 90))
    draw.polygon([(x + w * 0.7, y + 4), (x + w * 0.58, y + h * 0.5),
                  (x + w * 0.68, y + h * 0.5), (x + w * 0.56, y + h - 6),
                  (x + w * 0.78, y + h * 0.45), (x + w * 0.66, y + h * 0.45)],
                 fill=(255, 220, 80))


SCENES = {
    "parade": scene_parade, "india": scene_india, "eu": scene_eu,
    "chess": scene_chess, "kyiv": scene_kyiv, "korea": scene_korea,
    "riyadh": scene_riyadh, "hormuz": scene_hormuz, "tariff": scene_tariff,
    "wage": scene_wage, "space": scene_space, "solomon": scene_solomon,
    "power": scene_power,
}


# ---------------------------------------------------------------- map
# Rough continent outlines in (lon, lat); dots are plotted on a grid
# wherever the point falls inside one of them.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-80, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (25, 71), (18, 69),
     (12, 66), (5, 60), (-5, 58), (-10, 52)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (25, -34), (18, -35), (15, -27), (12, -18), (9, -1), (9, 4),
     (-8, 4), (-13, 8)],
    # Asia
    [(30, 36), (36, 36), (44, 39), (48, 30), (54, 26), (57, 25), (61, 25),
     (66, 25), (72, 20), (77, 8), (80, 7), (85, 19), (89, 22), (92, 21),
     (95, 16), (100, 8), (103, 1), (104, 9), (108, 11), (109, 15),
     (106, 20), (108, 18), (110, 20), (114, 22), (120, 25), (122, 31),
     (127, 35), (127, 40), (130, 42), (135, 44), (140, 46), (142, 50),
     (140, 53), (137, 55), (135, 59), (130, 59), (128, 62), (135, 65),
     (140, 68), (145, 70), (150, 70), (158, 69), (162, 66), (170, 66),
     (178, 65), (178, 70), (160, 70), (140, 72), (120, 73), (100, 74),
     (80, 73), (60, 69), (50, 68), (40, 67), (32, 70), (30, 66), (28, 62),
     (30, 59), (24, 58), (21, 55), (18, 54), (10, 57), (8, 55), (5, 53),
     (0, 51), (-2, 48), (-5, 43), (-9, 43), (-10, 36), (0, 36), (10, 37),
     (20, 32), (30, 31), (35, 28)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (137, -35), (140, -38), (146, -39), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 38),
     (141, 41), (142, 43), (145, 44), (143, 42), (141, 39), (139, 37),
     (136, 35), (133, 34), (130, 33)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (174, -41), (171, -43), (168, -46)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 57), (1, 52), (-1, 51),
     (-4, 50)],
]

PINS = {
    1: (-74.0, 40.7), 2: (72.8, 19.0), 3: (4.35, 50.85), 4: (6.14, 46.2),
    5: (30.5, 50.45), 6: (127.0, 37.5), 7: (46.7, 24.6), 8: (56.5, 26.5),
    9: (-77.0, 38.9), 10: (90.4, 23.8), 11: (100.3, 40.9), 12: (160.0, -9.4),
    13: (31.0, 49.0),
}


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            xint = (x2 - x1) * (lat - y1) / (y2 - y1) + x1
            if lon < xint:
                inside = not inside
    return inside


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=MAP_BG,
                   outline=INK, width=1)
    step = 6
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 75.0, -58.0
    for gy in range(int(y + 4), int(y + h - 3), step):
        lat = lat0 + (gy - y) / h * (lat1 - lat0)
        for gx in range(int(x + 4), int(x + w - 3), step):
            lon = lon0 + (gx - x) / w * (lon1 - lon0)
            if any(_inside(lon, lat, p) for p in CONTINENTS):
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=DOT)
    fnum = font(SANS_B, 9)
    for num, (lon, lat) in PINS.items():
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat - lat0) / (lat1 - lat0) * h
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(num), font=fnum)
        draw.text((px - tw / 2, py - 6), str(num), font=fnum,
                  fill=(255, 255, 255))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- eyebrow + rules
    d.line([M, 12, W - M, 12], fill=INK, width=2)
    d.text((M, 18), "THE DAY IN WORLD NEWS", font=font(SANS_B, 12), fill=INK)
    right = "36 STORIES  ·  9 REGIONS  ·  ONE DAY"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 12)), 18), right,
           font=font(SANS_B, 12), fill=RED)

    # --- masthead: mixed-case serif, the 26 in red
    f_mast = font(SERIF_B, 56)
    parts = [("Thursday ", INK), ("26", RED), (" November 2026", INK)]
    total = sum(d.textlength(t, font=f_mast) for t, _ in parts)
    cx = M + (CW - total) / 2
    for t, col in parts:
        d.text((cx, 38), t, font=f_mast, fill=col)
        cx += d.textlength(t, font=f_mast)
    d.line([M, 100, W - M, 100], fill=INK, width=1)

    # --- tagline (italic serif, 2 lines, centred)
    f_tag = font(SERIF_I, 15)
    tag = ("A nor'easter grounds New York's 100th Thanksgiving parade, "
           "India marks 18 years since the 26/11 Mumbai attacks, and EU "
           "leaders meet on budget and Ukraine aid.")
    lines = wrap(d, tag, f_tag, 900)
    ty = 106
    for line in lines:
        tw = d.textlength(line, font=f_tag)
        d.text((M + (CW - tw) / 2, ty), line, font=f_tag, fill=INK_SOFT)
        ty += 19

    # --- stats row: 6 big red numbers
    y_stats = 146
    d.line([M, y_stats - 6, W - M, y_stats - 6], fill=INK, width=1)
    d.line([M, y_stats + 40, W - M, y_stats + 40], fill=INK, width=1)
    cell = CW / 6
    for i, (num, lab) in enumerate(STATS):
        x0 = M + i * cell
        if i:
            d.line([x0, y_stats - 4, x0, y_stats + 38], fill=GREY, width=1)
        f_num = font(SANS_B, 21)
        tw = d.textlength(num, font=f_num)
        d.text((x0 + (cell - tw) / 2, y_stats), num, font=f_num, fill=RED)
        f_lab = font(SANS, 9)
        lab_lines = lab.split("\n")
        for j, lline in enumerate(lab_lines):
            lw = d.textlength(lline, font=f_lab)
            d.text((x0 + (cell - lw) / 2, y_stats + 20 + j * 9), lline,
                   font=f_lab, fill=INK_SOFT)

    # --- region bar
    region_txt = "  ·  ".join(REGIONS) + "   =   36 stories"
    f_reg = font(SANS, 11)
    tw = d.textlength(region_txt, font=f_reg)
    d.text((M + (CW - tw) / 2, 192), region_txt, font=f_reg, fill=INK)

    # --- UTC strip (full width, 6 slots)
    y_utc = 210
    d.rectangle([M, y_utc, W - M, y_utc + 26], fill=BAND)
    slot = CW / 6
    f_t = font(SANS_B, 10)
    f_u = font(SANS, 9)
    for i, (t, txt) in enumerate(UTC_SLOTS):
        x0 = M + i * slot
        if i:
            d.line([x0, y_utc + 3, x0, y_utc + 23], fill=GREY, width=1)
        d.text((x0 + 6, y_utc + 2), t, font=f_t, fill=RED)
        lines = wrap(d, txt, f_u, slot - 12)
        text_block(d, x0 + 6, y_utc + 13, lines[:1], f_u, INK, leading=10)

    # --- heroes (3 columns)
    y_hero = 242
    h_w = (CW - 2 * 12) // 3
    f_kick = font(SANS_B, 10)
    f_head = font(SERIF_B, 18)
    f_body = font(SANS, 11)
    f_src = font(SANS, 9)
    for i, hero in enumerate(HEROES):
        x0 = M + i * (h_w + 12)
        SCENES[hero["scene"]](d, x0, y_hero, h_w, 84)
        # number badge on the scene
        d.ellipse([x0 + 6, y_hero + 6, x0 + 26, y_hero + 26], fill=RED)
        f_nb = font(SANS_B, 12)
        d.text((x0 + 11, y_hero + 9), str(hero["num"]), font=f_nb,
               fill=(255, 255, 255))
        d.text((x0, y_hero + 88), hero["kicker"], font=f_kick, fill=RED)
        hy = text_block(d, x0, y_hero + 100,
                        wrap(d, hero["head"], f_head, h_w)[:3],
                        f_head, INK, leading=19)
        by = text_block(d, x0, hy + 3,
                        wrap(d, hero["body"], f_body, h_w)[:2],
                        f_body, INK_SOFT, leading=12)
        d.text((x0, by + 4), hero["src"], font=f_src, fill=GREY)
        tag_chip(d, x0 + h_w - 74, by + 3, hero["tag"],
                 TAG_FILL[hero["tag"]])

    # --- cards 4-13 (grid 5 x 2)
    y_cards = 442
    c_w = (CW - 4 * 10) // 5
    c_h = 100
    f_ch = font(SERIF_B, 12)
    f_cb = font(SANS, 9)
    for idx, card in enumerate(CARDS):
        row, col = divmod(idx, 5)
        x0 = M + col * (c_w + 10)
        y0 = y_cards + row * (c_h + 8)
        d.rectangle([x0, y0, x0 + c_w, y0 + c_h], fill=CARD_BG,
                    outline=(200, 192, 172), width=1)
        SCENES[card["scene"]](d, x0 + 1, y0 + 1, c_w - 2, 38)
        d.ellipse([x0 + 5, y0 + 5, x0 + 21, y0 + 21], fill=RED)
        f_nb = font(SANS_B, 10)
        d.text((x0 + 9, y0 + 7), str(card["num"]), font=f_nb,
               fill=(255, 255, 255))
        d.text((x0 + 4, y0 + 42), card["kicker"], font=font(SANS_B, 8),
               fill=RED)
        hy = text_block(d, x0 + 4, y0 + 52,
                        wrap(d, card["head"], f_ch, c_w - 8)[:2],
                        f_ch, INK, leading=12)
        text_block(d, x0 + 4, hy + 1,
                   wrap(d, card["body"], f_cb, c_w - 8)[:1],
                   f_cb, INK_SOFT, leading=10)
        d.text((x0 + 4, y0 + c_h - 12), card["src"], font=f_src, fill=GREY)
        tag_chip(d, x0 + c_w - 62, y0 + c_h - 13, card["tag"],
                 TAG_FILL[card["tag"]])

    # --- world map
    y_map = 654
    d.text((M, y_map), "WHERE IT HAPPENED — PINS 1–13",
           font=font(SANS_B, 11), fill=INK)
    draw_map(d, M, y_map + 16, CW, 84)

    # --- ALSO list 14-36, two columns
    y_also = 760
    d.text((M, y_also), "AND ALSO — STORIES 14–36",
           font=font(SANS_B, 11), fill=INK)
    f_a = font(SANS, 10)
    f_ab = font(SANS_B, 10)
    col_w = CW / 2
    for i, (num, city, story, src) in enumerate(ALSO):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x0 = M + col * col_w
        yy = y_also + 16 + row * 10
        num_s = "%d." % num
        d.text((x0, yy), num_s, font=f_ab, fill=RED)
        nx = x0 + d.textlength(num_s + " ", font=f_ab)
        d.text((nx, yy), city + " — ", font=f_ab, fill=INK)
        cx2 = nx + d.textlength(city + " — ", font=f_ab)
        rest = story + " — " + src
        d.text((cx2, yy), rest, font=f_a, fill=INK_SOFT)

    # --- DATE CHECK box
    y_dc = 902
    d.rectangle([M, y_dc, W - M, y_dc + 76], outline=RED, width=2)
    d.text((M + 8, y_dc + 5), "DATE CHECK — THESE ARE NOT 26 NOVEMBER",
           font=font(SANS_B, 11), fill=RED)
    f_dc = font(SANS, 10)
    for i, (item, when) in enumerate(DATE_CHECK):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        x0 = M + 8 + col * (CW / 2)
        yy = y_dc + 24 + row * 12
        d.text((x0, yy), "✕  " + item + " — " + when, font=f_dc, fill=INK)

    # --- footer
    f_f = font(SANS, 9)
    foot1 = ("Every story here happened or was first reported on Thursday "
             "26 November 2026. Sources are named on each story.")
    foot2 = ("HOW SURE:  OFFICIAL = government or institution  ·  "
             "CONFIRMED = named outlet  ·  REPORTED = one outlet  ·  "
             "CLAIM = unverified claim  ·  ONGOING = still unfolding.  "
             "Scenes are drawn illustrations, not photographs.")
    for j, line in enumerate((foot1, foot2)):
        tw = d.textlength(line, font=f_f)
        d.text((M + (CW - tw) / 2, 986 + j * 12), line, font=f_f, fill=GREY)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, "PNG", optimize=True)
    print("wrote", out)

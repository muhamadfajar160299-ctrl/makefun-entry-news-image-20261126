#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261126.

One image summing up the world news of Thursday 26 November 2026:
36 verified stories across 9 regions, 3 leads, 13 illustrated cards,
23 short text stories, a numbers sidebar, a map, a UTC timeline and a
date-check box. All illustrations are drawn here with plain shapes;
no photographs are used. Deterministic: same input, same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
CARD = (255, 253, 246)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
RED = (179, 32, 44)
GOLD = (176, 138, 30)
GREY = (96, 91, 80)
BORDER = (214, 206, 186)
LIGHT = (207, 200, 184)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def serif_b(s):
    return F("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return F("DejaVuSerif.ttf", s)


def sans_b(s):
    return F("DejaVuSans-Bold.ttf", s)


def sans(s):
    return F("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories

LEADS = [
    dict(kicker="WASHINGTON  •  TRADE", color=RED, art="tariffs",
         head="TRUMP'S NEW TARIFF SALVO",
         sub="US proposes duties on 14 partners \u2014 China up to 20%, EU 15%, "
             "India 25% \u2014 under Section 301. Hearing 25 January."),
    dict(kicker="PYONGYANG  •  NUCLEAR", color=RED, art="kim",
         head="KIM: SPREAD THE TACTICAL NUKES",
         sub="KCNA: Kim orders tactical nukes deployed \u201cacross multiple "
             "domains\u201d after touring arms plants."),
    dict(kicker="THE GULF  •  WAR", color=RED, art="gulf",
         head="FIRE IN THE GULF  \u25cb",
         sub="Houthis claim a hit on Ras Tanura, the biggest Saudi refinery; "
             "two tankers hit mines in Hormuz."),
]

CARDS2 = [
    dict(kicker="JERUSALEM  •  JUSTICE", color=NAVY2, art="court",
         head="JUDGES: DROP CASE 4000",
         sub="Judges urge dropping the Case 4000 bribery charge; rethink Case 2000."),
    dict(kicker="UKRAINE  •  WAR", color=NAVY2, art="jets",
         head="KYIV CLAIMS 5 JETS HIT  \u25cb",
         sub="Kyiv says 3 MiG-31s and 2 Su-34s hit at Savasleyka."),
    dict(kicker="CAIRO  •  DISASTER", color=NAVY2, art="tanker",
         head="31 DEAD IN CAIRO FIRE",
         sub="Tanker overturns on Cairo's Ring Road at Warraq; 31 killed, 21 hurt."),
    dict(kicker="NEW YORK  •  THANKSGIVING", color=NAVY2, art="parade",
         head="NO PARADE TODAY",
         sub="100th parade moves to Sat 28 Nov \u2014 first weather delay ever."),
]

CARDS3 = [
    dict(kicker="SPACE  •  CHINA", color=NAVY2, art="rocket",
         head="FIRST FOREIGNER ABOARD",
         sub="Shenzhou-24 docks at Tiangong; Muhammad Zeeshan Ali aboard."),
    dict(kicker="TECH  •  MARKETS", color=NAVY2, art="chip",
         head="S&P PUTS NVIDIA ON WATCH",
         sub="S&P puts Nvidia's AA rating on watch; shares fall 3.9% to $149.30."),
    dict(kicker="WALL STREET  •  MARKETS", color=NAVY2, art="chart",
         head="WALL ST'S WILD WEDNESDAY",
         sub="Dow plunges 1,100 intraday, then closes up 164; S&P \u22120.25%."),
]

CARDS4 = [
    dict(kicker="PYONGYANG  •  DIPLOMACY", color=NAVY2, art="swiss",
         head="SWISS ENVOY EXPELLED",
         sub="Pyongyang orders Swiss envoy Sylvain Astier out in 48 hours."),
    dict(kicker="WASHINGTON  •  THANKSGIVING", color=NAVY2, art="turkey",
         head="TURKEYS ARE SPARED",
         sub="Trump pardons Freedom and Feathers; both retire to Texas A&M."),
    dict(kicker="DHAKA  •  WORKERS", color=NAVY2, art="garment",
         head="GARMENT PAY UP 36%",
         sub="Garment pay up 36% to 17,000 taka after weeks of protests."),
]

TEXTS = [
    ("POLAND TO NATO: SHOOT THEM DOWN",
     "Warsaw asks allies to intercept Russian missiles over Ukraine."),
    ("SPAIN: TIKTOK ROW ROILS VOTE",
     "Maldita found 1,183 abuse videos, 48m views; vote is 29 Nov."),
    ("CHESS: 1\u20131 IN GENEVA",
     "Gukesh\u2013Sindarov draw Game 2 in 20 moves; Game 3 is played today."),
    ("HUAWEI GUILTY ON 10 OF 12",
     "Brooklyn jury convicts on trade secrets, bank fraud, Iran sanctions."),
    ("GIULIANI GETS MEDAL OF FREEDOM",
     "Trump honours the ex-NYC mayor in a private Oval Office ceremony."),
    ("PHONEPE REVIVES $12\u201315BN IPO",
     "India's payments giant to file within weeks; listing early 2027."),
    ("FLIPKART CHIEF STEPS DOWN",
     "Kalyan Krishnamurthy quits after 11 years; Thiagarajan leads interim."),
    ("US ECONOMY: Q3 GROWTH 4.3%",
     "Revised up from 3.4%, the fastest in three years."),
    ("KENYA: MACKENZIE CONVICTED AGAIN",
     "Cult leader, already serving 200 years for Shakahola, guilty again."),
    ("ANDY TAYLOR DIES AT 65",
     "Duran Duran's guitarist died at home on Monday; news confirmed Wed."),
    ("IPL AUCTION: 1,220 SIGN UP",
     "Players register for the 2027 Indian Premier League auction."),
    ("AUSTRALIA SIGNS SOLOMONS PACT",
     "Sweeping treaty as Honiara moves away from its China security pact."),
    ("LEBANON TO OPEN 2ND AIRPORT",
     "New gateway in the north next month as Hezbollah's sway fades."),
    ("NATIONS TO RUSSIA: STOP THE GAS",
     "Dozens of countries urge Moscow to halt alleged riot-agent use."),
    ("BIRTHRIGHT ORDER BLOCKED AGAIN",
     "A second judge halts Trump's order curtailing birthright citizenship."),
    ("MURMANSK GOVERNOR DETAINED",
     "Regional chief held for two months in a corruption case."),
    ("KING TIDES THREATEN US COASTS",
     "San Francisco Bay tides 2.8 ft above normal; waves to 30 ft."),
    ("NFL: THREE ON THANKSGIVING",
     "Bears\u2013Lions, Eagles\u2013Cowboys, Chiefs\u2013Bills fill the holiday slate."),
    ("INDIA MARKS CONSTITUTION DAY",
     "IITs to add 6,000 seats in robotics, AI and space technology."),
    ("INDIA AID FOR NEPAL: \u20b915,000 CR",
     "Package announced after Modi meets Nepal PM Balendra Shah."),
    ("GAZA: WINTER OUT OF REACH",
     "Winter survival goods stay beyond the grasp of families in need."),
    ("IOWA: ARMY BLASTS 4.5 TONNES",
     "Controlled detonation of lead azide called a \u201chuge success\u201d."),
    ("DUTERTE TRIAL: 100 WITNESSES",
     "ICC to call about 100 witnesses when the trial opens on 30 Nov."),
]

NUMBERS = [
    ("14", "trading partners in the new US tariff plan"),
    ("20%", "top proposed duty on China (40% if the truce fails)"),
    ("31", "killed in the Cairo tanker fire; 21 hurt"),
    ("5", "Russian jets Kyiv says it hit at Savasleyka"),
    ("\u22121,100", "points lost intraday, then closed +164"),
    ("4.3%", "US Q3 growth, revised up from 3.4%"),
    ("17,000", "taka: new Bangladesh garment wage (+36%)"),
    ("100th", "Macy's parade, postponed by weather for the first time"),
]

TIMELINE = [
    ("00\u201306 UTC", "KCNA: Kim orders wider tactical-nuke deployment. Cairo fire toll put at 31."),
    ("06\u201312 UTC", "Pyongyang expels Swiss envoy Astier. Dhaka approves +36% garment wage."),
    ("12\u201318 UTC", "USTR publishes tariff plan. Jerusalem judges urge dropping Case 4000."),
    ("18\u201324 UTC", "Macy's moves 100th parade to Saturday. Thanksgiving NFL triple-header kicks off."),
]

MAP_CITIES = [
    ("Washington", -77, 39), ("New York", -74, 41), ("Geneva", 6, 46),
    ("Warsaw", 21, 52), ("Madrid", -4, 40), ("Jerusalem", 35, 32),
    ("Cairo", 31, 30), ("Savasleyka", 43, 55), ("Dhaka", 90, 24),
    ("Pyongyang", 126, 39), ("Jiuquan", 99, 40), ("Honiara", 160, -9),
]


# ---------------------------------------------------------------- art
# Every illustration is drawn from plain shapes, with coordinates taken
# as fractions of the panel so the same drawing works at any card size.
# Keep them simple and recognisable at small size: one scene, two or
# three colours, no detail that turns to noise when the page shrinks.

def art_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 232, 242))
    d.rectangle([x, y + int(h * 0.82), x + w, y + h], fill=(52, 96, 140))
    cols = [(179, 32, 44), (201, 162, 39), (38, 90, 140), (46, 125, 70)]
    cw = w // 5
    for i, c in enumerate(cols):
        cx = x + 10 + i * cw
        d.rectangle([cx, y + int(h * 0.24), cx + cw - 5, y + int(h * 0.44)], fill=c)
        d.rectangle([cx, y + int(h * 0.48), cx + cw - 5, y + int(h * 0.68)], fill=c)
    d.polygon([(x + 6, y + int(h * 0.68)), (x + w - 6, y + int(h * 0.68)),
               (x + w - 20, y + int(h * 0.84)), (x + 20, y + int(h * 0.84))],
              fill=(20, 38, 74))
    d.rectangle([x + w - 30, y + 4, x + w - 6, y + 26], fill=(255, 255, 255))
    d.text((x + w - 28, y + 5), "%", font=sans_b(16), fill=(179, 32, 44))


def art_kim(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(20, 38, 74))
    for sx, sy in [(8, 8), (30, 20), (w - 14, 12), (w - 30, 30), (14, 44), (w - 8, 52)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    cx, cy, r = x + w - 32, y + int(h * 0.30), 12
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(179, 32, 44))
    mx = x + w // 2 - 8
    d.polygon([(mx, y + int(h * 0.10)), (mx + 16, y + int(h * 0.10)),
               (mx + 8, y + int(h * 0.02))], fill=(179, 32, 44))
    d.rectangle([mx, y + int(h * 0.10), mx + 16, y + int(h * 0.68)],
                fill=(240, 240, 235))
    d.rectangle([mx, y + int(h * 0.60), mx + 16, y + int(h * 0.68)],
                fill=(201, 162, 39))
    d.polygon([(mx - 6, y + int(h * 0.68)), (mx + 22, y + int(h * 0.68)),
               (mx + 8, y + int(h * 0.92))], fill=(232, 120, 30))
    d.rectangle([x, y + int(h * 0.92), x + w, y + h], fill=(46, 125, 70))


def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 196, 120))
    d.ellipse([x + w - 38, y + 6, x + w - 14, y + 30], fill=(232, 120, 30))
    base = y + int(h * 0.78)
    for i, th in enumerate([0.42, 0.55, 0.36]):
        tx = x + 12 + i * 26
        top = base - int(h * th)
        d.rectangle([tx, top, tx + 16, base], fill=(70, 70, 72))
        d.rectangle([tx + 5, top - 8, tx + 11, top], fill=(70, 70, 72))
        fx = tx + 8
        d.polygon([(fx - 6, top - 8), (fx, top - 8 - int(h * 0.14)),
                   (fx + 6, top - 8)], fill=(232, 80, 20))
    d.rectangle([x + 8, base, x + w - 8, base + 8], fill=(52, 52, 54))
    d.rectangle([x + w - 76, base + 2, x + w - 10, base + 12], fill=(20, 38, 74))
    d.rectangle([x + w - 68, base - 10, x + w - 54, base + 2], fill=(20, 38, 74))
    d.rectangle([x, y + int(h * 0.92), x + w, y + h], fill=(38, 90, 140))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    d.polygon([(x + 14, y + int(h * 0.30)), (x + w // 2, y + int(h * 0.08)),
               (x + w - 14, y + int(h * 0.30))], fill=(20, 38, 74))
    for i in range(4):
        cx = x + 24 + i * (w - 48) // 3
        d.rectangle([cx, y + int(h * 0.32), cx + 8, y + int(h * 0.82)],
                    fill=(255, 253, 246))
    d.rectangle([x + 12, y + int(h * 0.82), x + w - 12, y + int(h * 0.88)],
                fill=(20, 38, 74))
    d.rectangle([x + 8, y + int(h * 0.88), x + w - 8, y + int(h * 0.94)],
                fill=(20, 38, 74))
    d.rectangle([x + w - 42, y + int(h * 0.62), x + w - 14, y + int(h * 0.70)],
                fill=(120, 72, 32))
    d.rectangle([x + w - 29, y + int(h * 0.70), x + w - 25, y + int(h * 0.88)],
                fill=(120, 72, 32))


def art_jets(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(196, 210, 224))
    cx, cy = x + int(w * 0.78), y + int(h * 0.26)
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = int(h * 0.22) if i % 2 == 0 else int(h * 0.11)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(232, 120, 30))
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(201, 162, 39))
    jx, jy = x + 14, y + int(h * 0.60)
    d.polygon([(jx, jy + 10), (jx + 46, jy + 10), (jx + 62, jy + 4),
               (jx + 46, jy + 14), (jx + 20, jy + 18), (jx + 8, jy + 26),
               (jx + 4, jy + 14)], fill=(30, 30, 34))
    d.polygon([(jx + 30, jy + 10), (jx + 40, jy - 6), (jx + 44, jy + 10)],
              fill=(30, 30, 34))
    d.rectangle([x + 10, y + int(h * 0.82), x + 22, y + int(h * 0.94)],
                fill=(70, 70, 72))
    d.rectangle([x + 26, y + int(h * 0.86), x + 36, y + int(h * 0.94)],
                fill=(70, 70, 72))
    d.rectangle([x, y + int(h * 0.94), x + w, y + h], fill=(96, 91, 80))


def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    road = y + int(h * 0.80)
    d.rectangle([x, road, x + w, y + h], fill=(90, 86, 76))
    d.rectangle([x, road, x + w, road + 3], fill=(255, 255, 255))
    fx = x + w // 2
    d.polygon([(fx - 18, road), (fx - 5, y + int(h * 0.06)),
               (fx + 3, y + int(h * 0.34)), (fx + 14, y + int(h * 0.12)),
               (fx + 18, road)], fill=(232, 80, 20))
    d.polygon([(fx - 8, road), (fx, y + int(h * 0.26)), (fx + 8, road)],
              fill=(201, 162, 39))
    # truck: cab + cylinder tank
    d.rectangle([x + 12, road - 26, x + 34, road], fill=(179, 32, 44))
    d.rectangle([x + 16, road - 22, x + 30, road - 14], fill=(196, 220, 240))
    d.ellipse([x + 40, road - 26, x + w - 16, road], fill=(200, 200, 195))
    d.rectangle([x + 40, road - 26, x + w - 16, road - 13], fill=(210, 210, 205))
    d.ellipse([x + 18, road, x + 30, road + 10], fill=(30, 30, 30))
    d.ellipse([x + w - 30, road, x + w - 18, road + 10], fill=(30, 30, 30))


def art_parade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 236))
    for i, bh in enumerate([0.26, 0.40, 0.30, 0.48, 0.34]):
        bx = x + 8 + i * (w // 5)
        top = y + int(h * 0.82) - int(h * bh)
        d.rectangle([bx, top, bx + w // 5 - 8, y + int(h * 0.82)],
                    fill=(70, 84, 110))
    d.rectangle([x, y + int(h * 0.82), x + w, y + h], fill=(96, 91, 80))
    bx, by = x + w // 2, y + int(h * 0.40)
    rx, ry = min(30, w // 4), int(h * 0.26)
    d.ellipse([bx - rx, by - ry, bx + rx, by + ry], fill=(179, 32, 44))
    d.ellipse([bx - rx // 2, by - ry, bx + rx // 4, by + ry], fill=(201, 90, 90))
    d.line([bx - 12, by + ry, bx - 8, by + ry + 12], fill=(60, 60, 60), width=2)
    d.line([bx + 12, by + ry, bx + 8, by + ry + 12], fill=(60, 60, 60), width=2)
    d.rectangle([bx - 10, by + ry + 12, bx + 10, by + ry + 20], fill=(120, 72, 32))
    d.arc([x + 6, y + 6, x + 34, y + 22], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([x + w - 36, y + int(h * 0.55), x + w - 8, y + int(h * 0.55) + 16],
          200, 340, fill=(255, 255, 255), width=2)


def art_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sy in [(10, 10), (34, 26), (w - 12, 8), (w - 40, 40), (18, 58),
                   (w - 18, 66), (44, 8), (w - 60, 18)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    import math
    arc = [(x, y + h)]
    for i in range(21):
        t = i / 20.0
        arc.append((x + t * w, y + h - int(h * 0.14) * math.sin(math.pi * t)))
    arc.append((x + w, y + h))
    d.polygon(arc, fill=(38, 90, 140))
    d.rectangle([x + w - 78, y + 14, x + w - 14, y + 24], fill=(180, 180, 175))
    d.rectangle([x + w - 70, y + 6, x + w - 22, y + 14], fill=(52, 96, 140))
    d.rectangle([x + w - 70, y + 24, x + w - 22, y + 32], fill=(52, 96, 140))
    rx = x + 26
    d.polygon([(rx, y + int(h * 0.22)), (rx + 18, y + int(h * 0.22)),
               (rx + 9, y + int(h * 0.08))], fill=(179, 32, 44))
    d.rectangle([rx, y + int(h * 0.22), rx + 18, y + int(h * 0.70)],
                fill=(240, 240, 235))
    d.rectangle([rx + 4, y + int(h * 0.34), rx + 14, y + int(h * 0.46)],
                fill=(52, 96, 140))
    d.polygon([(rx - 6, y + int(h * 0.70)), (rx, y + int(h * 0.70)),
               (rx, y + int(h * 0.84))], fill=(179, 32, 44))
    d.polygon([(rx + 18, y + int(h * 0.70)), (rx + 24, y + int(h * 0.70)),
               (rx + 18, y + int(h * 0.84))], fill=(179, 32, 44))
    d.polygon([(rx + 2, y + int(h * 0.70)), (rx + 16, y + int(h * 0.70)),
               (rx + 9, y + int(h * 0.88))], fill=(232, 120, 30))


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 60, 40))
    s = min(42, int(h * 0.58))
    cx, cy = x + w // 2 - 34, y + int(h * 0.08)
    for i in range(5):
        px = cx + 6 + i * 10
        d.line([px, cy - 7, px, cy], fill=(201, 162, 39), width=3)
        d.line([px, cy + s, px, cy + s + 7], fill=(201, 162, 39), width=3)
        py = cy + 6 + i * 10
        d.line([cx - 7, py, cx, py], fill=(201, 162, 39), width=3)
        d.line([cx + s, py, cx + s + 7, py], fill=(201, 162, 39), width=3)
    d.rectangle([cx, cy, cx + s, cy + s], fill=(20, 38, 74))
    d.rectangle([cx + 11, cy + 11, cx + s - 11, cy + s - 11], fill=(28, 52, 96))
    d.text((cx + 14, cy + 13), "NV", font=sans_b(13), fill=(255, 255, 255))
    ax = x + w - 24
    d.line([ax, y + int(h * 0.10), ax, y + int(h * 0.62)], fill=(232, 80, 20),
           width=5)
    d.polygon([(ax - 9, y + int(h * 0.54)), (ax + 9, y + int(h * 0.54)),
               (ax, y + int(h * 0.72))], fill=(232, 80, 20))
    d.text((x + 10, y + h - 18), "$149.30  \u22123.9%", font=sans_b(11),
           fill=(255, 255, 255))


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 253, 246))
    for gy in [y + int(h * 0.25), y + int(h * 0.55), y + int(h * 0.85)]:
        d.line([x + 8, gy, x + w - 8, gy], fill=(230, 224, 210), width=1)
    vals = [0.85, 0.78, 0.62, 0.45, 0.30, 0.42, 0.55, 0.66, 0.74, 0.80]
    bw = (w - 20) // len(vals)
    for i, v in enumerate(vals):
        bx = x + 10 + i * bw
        top = y + int(h * 0.10) + (1 - v) * int(h * 0.78)
        col = (46, 125, 70) if i >= 5 else (179, 32, 44)
        d.rectangle([bx + 2, top, bx + bw - 3, y + int(h * 0.94)], fill=col)


def art_swiss(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 236))
    fx, fy, fs = x + 12, y + 8, min(40, int(h * 0.55))
    d.rectangle([fx, fy, fx + fs, fy + fs], fill=(179, 32, 44))
    d.rectangle([fx + fs // 2 - 4, fy + 7, fx + fs // 2 + 4, fy + fs - 7],
                fill=(255, 255, 255))
    d.rectangle([fx + 7, fy + fs // 2 - 4, fx + fs - 7, fy + fs // 2 + 4],
                fill=(255, 255, 255))
    px, py = x + w - 64, y + int(h * 0.52)
    d.polygon([(px, py + 8), (px + 52, py + 8), (px + 62, py + 4),
               (px + 52, py + 12), (px + 20, py + 14), (px + 8, py + 20),
               (px + 4, py + 10)], fill=(255, 255, 255))
    d.polygon([(px + 26, py + 8), (px + 34, py - 6), (px + 38, py + 8)],
              fill=(255, 255, 255))
    d.text((x + 12, y + h - 18), "48 HOURS TO LEAVE", font=sans_b(11),
           fill=(20, 38, 74))


def art_turkey(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 150))
    cx, cy = x + w // 2, y + int(h * 0.72)
    cols = [(179, 32, 44), (201, 162, 39), (46, 125, 70), (38, 90, 140),
            (232, 120, 30)]
    for i, c in enumerate(cols):
        ang = -160 + i * 35
        ex = cx + 32 * math.cos(math.radians(ang))
        ey = cy + 32 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=c, width=7)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=c)
    d.ellipse([cx - 20, cy - 22, cx + 20, cy + 10], fill=(120, 72, 32))
    d.ellipse([cx - 12, cy - 14, cx + 12, cy + 6], fill=(140, 88, 40))
    d.ellipse([cx + 8, cy - 34, cx + 24, cy - 18], fill=(120, 72, 32))
    d.polygon([(cx + 22, cy - 28), (cx + 32, cy - 25), (cx + 22, cy - 22)],
              fill=(232, 120, 30))
    d.ellipse([cx + 13, cy - 30, cx + 16, cy - 27], fill=(20, 20, 20))
    d.ellipse([x + w - 34, y + h - 26, x + w - 8, y + h - 6], fill=(232, 120, 30))
    d.rectangle([x + w - 23, y + h - 32, x + w - 19, y + h - 24],
                fill=(46, 125, 70))


def art_garment(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 200))
    sx, sy = x + 14, y + 8
    sh = int(h * 0.78)
    d.polygon([(sx + 18, sy), (sx + 52, sy), (sx + 70, sy + 14),
               (sx + 58, sy + 30), (sx + 52, sy + 24), (sx + 52, sy + sh),
               (sx + 18, sy + sh), (sx + 18, sy + 24), (sx + 12, sy + 30),
               (sx, sy + 14)], fill=(255, 253, 246))
    d.arc([sx + 26, sy - 4, sx + 44, sy + 12], 0, 180, fill=(179, 32, 44), width=3)
    d.text((x + w - 46, y + 8), "+36%", font=sans_b(13), fill=(179, 32, 44))
    for i in range(3):
        cy = y + h - 14 - i * 9
        d.ellipse([x + w - 40, cy - 5, x + w - 14, cy + 5], fill=(201, 162, 39))


ART = {"tariffs": art_tariffs, "kim": art_kim, "gulf": art_gulf,
       "court": art_court, "jets": art_jets, "tanker": art_tanker,
       "parade": art_parade, "rocket": art_rocket, "chip": art_chip,
       "chart": art_chart, "swiss": art_swiss, "turkey": art_turkey,
       "garment": art_garment}

# ---------------------------------------------------------------- layout
# Geometry, 1024 x 1024.
# Header 0-108. Leads 116-308 (3 x 256). Two rows of five narrow
# illustrated cards 316-486 and 494-664 (152 wide). Text zone 696-1000
# in four columns. Sidebar 800-1016: numbers, map, timeline, date check.

def draw_header(d):
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((16, 10), "THE WORLD IN ONE DAY", font=serif_b(34), fill=(246, 241, 229))
    d.text((W - 16, 16), "36 STORIES  \u2022  9 REGIONS",
           font=sans_b(13), fill=(201, 162, 39), anchor="ra")
    d.text((W - 16, 38), "ONE DAY  \u2022  ONE IMAGE",
           font=sans(11), fill=(180, 190, 210), anchor="ra")
    d.rectangle([16, 56, W - 16, 58], fill=(201, 162, 39))
    d.text((16, 64), "THURSDAY 26 NOVEMBER 2026", font=serif_b(40),
           fill=(255, 255, 255))
    d.rectangle([0, 104, W, 108], fill=RED)


def draw_card(d, x, y, w, h, c, size):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD, outline=BORDER, width=1)
    if size == "lead":
        kf, hf, sf, hl, sl, ah = sans_b(10), serif_b(19), sans(12), 21, 14, 78
        pad = 9
    else:
        kf, hf, sf, hl, sl, ah = sans_b(8), serif_b(12), sans(10), 14, 12, 70
        pad = 7
    d.text((x + pad, y + 5), c["kicker"], font=kf, fill=c["color"])
    ax, ay, aw = x + pad, y + 5 + 13, w - 2 * pad
    d.rectangle([ax, ay, ax + aw - 1, ay + ah - 1], outline=BORDER, width=1)
    ART[c["art"]](d, ax, ay, aw, ah)
    ty = ay + ah + 6
    head_lines = wrap(c["head"], hf, w - 2 * pad)
    ty = text_block(d, x + pad, ty, head_lines[:2], hf, NAVY, hl)
    sub_lines = wrap(c["sub"], sf, w - 2 * pad)
    text_block(d, x + pad, ty + 2, sub_lines[:3], sf, (52, 48, 40), sl)


def draw_text_zone(d):
    d.text((8, 672), "THE REST OF THE DAY", font=sans_b(12), fill=NAVY)
    d.rectangle([8, 690, 792, 692], fill=NAVY)
    cols = [TEXTS[0:6], TEXTS[6:12], TEXTS[12:18], TEXTS[18:23]]
    col_x = [8, 206, 404, 602]
    for ci, items in enumerate(cols):
        x = col_x[ci]
        y = 698
        for head, sub in items:
            hlines = wrap(head, sans_b(10), 190)
            y = text_block(d, x, y, hlines[:2], sans_b(10), NAVY, 11)
            slines = wrap(sub, sans(10), 190)
            y = text_block(d, x, y, slines[:2], sans(10), (52, 48, 40), 11)
            y += 6
    d.text((W // 2, 1006),
           "Sources: Reuters  \u2022  AP  \u2022  BBC  \u2022  CNN  \u2022  wires, 26 Nov 2026. "
           "All illustrations drawn for this page; no photographs.",
           font=sans(9), fill=GREY, anchor="ma")


def draw_numbers(d):
    x, y = 800, 116
    d.text((x, y), "THE DAY IN NUMBERS", font=sans_b(13), fill=NAVY)
    d.rectangle([x, y + 20, 1016, y + 22], fill=NAVY)
    y += 30
    for num, label in NUMBERS:
        d.text((x, y), num, font=sans_b(18), fill=RED)
        nw = sans_b(18).getlength(num)
        lab = wrap(label, sans(10), 208 - nw)
        text_block(d, x + nw + 8, y + 3, lab[:2], sans(10), INK, 12)
        y += 32
    return y


def draw_map(d, y):
    x = 800
    d.text((x, y), "WHERE IT HAPPENED", font=sans_b(13), fill=NAVY)
    d.rectangle([x, y + 20, 1016, y + 22], fill=NAVY)
    my = y + 30
    mw, mh = 216, 120
    d.rectangle([x, my, x + mw - 1, my + mh - 1], fill=(232, 228, 214),
                outline=BORDER, width=1)
    polys = [
        [(0.02, 0.18), (0.10, 0.08), (0.20, 0.10), (0.24, 0.18),
         (0.20, 0.28), (0.14, 0.34), (0.08, 0.30)],
        [(0.20, 0.42), (0.26, 0.40), (0.30, 0.48), (0.26, 0.62), (0.21, 0.55)],
        [(0.46, 0.14), (0.52, 0.10), (0.55, 0.16), (0.50, 0.22), (0.45, 0.20)],
        [(0.46, 0.30), (0.54, 0.28), (0.58, 0.38), (0.54, 0.55),
         (0.48, 0.50), (0.45, 0.38)],
        [(0.56, 0.08), (0.75, 0.06), (0.92, 0.12), (0.95, 0.22),
         (0.85, 0.30), (0.72, 0.28), (0.60, 0.22), (0.55, 0.14)],
        [(0.82, 0.62), (0.92, 0.60), (0.94, 0.68), (0.86, 0.70)],
    ]
    for poly in polys:
        pts = [(x + px * mw, my + py * mh) for px, py in poly]
        d.polygon(pts, fill=(203, 196, 178), outline=(170, 162, 140))
    for i, (name, lon, lat) in enumerate(MAP_CITIES, 1):
        px = x + (lon + 180) / 360.0 * mw
        py = my + (90 - lat) / 180.0 * mh
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + 4, py - 3), str(i), font=sans_b(8), fill=NAVY)
    ly = my + mh + 8
    for i, (name, lon, lat) in enumerate(MAP_CITIES, 1):
        col = 0 if i <= 6 else 1
        lx = x + col * 108
        ry = ly + (i - 1) % 6 * 11
        d.text((lx, ry), "%d  %s" % (i, name), font=sans(9), fill=INK)
    return ly + 6 * 11 + 8


def draw_timeline(d, y):
    x = 800
    d.text((x, y), "THE DAY IN UTC", font=sans_b(13), fill=NAVY)
    d.rectangle([x, y + 20, 1016, y + 22], fill=NAVY)
    y += 30
    for t, txt in TIMELINE:
        d.text((x, y), t, font=sans_b(10), fill=RED)
        lines = wrap(txt, sans(10), 216)
        text_block(d, x, y + 12, lines[:2], sans(10), INK, 11)
        y += 36
    return y


def draw_datecheck(d, y):
    x = 800
    d.rectangle([x, y, 1016, 1000], fill=(255, 253, 246), outline=NAVY, width=2)
    d.text((x + 10, y + 8), "DATE CHECK", font=sans_b(12), fill=NAVY)
    txt = ("Checked 26 Nov 2026 against Reuters, AP, BBC, CNN and wires. "
           "Most stories broke that day. Older: Andy Taylor died 23 Nov; "
           "Shenzhou-24 launched 25 Nov. Jet, refinery and mine claims are "
           "claims, not confirmed damage.")
    lines = wrap(txt, sans(10), 196)
    text_block(d, x + 10, y + 28, lines, sans(10), INK, 12)
    hy = y + 28 + len(lines) * 12 + 8
    d.text((x + 10, hy), "HOW SURE", font=sans_b(12), fill=NAVY)
    hy += 18
    for mark, label in [("\u25cf", "Confirmed by two or more wires"),
                        ("\u25d0", "One wire, or an official claim"),
                        ("\u25cb", "Claim, not independently confirmed")]:
        d.text((x + 10, hy), mark, font=sans(11), fill=RED)
        d.text((x + 28, hy), label, font=sans(9), fill=INK)
        hy += 13


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    for i, c in enumerate(LEADS):
        draw_card(d, 8 + i * 264, 116, 256, 192, c, "lead")
    narrow = CARDS2 + CARDS3 + CARDS4
    for i, c in enumerate(narrow[:5]):
        draw_card(d, 8 + i * 158, 316, 152, 170, c, "narrow")
    for i, c in enumerate(narrow[5:]):
        draw_card(d, 8 + i * 158, 494, 152, 170, c, "narrow")
    draw_text_zone(d)
    y = draw_numbers(d)
    y = draw_map(d, y + 8)
    y = draw_timeline(d, y + 8)
    draw_datecheck(d, y + 8)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")


if __name__ == "__main__":
    main()

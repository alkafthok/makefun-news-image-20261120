#!/usr/bin/env python3
"""Draw the one-day world news infographic for 20 November 2026 -> /output/entry.png"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
img = Image.new("RGB", (W, H), (16, 18, 24))
d = ImageDraw.Draw(img)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=True):
    f = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + f, int(size))

INK = (235, 238, 245)
MUT = (150, 158, 172)
RED = (232, 90, 84)
BLU = (110, 160, 228)
GRN = (110, 190, 140)
AMB = (235, 180, 70)
CARD = (26, 30, 40)

def center(x, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text((x - w / 2, y), text, font=font, fill=fill)

# header
d.rectangle([0, 0, W, 118], fill=(10, 12, 17))
center(W/2, 16, "THE WORLD IN ONE DAY", F(40), INK)
center(W/2, 66, "FRIDAY 20 NOVEMBER 2026", F(30), AMB)

CW, CH, GX, GY = 484, 268, 20, 18
X0, Y0 = 16, 140

def card(i, headline, lines, accent, icon=None):
    x = X0 + (i % 2) * (CW + GX)
    y = Y0 + (i // 2) * (CH + GY)
    d.rounded_rectangle([x, y, x+CW, y+CH], 14, fill=CARD)
    d.rounded_rectangle([x, y, x+8, y+CH], 4, fill=accent)
    d.text((x+26, y+18), headline, font=F(24), fill=accent)
    yy = y + 68
    for ln, big in lines:
        d.text((x+26, yy), ln, font=F(20, True) if big else F(17, False), fill=INK if big else MUT)
        yy += 34 if big else 27
    if icon:
        icon(x, y)

def ic_missiles(x, y):
    # missile trajectory arcs into a map dot
    cx, cy = x + CW - 150, y + CH - 90
    for k, (dx, dy) in enumerate([(-40, 60), (0, 70), (40, 60)]):
        d.arc([cx+dx-36, cy+dy-60, cx+dx+36, cy+dy+40], 200, 340, fill=RED, width=3)
    d.ellipse([cx-8, cy+58, cx+8, cy+74], fill=RED)
    d.text((cx-30, cy+80), "PL", font=F(18), fill=RED)

def ic_kyiv(x, y):
    cx, cy = x + CW - 90, y + CH - 106
    r = 26
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=AMB, width=3)
    d.ellipse([cx-9, cy-9, cx+9, cy+9], fill=AMB)
    for k in range(3):
        d.line([cx-40+k*30, cy-40, cx-30+k*30, cy-52], fill=AMB, width=3)

def ic_summit(x, y):
    bx = x + CW - 130
    for k, c in enumerate([(220, 80, 80), (235, 180, 70), (86, 140, 220)]):
        cx, cy = bx + k*44, y + CH - 112
        d.ellipse([cx-11, cy-24, cx+11, cy-2], fill=c)
        d.ellipse([cx-16, cy+2, cx+16, cy+42], outline=c, width=4)

def ic_gavel(x, y):
    cx, cy = x + CW - 80, y + CH - 104
    d.line([cx-26, cy+20, cx+26, cy+20], fill=GRN, width=5)
    d.line([cx, cy-16, cx, cy+20], fill=GRN, width=5)
    d.line([cx-20, cy-16, cx, cy+2], fill=GRN, width=4)
    d.line([cx+20, cy-16, cx, cy+2], fill=GRN, width=4)

def ic_flags(x, y):
    # EU stars + Union Jack-ish
    ex, ey = x + CW - 170, y + CH - 126
    d.ellipse([ex, ey, ex+52, ey+52], outline=BLU, width=3)
    for k in range(8):
        import math
        a = k * math.pi / 4
        d.ellipse([ex+23+16*math.cos(a)-2, ey+23+16*math.sin(a)-2,
                   ex+23+16*math.cos(a)+2, ey+23+16*math.sin(a)+2], fill=BLU)
    gx, gy = x + CW - 96, y + CH - 126
    d.rectangle([gx, gy, gx+52, gy+52], outline=MUT, width=2)
    d.line([gx, gy, gx+52, gy+52], fill=RED, width=5)
    d.line([gx+52, gy, gx, gy+52], fill=RED, width=5)
    d.line([gx+26, gy, gx+26, gy+52], fill=BLU, width=9)
    d.line([gx, gy+26, gx+52, gy+26], fill=BLU, width=9)
    d.line([gx+26, gy, gx+26, gy+52], fill=RED, width=4)
    d.line([gx, gy+26, gx+52, gy+26], fill=RED, width=4)

def ic_chart(x, y):
    cx, cy = x + CW - 170, y + CH - 128
    pts = [(0, 44), (28, 36), (56, 48), (84, 20), (112, 28), (140, 6)]
    for (a, b), (c2, e) in zip(pts, pts[1:]):
        d.line([cx+a, cy+b, cx+c2, cy+e], fill=GRN, width=4)
    d.ellipse([cx+137, cy+3, cx+143, cy+9], fill=GRN)

card(0, "RUSSIAN MISSILES LAND IN POLAND", [
    ("NATO calls it a violation", True),
    ("Struck during an 11-nation European", False),
    ("drill for a postwar Ukraine mission", False)], RED, ic_missiles)

card(1, "KYIV UNDER ATTACK", [
    ("Attacks kill 3, cut power, hit bridges", True),
    ("Ukraine braces for a 5th winter of war", False),
    ("aimed at its weakened energy grid", False)], AMB, ic_kyiv)

card(2, "TRUMP-XI-PUTIN SUMMIT", [
    ("Agree nuclear-weapons dialogue", True),
    ("Shenzhen APEC; Putin breaks isolation", False),
    ("UN reform pledged; results unclear", False)], BLU, ic_summit)

card(3, "ICJ: MYANMAR GUILTY", [
    ("Genocide against Rohingya minority", True),
    ("Historic ICJ ruling, welcomed by", False),
    ("Rohingya refugees in Bangladesh", False)], GRN, ic_gavel)

card(4, "UK-EU HOLD RARE SUMMIT", [
    ("PM Burnham in Brussels to mend", True),
    ("ties broken by Brexit, 10 years on", False),
    ("Youth mobility deal on the table", False)], BLU, ic_flags)

card(5, "ANTHROPIC IPO: BIGGEST EVER", [
    ("Debut opens at $111.50, +30% spike", True),
    ("AI-bubble fear: Taiwan's Taiex falls", False),
    ("6.2% in a week-long market rout", False)], GRN, ic_chart)

# footer strip
d.rectangle([0, H-118, W, H], fill=(10, 12, 17))
d.text((40, H-106), "ALSO THAT DAY", font=F(18, True), fill=AMB)
footer = [
    ("Climate talks overtime;", "fossil fuels left out"),
    ("Houthi missile hits Riyadh", "tallest skyscraper"),
    ("Denmark-US-Greenland", "security deal approved"),
    ("Fiji declares disaster", "in El Nino drought"),
    ("Fiona the hippo dies", "at Cincinnati Zoo"),
]
fx = 40
for a, b in footer:
    d.text((fx, H-74), a, font=F(13), fill=INK)
    d.text((fx, H-52), b, font=F(13), fill=MUT)
    fx += 196
    if fx < W-150:
        d.line([fx-20, H-76, fx-20, H-42], fill=(50, 56, 70), width=2)

os.makedirs("/output", exist_ok=True)
img.save("/output/entry.png", optimize=True)
img.save("/root/makefun/entry_preview.png", optimize=True)
print("saved", os.path.getsize("/output/entry.png"), "bytes")

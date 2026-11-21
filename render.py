#!/usr/bin/env python3
"""Render 'The World in One Day - Saturday 21 November 2026' as a 1024x1024
broadsheet front page. Reads stories.json, writes entry.png next to itself.
Deterministic: no clock, no randomness, no network, fixed PNG parameters."""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (250, 244, 230)
INK = (26, 22, 18)
RED = (176, 32, 24)
BLUE = (28, 58, 110)
GREY = (112, 102, 90)
RULE = (198, 188, 172)
GOLD = (232, 190, 90)
DARK = (24, 30, 48)
MUTED_FILL = (203, 192, 168)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIFB = lambda s: font("DejaVuSerif-Bold.ttf", s)
# No DejaVuSerif-Italic.ttf is installed, so the ticker uses regular serif.
SERIFI = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, text, cx, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rr = r if i % 2 == 0 else r * 0.42
        import math
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    draw.polygon(pts, fill=fill)


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        stories = json.load(fh)
    by_n = {s["n"]: s for s in stories}

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 16
    CW = W - 2 * MX

    # ---- top strip ----
    centre(d, "38 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
           W // 2, 7, SANSB(11), RED)
    d.line([(MX, 24), (W - MX, 24)], fill=INK, width=2)

    # ---- masthead ----
    centre(d, "Saturday 21 November 2026", W // 2, 30, SERIFB(38), INK)
    centre(d, "Missiles land in Poland  ·  Nasdaq −5.3%  ·  Kyiv bridges hit  ·  COP31 runs into overtime",
           W // 2, 76, SERIFI(15), BLUE)
    d.line([(MX, 98), (W - MX, 98)], fill=RULE, width=1)

    # ---- numbers strip: six boxes ----
    nums = [("3", "objects over Poland"), ("−5.3%", "Nasdaq"),
            ("110 + 400", "missiles and drones over Ukraine"),
            ("$58,317", "Bitcoin"), ("+898", "Sensex points"), ("4.2", "LA quake")]
    bw = (CW - 5 * 6) / 6
    y0 = 104
    for i, (num, lab) in enumerate(nums):
        x = MX + i * (bw + 6)
        d.rectangle([x, y0, x + bw, y0 + 44], outline=RULE, width=1, fill=(255, 251, 242))
        centre(d, num, x + bw / 2, y0 + 4, SERIFB(19), RED if i in (1, 3) else INK)
        centre(d, lab, x + bw / 2, y0 + 28, SANS(8), GREY)

    # ---- region colour bar ----
    regions = [("Europe", 9, (28, 58, 110)), ("Asia", 6, (176, 32, 24)),
               ("Middle East", 6, (120, 70, 20)), ("Africa", 3, (40, 110, 70)),
               ("Americas", 9, (90, 40, 110)), ("Oceania", 1, (150, 110, 20)),
               ("Global", 4, (70, 70, 70))]
    y0 = 154
    x = MX
    total = 38
    for name, count, col in regions:
        segw = CW * count / total
        d.rectangle([x, y0, x + segw - 1, y0 + 22], fill=col)
        label = f"{name} {count}" if segw >= 60 else (f"{count}" if segw < 40 else f"{name[:3]} {count}")
        centre(d, label, x + segw / 2, y0 + 5, SANSB(9), (255, 255, 255))
        x += segw
    d.text((MX, y0 + 24), "", font=SANS(8), fill=GREY)

    # ---- lead row: three big panels ----
    leads = [by_n[1], by_n[2], by_n[3]]
    ly, lh = 182, 190
    pw = (CW - 2 * 8) / 3
    for i, s in enumerate(leads):
        x = MX + i * (pw + 8)
        d.rectangle([x, ly, x + pw, ly + lh], outline=RULE, width=1, fill=(255, 251, 242))
        # number badge
        d.rectangle([x, ly, x + 24, ly + 20], fill=RED)
        d.text((x + 8, ly + 3), str(s["n"]), font=SANSB(12), fill=(255, 255, 255))
        # illustration
        ix, iy, iw, ih = x + 1, ly + 21, pw - 2, 60
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=DARK)
        if s["n"] == 1:
            for sx, sy in [(30, 12), (90, 8), (160, 16), (230, 10), (280, 18)]:
                d.ellipse([ix + sx, iy + sy, ix + sx + 3, iy + sy + 3], fill=GOLD)
            d.line([(ix + 20, iy + 58), (ix + 150, iy + 22), (ix + 250, iy + 30)],
                   fill=(255, 255, 255), width=2)
            d.polygon([(ix + 245, iy + 22), (ix + 258, iy + 26), (ix + 250, iy + 34)],
                      fill=(255, 255, 255))
            star(d, ix + 262, iy + 32, 16, (255, 170, 40))
            star(d, ix + 262, iy + 32, 8, (255, 220, 120))
            d.polygon([(ix + 10, iy + 60), (ix + 60, iy + 46), (ix + 120, iy + 60)],
                      fill=(60, 60, 70))
            d.polygon([(ix + 180, iy + 60), (ix + 230, iy + 48), (ix + 290, iy + 60)],
                      fill=(60, 60, 70))
        elif s["n"] == 2:
            for gx in range(0, int(iw), 32):
                d.line([(ix + gx, iy), (ix + gx, iy + ih)], fill=(50, 58, 80), width=1)
            for gy in range(0, ih, 16):
                d.line([(ix, iy + gy), (ix + iw, iy + gy)], fill=(50, 58, 80), width=1)
            d.line([(ix + 10, iy + 12), (ix + 80, iy + 18), (ix + 150, iy + 34),
                    (ix + 220, iy + 48), (ix + iw - 12, iy + 60)],
                   fill=(230, 60, 40), width=3)
            d.polygon([(ix + iw - 22, iy + 52), (ix + iw - 8, iy + 58), (ix + iw - 20, iy + 64)],
                      fill=(230, 60, 40))
            d.text((ix + 8, iy + 4), "−14%", font=SANSB(13), fill=(255, 120, 100))
        else:
            d.rectangle([ix, iy + 44, ix + iw, iy + 52], fill=(90, 90, 100))
            for tx in (70, 170, 260):
                d.rectangle([ix + tx, iy + 12, ix + tx + 6, iy + 52], fill=(120, 120, 130))
            d.line([(ix + 10, iy + 46), (ix + 73, iy + 14)], fill=(150, 150, 160), width=1)
            d.line([(ix + 76, iy + 14), (ix + 173, iy + 46)], fill=(150, 150, 160), width=1)
            d.line([(ix + 176, iy + 46), (ix + 263, iy + 14)], fill=(150, 150, 160), width=1)
            star(d, ix + 120, iy + 30, 14, (255, 170, 40))
            star(d, ix + 230, iy + 26, 11, (255, 170, 40))
            d.ellipse([ix + 108, iy + 40, ix + 132, iy + 52], fill=(255, 120, 60))
        ty = ly + 21 + 60 + 6
        d.text((x + 8, ty), f"{s['kicker']}  ·  {s['region'].upper()}",
               font=SANSB(10), fill=RED)
        ty += 15
        ty = draw_lines(d, wrap(d, s["headline"], SERIFB(16), pw - 16),
                        x + 8, ty, SERIFB(16), INK, 18)
        ty += 2
        ty = draw_lines(d, wrap(d, s["deck"], SANS(10), pw - 16)[:3],
                        x + 8, ty, SANS(10), INK, 12)
        d.text((x + 8, ty + 3), f"({s['source']})", font=SANS(9), fill=GREY)

    # ---- medium rows: ten panels, two rows of five ----
    meds = [by_n[n] for n in range(4, 14)]
    mw = (CW - 4 * 8) / 5
    mh = 100
    art_cols = [(28, 58, 110), (120, 70, 20), (176, 32, 24), (40, 110, 70),
                (90, 40, 110), (150, 110, 20), (70, 70, 70), (28, 58, 110),
                (176, 32, 24), (40, 110, 70)]
    for row in range(2):
        y = 378 + row * (mh + 6)
        for col in range(5):
            s = meds[row * 5 + col]
            x = MX + col * (mw + 8)
            d.rectangle([x, y, x + mw, y + mh], outline=RULE, width=1,
                        fill=(255, 251, 242))
            d.rectangle([x, y, x + 20, y + 16], fill=BLUE)
            d.text((x + 6, y + 2), str(s["n"]), font=SANSB(10), fill=(255, 255, 255))
            ax, ay, aw, ah = x + 1, y + 17, mw - 2, 30
            d.rectangle([ax, ay, ax + aw, ay + ah], fill=art_cols[s["n"] - 4])
            if s["n"] == 4:
                d.ellipse([ax + 60, ay + 4, ax + 120, ay + 26], outline=GOLD, width=2)
                d.line([(ax + 10, ay + 15), (ax + aw - 10, ay + 15)], fill=GOLD, width=2)
            elif s["n"] == 5:
                d.line([(ax + 20, ay + 6), (ax + 20, ay + 24)], fill=(255, 255, 255), width=2)
                d.line([(ax + 20, ay + 6), (ax + 170, ay + 6)], fill=(255, 255, 255), width=2)
                d.polygon([(ax + 55, ay + 10), (ax + 75, ay + 10), (ax + 65, ay + 22)],
                          outline=(255, 255, 255))
                d.polygon([(ax + 115, ay + 10), (ax + 135, ay + 10), (ax + 125, ay + 22)],
                          outline=(255, 255, 255))
            elif s["n"] == 6:
                d.polygon([(ax + 85, ay + 4), (ax + 105, ay + 22), (ax + 65, ay + 22)],
                          fill=GOLD)
                d.line([(ax + 10, ay + 25), (ax + aw - 10, ay + 25)], fill=(255, 255, 255), width=2)
            elif s["n"] == 7:
                d.line([(ax + 30, ay + 24), (ax + 85, ay + 6)], fill=(255, 255, 255), width=2)
                star(d, ax + 88, ay + 8, 7, (255, 170, 40))
                d.polygon([(ax + 110, ay + 24), (ax + 140, ay + 24), (ax + 125, ay + 8)],
                          outline=(255, 255, 255))
            elif s["n"] == 8:
                for fx in (30, 75, 120):
                    d.rectangle([ax + fx, ay + 6, ax + fx + 28, ay + 24], outline=GOLD, width=2)
            elif s["n"] == 9:
                d.line([(ax + 10, ay + 15), (ax + aw - 10, ay + 15)], fill=(255, 255, 255), width=3)
                for bx in (50, 95, 140):
                    d.rectangle([ax + bx, ay + 8, ax + bx + 8, ay + 22], fill=RED)
            elif s["n"] == 10:
                d.ellipse([ax + 70, ay + 3, ax + 100, ay + 27], outline=GOLD, width=3)
                d.text((ax + 80, ay + 8), "₿", font=SANSB(13), fill=GOLD)
                d.line([(ax + 10, ay + 22), (ax + 60, ay + 22), (ax + 110, ay + 12),
                        (ax + 160, ay + 8)], fill=(255, 120, 100), width=2)
            elif s["n"] == 11:
                d.line([(ax + 10, ay + 24), (ax + 60, ay + 18), (ax + 110, ay + 10),
                        (ax + 170, ay + 5)], fill=(120, 220, 120), width=3)
            elif s["n"] == 12:
                d.line([(ax + 10, ay + 15), (ax + 50, ay + 15), (ax + 65, ay + 6),
                        (ax + 80, ay + 24), (ax + 95, ay + 10), (ax + 140, ay + 15),
                        (ax + 180, ay + 15)], fill=(255, 255, 255), width=2)
            else:
                d.polygon([(ax + 20, ay + 22), (ax + 60, ay + 6), (ax + 110, ay + 6),
                           (ax + 160, ay + 22)], fill=(255, 255, 255))
                d.ellipse([ax + 82, ay + 14, ax + 92, ay + 24], fill=INK)
                d.ellipse([ax + 110, ay + 14, ax + 120, ay + 24], fill=INK)
            ty = y + 50
            d.text((x + 6, ty), f"{s['kicker']}  ·  {s['region'].upper()}",
                   font=SANSB(8), fill=RED)
            ty += 12
            ty = draw_lines(d, wrap(d, s["headline"], SANSB(11), mw - 12)[:3],
                            x + 6, ty, SANSB(11), INK, 13)
            d.text((x + 6, y + mh - 12), f"({s['source']})", font=SANS(8), fill=GREY)

    # ---- markets strip ----
    y0 = 590
    d.text((MX, y0), "MARKETS IN ONE GLANCE", font=SANSB(11), fill=INK)
    cells = [("Nasdaq", "−5.3%", -5.3, RED), ("S&P 500", "−3.7%", -3.7, RED),
             ("Dow", "−1.9%", -1.9, RED), ("Nvidia", "−14%", -14.0, RED),
             ("Bitcoin", "$58,317", -4.0, RED), ("Sensex", "+898", 2.0, (40, 110, 70))]
    cw2 = (CW - 5 * 6) / 6
    for i, (lab, val, pct, col) in enumerate(cells):
        x = MX + i * (cw2 + 6)
        d.rectangle([x, y0 + 16, x + cw2, y0 + 44], outline=RULE, width=1,
                    fill=(255, 251, 242))
        d.text((x + 6, y0 + 19), lab, font=SANSB(9), fill=INK)
        d.text((x + cw2 - 52, y0 + 19), val, font=SANSB(9), fill=col)
        barw = max(6, int(abs(pct) / 14.0 * (cw2 - 12)))
        d.rectangle([x + 6, y0 + 35, x + 6 + barw, y0 + 40], fill=col)

    # ---- world map strip ----
    y0 = 646
    d.text((MX, y0), "WHERE IT HAPPENED", font=SANSB(11), fill=INK)
    d.text((MX + 150, y0), "—  each number is that story on this page",
           font=SANS(10), fill=GREY)
    mx0, my0, mw2, mh2 = MX, y0 + 16, CW, 62
    d.rectangle([mx0, my0, mx0 + mw2, my0 + mh2], outline=RULE, width=1,
                fill=(238, 232, 214))
    continents = [
        [(60, 8), (180, 4), (225, 14), (205, 34), (150, 38), (95, 28), (55, 18)],
        [(218, 36), (258, 40), (248, 58), (228, 56)],
        [(458, 8), (520, 4), (538, 24), (500, 34), (468, 28)],
        [(468, 36), (528, 36), (548, 56), (508, 60), (480, 52)],
        [(540, 4), (748, 4), (758, 32), (650, 42), (558, 28)],
        [(758, 50), (798, 50), (798, 60), (762, 60)],
    ]
    for poly in continents:
        d.polygon([(mx0 + px, my0 + py) for px, py in poly], fill=MUTED_FILL)
    pins = {1: (498, 20), 2: (170, 24), 3: (518, 28), 4: (530, 38), 5: (466, 10),
            6: (582, 30), 7: (562, 44), 8: (488, 26), 9: (534, 8), 10: (202, 28),
            11: (640, 34), 12: (116, 28), 13: (142, 38)}
    for n, (px, py) in pins.items():
        cx, cy = mx0 + px, my0 + py
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx - 3 if n < 10 else cx - 6, cy - 6), str(n), font=SANSB(8),
               fill=(255, 255, 255))

    # ---- also on Saturday: stories 14-38, two columns ----
    y0 = 736
    d.text((MX, y0), "ALSO ON SATURDAY 21 NOVEMBER — 25 MORE STORIES",
           font=SANSB(12), fill=INK)
    d.line([(MX, y0 + 17), (W - MX, y0 + 17)], fill=INK, width=1)
    colw = (CW - 16) / 2
    fnt = SANS(10)
    for ci, group in enumerate([range(14, 27), range(27, 39)]):
        x = MX + ci * (colw + 16)
        yy = y0 + 22
        for n in group:
            s = by_n[n]
            text = f"{n}. {s['deck']} ({s['source']})"
            lines = wrap(d, text, fnt, colw)
            yy = draw_lines(d, lines, x, yy, fnt, INK, 12)
            yy += 1
    # ---- date check box ----
    y0 = 958
    d.rectangle([MX, y0, W - MX, y0 + 34], outline=RED, width=1)
    d.text((MX + 8, y0 + 4), "DATE CHECK", font=SANSB(9), fill=RED)
    wrap_lines = wrap(d, "Left out as Thursday's news: the Shenzhen declaration itself; the US "
                         "Senate's 51–48 Iran vote; the ICJ verdict itself — shown here only "
                         "through Saturday's follow-ups.", SANS(9), CW - 110)
    draw_lines(d, wrap_lines, MX + 82, y0 + 4, SANS(9), INK, 12)

    # ---- footer ----
    centre(d, "Every story here happened, or was first reported, on Saturday 21 November 2026. "
              "Officials' counts are attributed.", W // 2, 998, SANS(9), GREY)
    centre(d, "Sources: AP · AFP · Reuters · WSJ · CNN · UN News · PTI · NASA · USGS",
           W // 2, 1010, SANS(9), GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the news-image-20261119 entry: a one-page front page for 19 Nov 2026.

Deterministic, no network. Draws with PIL only, DejaVu fonts.
Writes entry.png next to this script (1024x1024, PNG).
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (0, 0, 0)
PAPER = (255, 255, 255)
RED = (178, 0, 0)
GREY = (90, 90, 90)
LIGHT = (235, 235, 235)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, weight=2, x0=None, x1=None):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    stripe = h / 13
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(179, 25, 66))
    cw, ch = w * 0.4, h * 7 / 13
    draw.rectangle([x, y, x + cw, y + ch], fill=(10, 49, 97))
    for r in range(3):
        for c in range(4):
            cx = x + 8 + c * (cw - 16) / 3
            cy = y + 7 + r * (ch - 14) / 2
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    # one large star + four small stars, drawn as simple 5-point stars
    def star(cx, cy, r):
        import math
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=(255, 222, 0))
    star(x + w * 0.22, y + h * 0.30, h * 0.22)
    for sx, sy in [(0.55, 0.18), (0.68, 0.32), (0.68, 0.52), (0.55, 0.66)]:
        star(x + w * sx, y + h * sy, h * 0.09)


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=(255, 255, 255))
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 0, 50))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    title = "NINETEEN"
    tf = SERIF_B(108)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=INK)
    rule(d, 148, 3)
    date_f = SANS_B(27)
    date_txt = "THURSDAY  19  NOVEMBER  2026"
    dw = d.textlength(date_txt, font=date_f)
    d.text(((W - dw) / 2, 158), date_txt, font=date_f, fill=RED)
    tag_f = SANS(20)
    tag_txt = "THE WORLD IN ONE PAGE"
    gw = d.textlength(tag_txt, font=tag_f)
    d.text(((W - gw) / 2, 192), tag_txt, font=tag_f, fill=INK)
    rule(d, 224, 2)
    rule(d, 229, 1)

    # ---- Lead story ----
    y = 244
    kick_f = SANS_B(17)
    d.text((MARGIN, y), "LEAD STORY  •  SHENZHEN, CHINA", font=kick_f, fill=RED)
    y += 26
    head_f = SERIF_B(40)
    y = draw_wrapped(d, MARGIN, y,
                     "Trump, Xi and Putin meet today in Shenzhen",
                     head_f, W - 2 * MARGIN, 46)
    y += 4
    # body left, three-flag motif right
    body_x, body_w = MARGIN, 610
    motif_x, motif_w = 690, 298
    body_f = SANS(18)
    body = ("The first-ever three-way meeting of the three leaders, on the "
            "APEC sidelines at Kylin Villa. Trump arrived on 18 November and was "
            "welcomed by Xi; a bilateral meeting and a working lunch come first.")
    y_body = draw_wrapped(d, body_x, y, body, body_f, body_w, 22)
    body2 = ("Agenda: Ukraine, Iran, trade, AI and nuclear arms. The "
             "US\u2013China trade truce expires 10 January 2027 \u2014 soybeans, "
             "rare earths and tariffs at stake.")
    y_body = draw_wrapped(d, body_x, y_body + 6, body2, body_f, body_w, 22)
    # motif: three stacked flags with labels
    fy = y
    fh = 42
    for draw_flag, label in [(flag_us, "UNITED STATES"),
                             (flag_cn, "CHINA"),
                             (flag_ru, "RUSSIA")]:
        draw_flag(d, motif_x, fy, 150, fh)
        d.text((motif_x + 160, fy + 11), label, font=SANS_B(16), fill=INK)
        fy += fh + 10
    rule(d, 534, 2)

    # ---- Second story ----
    y = 548
    d.text((MARGIN, y), "US\u2013IRAN EXCHANGE OF FIRE WIDENS", font=SERIF_B(29), fill=INK)
    y += 36
    y = draw_wrapped(d, MARGIN, y,
                     "Iran struck a US base in Kuwait and hit the Bahrain radar again "
                     "on 18 November. The US struck a missile site on Iran\u2019s "
                     "Qeshm Island on 17 November.",
                     SANS(19), W - 2 * MARGIN, 25)
    rule(d, 638, 1)

    # ---- Third story ----
    y = 652
    d.text((MARGIN, y), "EU PROPOSES \u20ac45 BILLION LOAN FOR UKRAINE",
           font=SERIF_B(29), fill=INK)
    y += 36
    y = draw_wrapped(d, MARGIN, y,
                     "The loan would be repaid from Russian reparations.",
                     SANS(19), W - 2 * MARGIN, 25)
    rule(d, 726, 1)

    # ---- Fourth story ----
    y = 740
    d.text((MARGIN, y), "GRAND THEFT AUTO VI LAUNCHES WORLDWIDE TODAY",
           font=SERIF_B(29), fill=INK)
    y += 36
    y = draw_wrapped(d, MARGIN, y,
                     "The long-awaited game arrives today, scoring 99 on Metacritic, "
                     "as the global rollout gets under way.",
                     SANS(19), W - 2 * MARGIN, 25)

    # ---- Bottom strip: The Day in Brief ----
    strip_y = 840
    d.rectangle([MARGIN, strip_y, W - MARGIN, strip_y + 32], fill=INK)
    d.text((MARGIN + 12, strip_y + 6), "THE DAY IN BRIEF",
           font=SANS_B(19), fill=PAPER)
    items = [
        "NASA\u2019s Voyager 1 reaches one light-day from Earth.",
        "The UN court (ICJ) rules today in The Gambia v. Myanmar over the Rohingya.",
        "Cyclone Akvan nears India\u2019s east coast; landfall between Machilipatnam and Puri.",
        "Democrats nominate Hakeem Jeffries for Speaker of the US House.",
        "Nvidia halts H-series chip shipments to China after founder Jensen Huang\u2019s resignation.",
        "Fed minutes point to further rate rises.",
    ]
    iy = strip_y + 42
    col_w = (W - 2 * MARGIN) // 2
    for i, item in enumerate(items):
        col = i % 2
        row = i // 2
        x = MARGIN + col * col_w
        yy = iy + row * 40
        d.text((x, yy), "\u2022", font=SANS_B(16), fill=RED)
        draw_wrapped(d, x + 16, yy, item, SANS(15), col_w - 24, 19)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render one 1920x1080 PNG slide per scene for the Static Factory video."""

import os
import sys
import matplotlib
from PIL import Image, ImageDraw, ImageFont

from scenes import SCENES

W, H = 1920, 1080

BG = (15, 23, 42)
PANEL = (30, 41, 59)
TEXT = (226, 232, 240)
MUTED = (148, 163, 184)
ACCENT = (167, 139, 250)
CLIENT = (56, 189, 248)
HIDDEN = (251, 191, 36)
PINK = (244, 114, 182)
RED = (248, 113, 113)
GREEN = (52, 211, 153)
LINE = (71, 85, 105)

FONT_DIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def base_slide():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=ACCENT)
    return img, d


def gradient(img, top, bottom):
    """A vertical wash, used by the poster and the sign-off card."""
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))


def footer(d, label):
    d.text((70, H - 58), label, font=f(SANS, 24), fill=(80, 94, 118))
    d.text((W - 70, H - 58), "Static Factory Method  ·  Java 21",
           font=f(SANS, 24), fill=(80, 94, 118), anchor="ra")


def draw_title(d, text):
    d.text((100, 92), text, font=f(SANS_B, 62), fill=TEXT)
    d.line([(100, 190), (W - 100, 190)], fill=LINE, width=2)


def kind_title(scene, img, d):
    d.text((W // 2, 400), scene["title"], font=f(SANS_B, 104), fill=TEXT, anchor="ma")
    y = 580
    for ln in scene["body"]:
        d.text((W // 2, y), ln, font=f(SANS, 42), fill=MUTED, anchor="ma")
        y += 72
    d.line([(W // 2 - 220, 545), (W // 2 + 220, 545)], fill=ACCENT, width=4)


def kind_bullets(scene, img, d):
    draw_title(d, scene["title"])
    y = 275
    for ln in scene["body"]:
        col = TEXT
        fnt = f(SANS, 40)
        if ln.startswith("✗"):
            col = RED
        elif ln.startswith("✓"):
            col = GREEN
        elif "←" in ln or "→" in ln:
            # an annotated line: keep it the same size as its siblings
            col = ACCENT
            if "   " in ln.strip():
                fnt = f(MONO, 30)
        elif "   " in ln.strip():
            # a multi-column line: mono keeps the columns lined up
            fnt = f(MONO, 30)
        d.text((110, y), ln, font=fnt, fill=col)
        y += 62


def kind_quote(scene, img, d):
    draw_title(d, scene["title"])
    d.rectangle([100, 260, 112, 800], fill=ACCENT)
    y = 290
    for ln in scene["body"]:
        col = TEXT
        fnt = f(SANS, 44)
        if ln.startswith("—"):
            col, fnt = MUTED, f(SANS, 34)
        elif ln.startswith("In plain") or ln.startswith("Instead of"):
            col, fnt = ACCENT, f(SANS_B, 42)
        d.text((150, y), ln, font=fnt, fill=col)
        y += 62


def fit_mono(lines, max_w, max_h, line_ratio, start=34, floor=16):
    """Largest mono font size where the block fits the given box."""
    for size in range(start, floor - 1, -1):
        lh = int(size * line_ratio)
        if lh * len(lines) + 56 > max_h:
            continue
        fnt = f(MONO_B, size)
        widest = max((fnt.getlength(ln) for ln in lines), default=0)
        if widest <= max_w:
            return size, lh
    return floor, int(floor * line_ratio)


def kind_code(scene, img, d):
    draw_title(d, scene["title"])
    lines = scene["body"].split("\n")
    top = 250
    avail_h = (H - 110) - top
    size, lh = fit_mono(lines, W - 272, avail_h, 1.52)
    box_h = lh * len(lines) + 56
    d.rounded_rectangle([100, top, W - 100, top + box_h],
                        radius=16, fill=(2, 6, 23), outline=LINE, width=2)
    y = top + 28
    for ln in lines:
        col = TEXT
        fnt = f(MONO, size)
        s = ln.strip()
        if s.startswith("//") or s.startswith("..."):
            col = (100, 180, 130)
        elif s.startswith("error:"):
            col = RED
            fnt = f(MONO_B, size)
        elif s.startswith("if (") or s.startswith("throw"):
            col = RED
        elif s.startswith("return new") or s.startswith("new "):
            col = PINK
        elif s.startswith("return"):
            col = CLIENT
        elif s.startswith("this."):
            col = CLIENT
        elif s.startswith("static ") or s.startswith("public static"):
            col = HIDDEN
            fnt = f(MONO_B, size)
        elif s.startswith("public") or s.startswith("private") or s.startswith("final class"):
            col = HIDDEN
            fnt = f(MONO_B, size)
        elif s.startswith(("Discount ", "Money ")):
            col = ACCENT
        d.text((136, y), ln, font=fnt, fill=col)
        y += lh


def kind_console(scene, img, d):
    draw_title(d, scene["title"])
    lines = scene["body"].split("\n")
    top = 250
    size, lh = fit_mono(lines, W - 272, (H - 110) - top, 1.62, start=32)
    d.rounded_rectangle([100, top, W - 100, top + lh * len(lines) + 56],
                        radius=16, fill=(2, 6, 23), outline=LINE, width=2)
    y = top + 28
    for ln in lines:
        col = TEXT
        if ln.startswith("$"):
            col = MUTED
        elif ln.startswith("Rejected"):
            col = RED
        elif ln.startswith("Coupon"):
            col = PINK
        elif "shared: true" in ln:
            col = HIDDEN
        elif "->" in ln:
            col = ACCENT
        elif "total" in ln:
            col = GREEN
        elif ln.startswith("Checkout"):
            col = TEXT
        d.text((136, y), ln, font=f(MONO, size), fill=col)
        y += lh


def box(d, x, y, w, h, label, sub, colour, label_size=30):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=colour, width=3)
    size = label_size
    while size > 14 and f(SANS_B, size).getlength(label) > w - 28:
        size -= 1
    if sub:
        d.text((x + w // 2, y + h // 2 - 26), label, font=f(SANS_B, size),
               fill=TEXT, anchor="ma")
        d.text((x + w // 2, y + h // 2 + 14), sub, font=f(SANS, 22),
               fill=MUTED, anchor="ma")
    else:
        d.text((x + w // 2, y + h // 2 - 14), label, font=f(SANS_B, size),
               fill=TEXT, anchor="ma")


def arrow(d, x1, y1, x2, y2, colour, width=3):
    d.line([(x1, y1), (x2, y2)], fill=colour, width=width)
    d.polygon([(x2 - 10, y2 - 16), (x2 + 10, y2 - 16), (x2, y2)], fill=colour)


def kind_diagram(scene, img, d):
    """The package boundary: one public door, five classes nobody can name."""
    draw_title(d, scene["title"])

    box(d, 700, 226, 520, 100, "Your code", "the Client", CLIENT)
    arrow(d, 960, 326, 960, 392, LINE)
    d.text((980, 340), "Discount.percentage(10)", font=f(MONO, 24), fill=MUTED)

    # the public door
    d.rounded_rectangle([120, 392, W - 120, 600], radius=18, outline=ACCENT, width=3)
    d.text((150, 410), "PUBLIC  —  THE ONLY WAY IN", font=f(SANS_B, 22), fill=ACCENT)

    box(d, 660, 444, 600, 110, "Discount",
        "public interface  ·  six static factory methods", ACCENT)

    centres = [280, 620, 960, 1300, 1640]

    bus_y = 626
    d.line([(960, 554), (960, bus_y)], fill=LINE, width=2)
    d.line([(centres[0], bus_y), (centres[-1], bus_y)], fill=LINE, width=2)

    # everything the caller cannot see
    d.rounded_rectangle([120, 668, W - 120, 838], radius=18, outline=HIDDEN, width=3)
    d.text((W // 2, 678), "PACKAGE-PRIVATE  —  YOUR CODE CANNOT NAME ANY OF THESE",
           font=f(SANS_B, 22), fill=HIDDEN, anchor="ma")

    impls = ["NoDiscount", "PercentageDiscount", "AmountOffDiscount",
             "FreeShippingDiscount", "BestOfDiscount"]

    for name, cx in zip(impls, centres):
        arrow(d, cx, bus_y, cx, 716, LINE, 2)
        box(d, cx - 160, 716, 320, 100, name, "", HIDDEN, label_size=24)

    d.text((W // 2, 886),
           "the method picks the class — the caller only ever sees Discount",
           font=f(SANS_B, 32), fill=PINK, anchor="ma")
    d.text((W // 2, 940),
           "Rename all five tomorrow. Nothing breaks.",
           font=f(SANS_B, 34), fill=TEXT, anchor="ma")


AUTHOR = "Jayasekhar Konduru"

# The poster doubles as the YouTube thumbnail, so everything on it has to
# survive being shrunk to about 320 pixels wide in a search result: few
# words, very large type, and strong colour contrast.
POSTER_TOP = (49, 16, 92)
POSTER_BOTTOM = (10, 18, 58)


def pill(d, x, y, w, h, colour, code, note, strike=False):
    d.rounded_rectangle([x, y, x + w, y + h], radius=22,
                        fill=(12, 18, 46), outline=colour, width=5)
    fnt = f(MONO_B, 42)
    while fnt.getlength(code) > w - 60:
        fnt = f(MONO_B, fnt.size - 2)
    cx, cy = x + w // 2, y + 34
    d.text((cx, cy), code, font=fnt, fill=TEXT, anchor="ma")
    if strike:
        half = fnt.getlength(code) / 2
        d.line([(cx - half, cy + 26), (cx + half, cy + 26)], fill=colour, width=6)
    d.text((cx, y + h - 58), note, font=f(SANS_B, 34), fill=colour, anchor="ma")


def kind_poster(scene, img, d):
    """Title card and YouTube thumbnail in one."""
    gradient(img, POSTER_TOP, POSTER_BOTTOM)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=HIDDEN)
    d.text((110, 88), "DESIGN PATTERNS  -  JAVA",
           font=f(SANS_B, 36), fill=HIDDEN)

    d.text((110, 156), "STATIC FACTORY", font=f(SANS_B, 128), fill=TEXT)
    d.text((110, 296), "METHOD", font=f(SANS_B, 128), fill=ACCENT)

    d.rectangle([110, 462, 620, 472], fill=PINK)

    # One box around the whole idea — the two call sites and the sentence that
    # explains them — so the tagline reads as part of the pattern rather than
    # as a caption floating under it.
    d.rounded_rectangle([110, 516, W - 110, 842], radius=26,
                        outline=ACCENT, width=4)

    pill(d, 150, 556, 700, 170, RED, "new Discount(10)",
         "cannot be named", strike=True)
    pill(d, 1070, 556, 700, 170, GREEN, "Discount.percentage(10)",
         "says what it means")

    arrow_y = 636
    d.line([(880, arrow_y), (1010, arrow_y)], fill=TEXT, width=8)
    d.polygon([(1010, arrow_y - 22), (1010, arrow_y + 22), (1052, arrow_y)],
              fill=TEXT)

    d.text((W // 2, 758), "Give the constructor a name",
           font=f(SANS_B, 54), fill=TEXT, anchor="ma")

    # Bottom left, on the same edge as the eyebrow, the title and the rule, so
    # the card has one alignment rather than a centred name under left-aligned
    # everything else. It also keeps clear of YouTube's furniture: the duration
    # badge sits bottom right, and the watched-progress bar covers the last
    # forty pixels or so of the height.
    byline = "by " + AUTHOR
    fnt = f(SANS_B, 54)
    pill_w = int(fnt.getlength(byline)) + 96
    d.rounded_rectangle([110, 896, 110 + pill_w, 1000], radius=52,
                        fill=(12, 18, 46), outline=CLIENT, width=4)
    d.text((110 + pill_w // 2, 918), byline, font=fnt,
           fill=CLIENT, anchor="ma")


def kind_outro(scene, img, d):
    """The sign-off card: like, subscribe, and who made it."""
    gradient(img, POSTER_BOTTOM, POSTER_TOP)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=HIDDEN)

    d.text((W // 2, 150), scene["title"], font=f(SANS_B, 96), fill=TEXT, anchor="ma")
    d.line([(W // 2 - 240, 290), (W // 2 + 240, 290)], fill=PINK, width=6)

    labels = [("LIKE", GREEN), ("SUBSCRIBE", RED), ("SHARE", CLIENT)]
    box_w, gap = 480, 60
    left = (W - (box_w * 3 + gap * 2)) // 2
    for i, (label, colour) in enumerate(labels):
        x = left + i * (box_w + gap)
        d.rounded_rectangle([x, 350, x + box_w, 490], radius=24,
                            fill=(12, 18, 46), outline=colour, width=5)
        d.text((x + box_w // 2, 388), label, font=f(SANS_B, 58),
               fill=colour, anchor="ma")

    y = 580
    for ln in scene["body"]:
        d.text((W // 2, y), ln, font=f(SANS, 42), fill=MUTED, anchor="ma")
        y += 66

    d.rounded_rectangle([560, 880, 1360, 978], radius=49,
                        fill=(12, 18, 46), outline=CLIENT, width=4)
    d.text((W // 2, 902), "by " + AUTHOR, font=f(SANS_B, 54),
           fill=CLIENT, anchor="ma")


RENDERERS = {
    "poster": kind_poster,
    "outro": kind_outro,
    "title": kind_title,
    "bullets": kind_bullets,
    "quote": kind_quote,
    "code": kind_code,
    "console": kind_console,
    "diagram": kind_diagram,
}


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build"
    os.makedirs(out_dir, exist_ok=True)
    for i, scene in enumerate(SCENES, start=1):
        img, d = base_slide()
        RENDERERS[scene["kind"]](scene, img, d)
        if scene["kind"] not in ("title", "poster", "outro"):
            footer(d, "%d / %d" % (i, len(SCENES)))
        path = os.path.join(out_dir, scene["key"] + ".png")
        img.save(path)
        print("slide  ->", path)


if __name__ == "__main__":
    main()

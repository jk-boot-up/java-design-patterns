#!/usr/bin/env python3
"""Render one 1920x1080 PNG slide per scene for the Abstract Factory video."""

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
UK = (52, 211, 153)
US = (251, 191, 36)
INDIA = (34, 211, 238)
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


def footer(d, label):
    d.text((70, H - 58), label, font=f(SANS, 24), fill=(80, 94, 118))
    d.text((W - 70, H - 58), "Abstract Factory  ·  Java 21",
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
        elif ln.startswith("In plain") or ln.startswith("choose "):
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
        elif s.startswith("if (") or s.startswith("} else") or s.startswith("throw"):
            col = RED
        elif s.startswith("return new"):
            col = PINK
        elif s.startswith("return"):
            col = CLIENT
        elif s.startswith("this."):
            col = CLIENT
        elif s.startswith("public"):
            col = US
            fnt = f(MONO_B, size)
        elif s.startswith(("TaxCalculator", "CurrencyFormatter", "AddressValidator",
                           "String ", "double ")):
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
        elif "£" in ln:
            col = UK
        elif "$1" in ln or "$120" in ln or "USD" in ln or "Sales Tax" in ln:
            col = US
        elif "₹" in ln:
            col = INDIA
        elif ln.startswith("Checkout"):
            col = ACCENT
        d.text((136, y), ln, font=f(MONO, size), fill=col)
        y += lh


def box(d, x, y, w, h, label, sub, colour, label_size=30):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=colour, width=3)
    size = label_size
    while size > 16 and f(SANS_B, size).getlength(label) > w - 32:
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


def kind_grid(scene, img, d):
    """The 3x3 product grid, with each family boxed as a row."""
    draw_title(d, scene["title"])

    cols = ["TaxCalculator", "CurrencyFormatter", "AddressValidator"]
    rows = [
        ("United Kingdom", UK,
         ["UkVatCalculator", "PoundFormatter", "UkPostcodeValidator"]),
        ("United States", US,
         ["UsSalesTaxCalculator", "DollarFormatter", "UsZipValidator"]),
        ("India", INDIA,
         ["IndiaGstCalculator", "RupeeFormatter", "IndiaPinValidator"]),
    ]

    left = 130
    label_w = 300
    cell_w = 440
    gap = 20
    grid_x = left + label_w + 30

    # column headers
    for c, name in enumerate(cols):
        cx = grid_x + c * (cell_w + gap) + cell_w // 2
        d.text((cx, 250), name, font=f(SANS_B, 28), fill=PINK, anchor="ma")
        d.text((cx, 288), "interface", font=f(SANS, 20), fill=MUTED, anchor="ma")

    top = 350
    row_h = 118
    row_gap = 50

    for r, (market, colour, cells) in enumerate(rows):
        y = top + r * (row_h + row_gap)

        # the family outline: this row is the unit of choice
        d.rounded_rectangle(
            [left - 16, y - 16, grid_x + 3 * cell_w + 2 * gap + 16, y + row_h + 16],
            radius=18, outline=colour, width=3)

        d.text((left + 8, y + row_h // 2 - 34), market,
               font=f(SANS_B, 30), fill=colour)
        d.text((left + 8, y + row_h // 2 + 6), "one family",
               font=f(SANS, 22), fill=MUTED)

        for c, cell in enumerate(cells):
            x = grid_x + c * (cell_w + gap)
            box(d, x, y, cell_w, row_h, cell, "", colour, label_size=27)

    d.text((W // 2, 880),
           "Read down a column: an ordinary interface.   Read across a row: a family.",
           font=f(SANS_B, 32), fill=TEXT, anchor="ma")
    d.text((W // 2, 936),
           "Nine classes.  Only three combinations are legal.",
           font=f(SANS, 28), fill=MUTED, anchor="ma")


def kind_diagram(scene, img, d):
    draw_title(d, scene["title"])

    box(d, 700, 232, 520, 100, "CheckoutService", "the Client", CLIENT)
    arrow(d, 960, 332, 960, 396, LINE)
    d.text((980, 348), "new CheckoutService(factory)", font=f(SANS, 24), fill=MUTED)

    d.rounded_rectangle([120, 396, W - 120, 762], radius=18,
                        outline=ACCENT, width=3)
    d.text((150, 414), "ABSTRACT FACTORY", font=f(SANS_B, 22), fill=ACCENT)

    box(d, 700, 442, 520, 100, "MarketFactory",
        "3 creation methods, no market", ACCENT)

    factories = [
        ("UkMarketFactory", "VAT · £ · postcode", UK),
        ("UsMarketFactory", "Sales Tax · $ · ZIP", US),
        ("IndiaMarketFactory", "GST · ₹ · PIN", INDIA),
    ]
    centres = [400, 960, 1520]

    bus_y = 586
    d.line([(960, 542), (960, bus_y)], fill=LINE, width=2)
    d.line([(centres[0], bus_y), (centres[-1], bus_y)], fill=LINE, width=2)

    for (name, sub, col), cx in zip(factories, centres):
        arrow(d, cx, bus_y, cx, 622, LINE, 2)
        box(d, cx - 250, 622, 500, 110, name, sub, col)

    products = [
        ("TaxCalculator", PINK),
        ("CurrencyFormatter", PINK),
        ("AddressValidator", PINK),
    ]
    # one bus out of the shell, then into each product interface: every
    # factory produces all three kinds, not one each
    out_y = 782
    d.line([(960, 762), (960, out_y)], fill=LINE, width=2)
    d.line([(centres[0], out_y), (centres[-1], out_y)], fill=LINE, width=2)
    for (name, col), cx in zip(products, centres):
        arrow(d, cx, out_y, cx, 806, LINE, 2)
        box(d, cx - 250, 806, 500, 76, name, "", col, label_size=28)

    d.text((W // 2, 916),
           "each factory builds one complete, matching family",
           font=f(SANS_B, 32), fill=PINK, anchor="ma")
    d.text((W // 2, 966),
           "You pick a set, never a piece.",
           font=f(SANS_B, 34), fill=TEXT, anchor="ma")


RENDERERS = {
    "title": kind_title,
    "bullets": kind_bullets,
    "quote": kind_quote,
    "code": kind_code,
    "console": kind_console,
    "diagram": kind_diagram,
    "grid": kind_grid,
}


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build"
    os.makedirs(out_dir, exist_ok=True)
    for i, scene in enumerate(SCENES, start=1):
        img, d = base_slide()
        RENDERERS[scene["kind"]](scene, img, d)
        if scene["kind"] != "title":
            footer(d, "%d / %d" % (i, len(SCENES)))
        path = os.path.join(out_dir, scene["key"] + ".png")
        img.save(path)
        print("slide  ->", path)


if __name__ == "__main__":
    main()

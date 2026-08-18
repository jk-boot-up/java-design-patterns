#!/usr/bin/env python3
"""Render one 1920x1080 PNG slide per scene for the Factory Method video."""

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
GREEN = (52, 211, 153)
AMBER = (251, 191, 36)
ROSE = (251, 113, 133)
CYAN = (34, 211, 238)
PINK = (244, 114, 182)
RED = (248, 113, 113)
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
    d.text((W - 70, H - 58), "Factory Method  ·  Java 21",
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
        elif "←" in ln:
            # an annotated step: keep it the same size as its siblings
            col = ACCENT
        elif ln.strip().startswith(tuple("1234")) and "." in ln[:6]:
            col = CLIENT
            if "   " in ln.strip():
                fnt = f(MONO, 32)
        elif "   " in ln.strip():
            # a two-column line: mono keeps the columns lined up
            fnt = f(MONO, 32)
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
        elif ln.startswith("In plain") or ln.startswith("leave "):
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
        if s.startswith("//"):
            col = (100, 180, 130)
        elif s.startswith("if (") or s.startswith("} else"):
            col = ROSE
        elif s.startswith("return new") or s.startswith("Courier courier ="):
            col = PINK
        elif s.startswith("return"):
            col = CLIENT
        elif s.startswith("public"):
            col = AMBER
            fnt = f(MONO_B, size)
        elif s.startswith("protected"):
            col = ACCENT
            fnt = f(MONO_B, size)
        elif s.startswith("System.out"):
            col = MUTED
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
        elif ln.startswith(("Standard", "Express", "Same Day", "International")):
            col = ACCENT
        elif ln.startswith("Royal Post"):
            col = GREEN
        elif ln.startswith("SkyLink Air"):
            col = AMBER
        elif ln.startswith("CityRide"):
            col = ROSE
        elif ln.startswith("TransWorld"):
            col = CYAN
        elif ln.startswith(" "):
            col = MUTED
        d.text((136, y), ln, font=f(MONO, size), fill=col)
        y += lh


def box(d, x, y, w, h, label, sub, colour):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=colour, width=3)
    # shrink the label until it clears the box sides
    size = 30
    while size > 18 and f(SANS_B, size).getlength(label) > w - 40:
        size -= 1
    d.text((x + w // 2, y + h // 2 - 26), label, font=f(SANS_B, size),
           fill=TEXT, anchor="ma")
    d.text((x + w // 2, y + h // 2 + 14), sub, font=f(SANS, 22),
           fill=MUTED, anchor="ma")


def arrow(d, x1, y1, x2, y2, colour, width=3):
    d.line([(x1, y1), (x2, y2)], fill=colour, width=width)
    d.polygon([(x2 - 10, y2 - 16), (x2 + 10, y2 - 16), (x2, y2)], fill=colour)


def kind_diagram(scene, img, d):
    draw_title(d, scene["title"])

    box(d, 760, 240, 400, 110, "FactoryMethodDemo", "the Client", CLIENT)
    arrow(d, 960, 350, 960, 420, LINE)
    d.text((980, 370), "service.ship(order)", font=f(SANS, 24), fill=MUTED)

    d.rounded_rectangle([120, 420, W - 120, 790], radius=18,
                        outline=ACCENT, width=3)
    d.text((150, 438), "CREATOR", font=f(SANS_B, 22), fill=ACCENT)

    box(d, 760, 470, 400, 110, "DeliveryService",
        "abstract createCourier()", ACCENT)

    creators = [
        ("StandardDelivery", "new PostalCourier()", GREEN),
        ("ExpressDelivery", "new AirCourier()", AMBER),
        ("SameDayDelivery", "new BikeCourier()", ROSE),
        ("InternationalDelivery", "new GlobalCourier()", CYAN),
    ]
    centres = [175 + 190 + 400 * i for i in range(4)]

    # vertical stub down from the creator, then a horizontal bus, then a
    # straight drop into each subclass -- no crossing lines
    bus_y = 615
    d.line([(960, 580), (960, bus_y)], fill=LINE, width=2)
    d.line([(centres[0], bus_y), (centres[-1], bus_y)], fill=LINE, width=2)

    for (name, sub, col), cx in zip(creators, centres):
        arrow(d, cx, bus_y, cx, 650, LINE, 2)
        box(d, cx - 190, 650, 380, 110, name, sub, col)

    d.text((W // 2, 830),
           "returns a Courier  —  never a concrete carrier",
           font=f(SANS_B, 32), fill=PINK, anchor="ma")
    d.text((W // 2, 886),
           "The parent writes the call.  The child decides what comes back.",
           font=f(SANS_B, 34), fill=TEXT, anchor="ma")
    d.text((W // 2, 940),
           "There is no switch anywhere in this project.",
           font=f(SANS, 28), fill=MUTED, anchor="ma")


RENDERERS = {
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
        if scene["kind"] != "title":
            footer(d, "%d / %d" % (i, len(SCENES)))
        path = os.path.join(out_dir, scene["key"] + ".png")
        img.save(path)
        print("slide  ->", path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render one 1920x1080 PNG slide per scene for the Singleton Pattern video."""

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
ENUM = (52, 211, 153)
LEGACY = (251, 191, 36)
CLIENT = (56, 189, 248)
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
    d.text((W - 70, H - 58), "Singleton Pattern  ·  Java 21",
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
            col = ACCENT
            if "   " in ln.strip():
                fnt = f(MONO, 30)
        elif "   " in ln.strip():
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
        elif ln.startswith("In plain") or ln.startswith("The question"):
            col, fnt = ACCENT, f(SANS_B, 40)
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
        elif s.startswith("if (") or s.startswith("throw"):
            col = RED
        elif s.startswith("return new") or s.startswith("new "):
            col = PINK
        elif s.startswith("return"):
            col = CLIENT
        elif s.startswith("counter"):
            col = CLIENT
        elif s.startswith("static ") or s.startswith("public static"):
            col = LEGACY
            fnt = f(MONO_B, size)
        elif s.startswith("public") or s.startswith("private") or s.startswith("final class"):
            col = LEGACY
            fnt = f(MONO_B, size)
        elif s.startswith(("OrderSequenceGenerator", "LegacyOrderSequenceGenerator",
                            "INSTANCE", "AtomicLong", "Constructor")):
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
        elif ln.startswith("=="):
            col = ACCENT
        elif "false" in ln:
            col = RED
        elif "true" in ln:
            col = GREEN
        elif ln.startswith("ORD-"):
            col = LEGACY
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
    """Every caller reaches one enum constant -> three JVM guarantees protect it,
    contrasted with the legacy shape where the same two attacks both land."""
    draw_title(d, scene["title"])

    box(d, 700, 216, 520, 90, "Every caller", "checkout, admin, retry job", CLIENT)
    arrow(d, 960, 306, 960, 366, LINE)

    box(d, 660, 366, 600, 84, "OrderSequenceGenerator.INSTANCE", "", ENUM, label_size=26)
    arrow(d, 960, 450, 960, 500, LINE)

    d.rounded_rectangle([120, 500, W - 120, 660], radius=18, outline=ENUM, width=3)
    d.text((W // 2, 512), "THREE GUARANTEES, ZERO EXTRA CODE",
           font=f(SANS_B, 24), fill=ENUM, anchor="ma")
    box(d, 150, 556, 520, 84, "class loading", "JVM builds it once, thread-safe by the JLS", ENUM, label_size=22)
    box(d, 700, 556, 520, 84, "reflection", "newInstance() rejects enum types", ENUM, label_size=22)
    box(d, 1250, 556, 520, 84, "serialization", "resolved by name, not rebuilt from bytes", ENUM, label_size=22)

    d.line([(120, 700), (W - 120, 700)], fill=LINE, width=2)
    d.text((W // 2, 712), "the same two attacks, aimed at the classic shape instead",
           font=f(SANS, 26), fill=MUTED, anchor="ma")

    box(d, 700, 760, 520, 84, "LegacyOrderSequenceGenerator", "private constructor + static field", LEGACY, label_size=24)
    arrow(d, 860, 844, 500, 900, RED)
    arrow(d, 1060, 844, 1420, 900, RED)

    box(d, 220, 900, 560, 100, "reflection: forged instance", "setAccessible(true) bypasses \"private\"", RED, label_size=24)
    box(d, 1140, 900, 560, 100, "serialization: new instance", "no constructor call, counter resets", RED, label_size=24)

    d.text((W // 2, 1030), "one shape closes both holes for free; the other needs readResolve() and still allows one",
           font=f(SANS_B, 24), fill=MUTED, anchor="ma")


AUTHOR = "Jayasekhar Konduru"

POSTER_TOP = (49, 16, 92)
POSTER_BOTTOM = (10, 18, 58)


def pill(d, x, y, w, h, colour, code, note, tag=None):
    """A code sample in a coloured box, with a one-line verdict under it.

    `tag` puts a small chip on the top edge -- BEFORE on the rejected
    approach, AFTER on the pattern. That chip replaces the strikethrough the
    "before" sample used to carry. A rule drawn through monospace is hard to
    read at full size and illegible at the ~360 px wide thumbnail YouTube
    actually serves in search results, which is the size that decides whether
    anyone clicks; and striking the code out made the card read as being about
    what is wrong rather than about what is worth learning. The contrast is
    still there, carried by colour and by the label instead.
    """
    d.rounded_rectangle([x, y, x + w, y + h], radius=22,
                        fill=(12, 18, 46), outline=colour, width=5)
    if tag:
        tag_font = f(SANS_B, 26)
        tag_w = int(tag_font.getlength(tag)) + 44
        d.rounded_rectangle([x + 28, y - 20, x + 28 + tag_w, y + 20],
                            radius=20, fill=colour)
        d.text((x + 28 + tag_w // 2, y - 16), tag, font=tag_font,
               fill=(12, 18, 46), anchor="ma")
    fnt = f(MONO_B, 42)
    while fnt.getlength(code) > w - 60:
        fnt = f(MONO_B, fnt.size - 2)
    d.text((x + w // 2, y + 46), code, font=fnt, fill=TEXT, anchor="ma")
    d.text((x + w // 2, y + h - 58), note, font=f(SANS_B, 34), fill=colour,
           anchor="ma")


def kind_poster(scene, img, d):
    """Title card and YouTube thumbnail in one."""
    gradient(img, POSTER_TOP, POSTER_BOTTOM)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=LEGACY)
    d.text((110, 88), "DESIGN PATTERNS  -  JAVA",
           font=f(SANS_B, 36), fill=LEGACY)

    d.text((110, 156), "SINGLETON", font=f(SANS_B, 128), fill=TEXT)
    d.text((110, 296), "PATTERN", font=f(SANS_B, 128), fill=ACCENT)

    d.rectangle([110, 462, 620, 472], fill=PINK)

    d.rounded_rectangle([110, 516, W - 110, 842], radius=26,
                        outline=ACCENT, width=4)

    pill(d, 150, 556, 700, 170, RED, "ctor.newInstance()",
         "breaks a private constructor", tag="BEFORE")
    pill(d, 1070, 556, 700, 170, GREEN, "enum INSTANCE",
         "the JVM won't allow a second", tag="AFTER")

    arrow_y = 636
    d.line([(880, arrow_y), (1010, arrow_y)], fill=TEXT, width=8)
    d.polygon([(1010, arrow_y - 22), (1010, arrow_y + 22), (1052, arrow_y)],
              fill=TEXT)

    d.text((W // 2, 758), "Exactly one instance, actually enforced",
           font=f(SANS_B, 50), fill=TEXT, anchor="ma")

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

    d.rectangle([0, 0, W, 14], fill=LEGACY)

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

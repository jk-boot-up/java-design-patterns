#!/usr/bin/env python3
"""Render one 1920x1080 PNG slide per scene for the Idempotent Consumer video."""

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
    d.text((W - 70, H - 58), "Idempotent Consumer  ·  Java 21",
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
    y = 260
    for ln in scene["body"]:
        col = TEXT
        fnt = f(SANS, 40)
        if ln.startswith("✗"):
            col = RED
        elif ln.startswith("✓"):
            col = GREEN
        elif ln.strip().startswith(tuple("1234")) and "." in ln[:6]:
            col = CLIENT
        d.text((110, y), ln, font=fnt, fill=col)
        y += 60


def kind_quote(scene, img, d):
    draw_title(d, scene["title"])
    # A bare string here would be iterated character by character, which puts
    # one letter on each line. Guard against it rather than trusting the data.
    body = scene["body"]
    if isinstance(body, str):
        raise TypeError("quote body must be a list of lines, not a string")
    d.rectangle([100, 260, 112, 860], fill=ACCENT)
    y = 290
    for ln in body:
        col = TEXT
        fnt = f(SANS, 42)
        if ln.startswith("—"):
            col, fnt = MUTED, f(SANS, 34)
        elif ln.startswith("In plain") or ln.startswith("hand out") \
                or ln.startswith("so nobody"):
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
        elif s.startswith("throw"):
            col = ROSE
        elif s.startswith("return"):
            col = CLIENT
        elif s.startswith("public"):
            col = AMBER
            fnt = f(MONO_B, size)
        elif s.startswith("private") or s.startswith("static") or s.startswith("protected"):
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
        elif ln.startswith("=="):
            col = ACCENT
        elif ln.strip().startswith("["):
            col = GREEN
        elif ln.startswith(" ") or ln.startswith("  "):
            col = MUTED
        d.text((136, y), ln, font=f(MONO, size), fill=col)
        y += lh


def box(d, x, y, w, h, label, sub, colour, label_size=30, sub_size=22):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=colour, width=3)
    fnt = f(SANS_B, label_size)
    while fnt.getlength(label) > w - 24 and fnt.size > 14:
        fnt = f(SANS_B, fnt.size - 2)
    sub_fnt = f(SANS, sub_size)
    while sub_fnt.getlength(sub) > w - 20 and sub_fnt.size > 12:
        sub_fnt = f(SANS, sub_fnt.size - 1)
    d.text((x + w // 2, y + h // 2 - 26), label, font=fnt, fill=TEXT, anchor="ma")
    d.text((x + w // 2, y + h // 2 + 14), sub, font=sub_fnt, fill=MUTED, anchor="ma")


def arrow(d, x1, y1, x2, y2, colour, width=3):
    """Arrow with the head at (x2, y2), pointing downwards."""
    d.line([(x1, y1), (x2, y2)], fill=colour, width=width)
    d.polygon([(x2 - 10, y2 - 16), (x2 + 10, y2 - 16), (x2, y2)], fill=colour)


def arrow_right(d, x1, y, x2, colour, width=3):
    d.line([(x1, y), (x2, y)], fill=colour, width=width)
    d.polygon([(x2 - 16, y - 10), (x2 - 16, y + 10), (x2, y)], fill=colour)


def arrow_up(d, x, y1, y2, colour, width=3):
    d.line([(x, y1), (x, y2)], fill=colour, width=width)
    d.polygon([(x - 10, y2 + 16), (x + 10, y2 + 16), (x, y2)], fill=colour)


def arrow_left(d, x1, y, x2, colour, width=3):
    """Arrow with the head at (x2, y), pointing leftwards."""
    d.line([(x1, y), (x2, y)], fill=colour, width=width)
    d.polygon([(x2 + 16, y - 10), (x2 + 16, y + 10), (x2, y)], fill=colour)


def arrow_diag_up(d, x1, y1, x2, y2, colour, width=3):
    """Arrow with the head at (x2, y2), pointing upwards along any slope."""
    d.line([(x1, y1), (x2, y2)], fill=colour, width=width)
    d.polygon([(x2 - 10, y2 + 16), (x2 + 10, y2 + 16), (x2, y2)], fill=colour)


def kind_diagram(scene, img, d):
    draw_title(d, scene["title"])

    # Down the left is the version with the ids in a field, and the two ways it
    # loses. The viewer has to have watched both before the right-hand column
    # reads as anything other than extra machinery.
    box(d, 70, 232, 560, 120, "NaiveNotificationConsumer",
        "«a HashSet of ids»   remembered in a field", MUTED,
        label_size=28, sub_size=24)

    arrow(d, 200, 356, 200, 430, RED, 5)
    d.text((250, 366), "a deploy empties the set",
           font=f(MONO_B, 26), fill=RED, anchor="la")
    d.text((250, 398), "and a crash can land between the work and the record",
           font=f(SANS, 21), fill=MUTED, anchor="la")

    box(d, 70, 434, 560, 130, "two identical emails",
        "one order, and nothing threw", AMBER,
        label_size=30, sub_size=22)

    d.text((80, 590), "the database survived the deploy",
           font=f(SANS_B, 26), fill=RED, anchor="la")
    d.text((80, 622), "the HashSet did not",
           font=f(SANS, 22), fill=MUTED, anchor="la")

    box(d, 70, 680, 560, 110, "CallLog",
        "the timeline, and the evidence  ·  SimulatedClock", MUTED,
        label_size=28, sub_size=22)

    d.text((1465, 372), "the record of handling it goes in the same commit",
           font=f(SANS_B, 26), fill=GREEN, anchor="ma")
    d.text((1465, 408), "and the cheapest answer is not to need a store at all",
           font=f(SANS, 22), fill=MUTED, anchor="ma")

    work = [
        ("IdempotentConsumer → Transaction", "queueConfirmation  ·  recordHandled  ·  commit", GREEN),
        ("NotificationsDatabase", "the effect and the memory, in one place", CYAN),
        ("ShipmentStatusConsumer", "naturally idempotent  ·  no store at all", MUTED),
        ("forgetHandledOlderThan", "ids expire, and the window is a guess", AMBER),
    ]
    d.line([(1084, 500), (1084, 848)], fill=LINE, width=3)

    y = 452
    for label, sub, colour in work:
        box(d, 1160, y, 690, 96, label, sub, colour,
            label_size=27, sub_size=22)
        arrow_left(d, 1154, y + 48, 1088, colour, 3)
        y += 116

    d.text((W // 2, 960),
           "Ask whether the handler can be rewritten  "
           "before reaching for a dedupe table.",
           font=f(SANS_B, 28), fill=AMBER, anchor="ma")


AUTHOR = "Jayasekhar Konduru"
POSTER_TOP = (49, 16, 92)
POSTER_BOTTOM = (10, 18, 58)
GOLD = AMBER
RULE = ROSE


def gradient(img, top, bottom):
    """A vertical wash, used by the poster and the sign-off card."""
    g = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        g.line([(0, y), (W, y)],
               fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))


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
    # The verdict shrinks to fit too. These lines are longer here than on the
    # other posters, and a note that touches the border reads as clipped.
    note_fnt = f(SANS_B, 34)
    while note_fnt.getlength(note) > w - 60 and note_fnt.size > 20:
        note_fnt = f(SANS_B, note_fnt.size - 1)
    d.text((x + w // 2, y + h - 58), note, font=note_fnt, fill=colour,
           anchor="ma")


def name_pill(d, x, y):
    """The author's name in a box, sized to the text. x=None centres it."""
    text = "by " + AUTHOR
    fnt = f(SANS_B, 54)
    w = int(fnt.getlength(text)) + 96
    if x is None:
        x = (W - w) // 2
    d.rounded_rectangle([x, y, x + w, y + 104], radius=52,
                        fill=(12, 18, 46), outline=CLIENT, width=4)
    d.text((x + w // 2, y + 22), text, font=fnt, fill=CLIENT, anchor="ma")


def kind_poster(scene, img, d):
    """Title card and YouTube thumbnail in one."""
    gradient(img, POSTER_TOP, POSTER_BOTTOM)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=GOLD)
    d.text((110, 88), "DESIGN PATTERNS  -  JAVA", font=f(SANS_B, 36), fill=GOLD)

    # "IDEMPOTENT" is a word most viewers have read and never had explained, so
    # it gets the thumbnail-sized type and the accent line underneath says what
    # it means in five ordinary words.
    d.text((110, 152), "IDEMPOTENT", font=f(SANS_B, 140), fill=TEXT)
    d.text((110, 332), "HANDLE IT TWICE, SAFELY", font=f(SANS_B, 64), fill=ACCENT)

    d.rectangle([110, 462, 620, 472], fill=RULE)

    d.rounded_rectangle([110, 516, W - 110, 866], radius=26,
                        outline=ACCENT, width=4)

    # Both sets of numbers come out of the demo: acts two and three, then act four.
    pill(d, 150, 556, 700, 170, RED, 'a set of ids in memory',
         "2 emails  ·  1 order  ·  and the test was green", tag="BEFORE")
    pill(d, 1070, 556, 700, 170, GREEN, 'the id, in the same commit',
         "1 email  ·  1 order  ·  restart it, crash it", tag="AFTER")

    arrow_y = 636
    d.line([(880, arrow_y), (1010, arrow_y)], fill=TEXT, width=8)
    d.polygon([(1010, arrow_y - 22), (1010, arrow_y + 22), (1052, arrow_y)],
              fill=TEXT)

    d.text((W // 2, 750), "The broker will send it twice. It is the receiver that decides what that means.",
           font=f(SANS_B, 34), fill=TEXT, anchor="ma")
    d.text((W // 2, 800), "Exactly once, out of at least once.",
           font=f(SANS_B, 46), fill=GOLD, anchor="ma")

    name_pill(d, 110, 896)


def kind_outro(scene, img, d):
    """The sign-off card: like, subscribe, and who made it."""
    gradient(img, POSTER_BOTTOM, POSTER_TOP)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=GOLD)

    d.text((W // 2, 150), scene["title"], font=f(SANS_B, 96), fill=TEXT, anchor="ma")
    d.line([(W // 2 - 240, 290), (W // 2 + 240, 290)], fill=RULE, width=6)

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

    # This card is centred throughout and is never a thumbnail, so the name
    # stays centred here rather than pinned left as it is on the poster.
    name_pill(d, None, 880)


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

#!/usr/bin/env python3
"""Render one 1920x1080 PNG slide per scene for the State pattern video."""

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
    d.text((W - 70, H - 58), "State Pattern  ·  Java 21",
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
    d.rectangle([100, 260, 112, 860], fill=ACCENT)
    y = 290
    for ln in scene["body"]:
        col = TEXT
        fnt = f(SANS, 42)
        if ln.startswith("—"):
            col, fnt = MUTED, f(SANS, 34)
        elif ln.startswith("In plain") or ln.startswith("the subclass") \
                or ln.startswith("It never"):
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


def kind_diagram(scene, img, d):
    draw_title(d, scene["title"])

    # The context, centred: it holds one state and forwards to it.
    d.text((880, 232), "CONTEXT", font=f(SANS_B, 24), fill=ACCENT, anchor="ma")
    box(d, 560, 270, 640, 110, "Order",
        "holds one OrderState, forwards every request", ACCENT)

    # The client, left: asks the order to do things, and is told no.
    d.text((280, 232), "CLIENT", font=f(SANS_B, 24), fill=CLIENT, anchor="ma")
    box(d, 80, 270, 400, 110, "OrderStateDemo", "order.cancel(reason)", CLIENT)
    arrow_right(d, 484, 325, 554, CLIENT, 4)

    # The evidence, right: where a wrong answer shows up as money.
    d.text((1560, 232), "EVIDENCE", font=f(SANS_B, 24), fill=GREEN, anchor="ma")
    box(d, 1280, 270, 560, 110, "Ledger + history",
        "every move and every refusal is recorded", GREEN)
    arrow_right(d, 1206, 325, 1276, GREEN, 3)

    # The interface. Every request has a body, and every body throws -- so a
    # state lists what it allows, and the rest refuse on their own.
    box(d, 460, 425, 1000, 100, "OrderState",
        "«interface»   six requests, and every default throws", ROSE,
        label_size=28, sub_size=22)
    arrow(d, 960, 385, 960, 421, ACCENT, 3)

    # A rail gathering the seven states, with one arrow up at the interface.
    d.line([(192, 600), (1728, 600)], fill=LINE, width=3)
    arrow_up(d, 960, 600, 531, LINE, 3)

    states = [
        ("PLACED", "[pay, cancel]", CYAN),
        ("PAID", "[pack, cancel]", CYAN),
        ("PACKED", "[ship, cancel]", CYAN),
        ("SHIPPED", "[deliver]", CYAN),
        ("DELIVERED", "[refund]", CYAN),
        ("CANCELLED", "«terminal»  []", MUTED),
        ("REFUNDED", "«terminal»  []", MUTED),
    ]
    sw, gap, sx = 240, 16, 72
    for i, (label, sub, colour) in enumerate(states):
        x = sx + i * (sw + gap)
        box(d, x, 660, sw, 120, label, sub, colour, label_size=26, sub_size=20)
        d.line([(x + sw // 2, 660), (x + sw // 2, 600)], fill=LINE, width=3)

    d.text((W // 2, 812),
           "Seven states. Each lists what it allows; everything else refuses.",
           font=f(SANS_B, 34), fill=TEXT, anchor="ma")
    d.text((W // 2, 862),
           "Order has no if that mentions a status. It forwards, and the state answers.",
           font=f(SANS, 28), fill=MUTED, anchor="ma")

    # The rejected alternative, kept on screen so the contrast is explicit.
    box(d, 620, 900, 680, 100, "NaiveOrder",
        "«the trap»  one enum, and six chains that disagree", AMBER)


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
    d.text((x + w // 2, y + h - 58), note, font=f(SANS_B, 34), fill=colour,
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

    d.text((110, 156), "THE STATE", font=f(SANS_B, 128), fill=TEXT)
    d.text((110, 296), "PATTERN", font=f(SANS_B, 128), fill=ACCENT)

    d.rectangle([110, 462, 620, 472], fill=RULE)

    # One box around the whole idea - the two call sites and the sentence that
    # explains them - so the tagline reads as part of the pattern rather than
    # as a caption floating under it.
    d.rounded_rectangle([110, 516, W - 110, 842], radius=26,
                        outline=ACCENT, width=4)

    # A rule copied into six methods vs. a rule that has somewhere to live.
    pill(d, 150, 556, 700, 170, RED, "if (status == ...)",
         "one rule, copied into six methods", tag="BEFORE")
    pill(d, 1070, 556, 700, 170, GREEN, "state.cancel(order)",
         "one class per state, and it decides", tag="AFTER")

    arrow_y = 636
    d.line([(880, arrow_y), (1010, arrow_y)], fill=TEXT, width=8)
    d.polygon([(1010, arrow_y - 22), (1010, arrow_y + 22), (1052, arrow_y)],
              fill=TEXT)

    d.text((W // 2, 758), "Stop checking the status. Give it a type.",
           font=f(SANS_B, 52), fill=TEXT, anchor="ma")

    # Bottom left, on the same edge as the eyebrow, the title and the rule, and
    # clear of YouTube's own furniture: the duration badge sits bottom right and
    # the watched-progress bar covers the last forty pixels of the height.
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

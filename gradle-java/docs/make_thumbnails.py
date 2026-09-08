#!/usr/bin/env python3
"""Render `docs/thumbnail.png` for every pattern project.

Why this exists separately from `video/poster.png`: the poster is the
video's opening frame, so it is composed for a screen and carries the
before/after comparison, the arrow and the author credit. A thumbnail is
judged at about 360 pixels wide in a search result, and at that size the
comparison is a smudge. This renders a purpose-built 1280x720 image with
the same palette and branding but only three things on it -- the pattern
name, one line saying what it buys you, and one short piece of code -- each
set large enough to survive the shrink.

Both images stay in the repository. Upload this one as the thumbnail; the
poster remains what a viewer sees when the video starts.

Usage:
    python3 docs/make_thumbnails.py            # all projects
    python3 docs/make_thumbnails.py proxy      # one project
"""

import os
import sys

import matplotlib
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H = 1280, 720  # YouTube's recommended thumbnail size, 16:9

TEXT = (226, 232, 240)
ACCENT = (167, 139, 250)
GREEN = (52, 211, 153)
GOLD = (251, 191, 36)
CYAN = (56, 189, 248)
TOP = (49, 16, 92)
BOTTOM = (10, 18, 58)
CODE_BG = (12, 18, 46)

FONT_DIR = os.path.join(os.path.dirname(matplotlib.__file__),
                        "mpl-data", "fonts", "ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

AUTHOR = "Jayasekhar Konduru"

# Per project: the name split across lines, the promise, and one short piece
# of code. The code is deliberately the *after* form only -- a thumbnail has
# no room to argue, so it shows the destination rather than the contrast.
# Everything here is kept short on purpose; anything longer stops being
# readable once YouTube scales the image down.
META = {
    "simple-factory": (["SIMPLE", "FACTORY"], "Let data choose the class",
                       "Factory.create(type)"),
    "static-factory": (["STATIC", "FACTORY"], "Give the constructor a name",
                       "Discount.percentage(10)"),
    "factory-method": (["FACTORY", "METHOD"], "One step, left to the subclass",
                       "createCourier()"),
    "abstract-factory": (["ABSTRACT", "FACTORY"],
                         "Choose the whole family at once",
                         "factory.taxRule()"),
    "builder": (["BUILDER"], "Decide it a piece at a time",
                ".addItem(x).build()"),
    "prototype": (["PROTOTYPE"], "Copy the one you already have",
                  "master.copy()"),
    "singleton": (["SINGLETON"], "Exactly one, actually enforced",
                  "enum INSTANCE"),
    "adapter": (["ADAPTER"], "One class translates, not every caller",
                "provider.quoteRate(...)"),
    "bridge": (["BRIDGE"], "Two hierarchies, varying independently",
               "new Notification(channel)"),
    "composite": (["COMPOSITE"], "One tree, one interface, zero instanceof",
                  "child.totalPrice()"),
    "decorator": (["DECORATOR"], "Wrap it, don't subclass it",
                  "new Insurance(gift)"),
    "facade": (["FACADE"], "One door in front of many",
               "facade.placeOrder(r)"),
    "flyweight": (["FLYWEIGHT"], "Stop paying for the same data twice",
                  "styleFor(SALE)"),
    "proxy": (["PROXY"], "Same interface, it controls the door",
              "new LazyProductImage(sku)"),
    "strategy": (["STRATEGY"], "Swap the rule, not the code",
                 "rule.costFor(shipment)"),
    "observer": (['OBSERVER'], "Tell everyone, know no one",
             "order.addListener(x)"),
    "command": (['COMMAND'], "Make the action an object",
            "history.undo()"),
    "template-method": (['TEMPLATE', 'METHOD'], "Fix the steps, vary the how",
                    "fulfil(order)"),
    "state": (['STATE'], "Behaviour follows the state",
          "order.cancel()"),
    "chain-of-responsibility": (['CHAIN OF', 'RESPONSIBILITY'], "Each link answers or passes it on",
                            "next.screen(request)"),
    "iterator": (['ITERATOR'], "Hide how the walk really works",
             "for (Product p : results)"),
    "mediator": (['MEDIATOR'], "Components talk through one hub",
             "hub.changed(field)"),
    "memento": (['MEMENTO'], "Snapshot it, restore it, safely",
            "cart.restore(saved)"),
    "visitor": (['VISITOR'], "New reports, untouched model",
            "node.accept(report)"),
    "interpreter": (['INTERPRETER'], "Turn a rule into a tree",
                "rule.matches(cart)"),
}

GROUP = {
    "simple-factory": "creational", "static-factory": "creational",
    "factory-method": "creational", "abstract-factory": "creational",
    "builder": "creational", "prototype": "creational",
    "singleton": "creational",
    "adapter": "structural", "bridge": "structural",
    "composite": "structural", "decorator": "structural",
    "facade": "structural", "flyweight": "structural", "proxy": "structural",
    "strategy": "behavioural",
    "observer": "behavioural",
    "command": "behavioural",
    "template-method": "behavioural",
    "state": "behavioural",
    "chain-of-responsibility": "behavioural",
    "iterator": "behavioural",
    "mediator": "behavioural",
    "memento": "behavioural",
    "visitor": "behavioural",
    "interpreter": "behavioural",
}


def f(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, max_width, start):
    """Largest font size at which `text` still fits `max_width`."""
    size = start
    while size > 12 and f(path, size).getlength(text) > max_width:
        size -= 2
    return f(path, size)


def gradient(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)))


def render(slug):
    names, promise, code = META[slug]
    img = Image.new("RGB", (W, H), BOTTOM)
    gradient(img)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 10], fill=GOLD)

    d.text((64, 46), "JAVA  ·  DESIGN PATTERNS", font=f(SANS_B, 26), fill=GOLD)

    # The name is the one thing that has to be legible at any size, so it is
    # grown until the widest of its lines fills the frame. A one-word name
    # like PROXY therefore ends up far bigger than a two-line one, which is
    # the point -- the space is there, and dead space below the text is what
    # makes a thumbnail look unfinished.
    pattern_font = f(SANS_B, 64)
    promise_font = fit(SANS_B, promise, W - 128, 44)
    code_font = fit(MONO_B, code, W - 200, 38)

    # Everything below the name has a known height, so the name gets what is
    # left. Fitting it to the frame width alone is not enough -- a two-line
    # name sized to the width would run off the bottom and collide with the
    # author credit -- so it is capped by the vertical budget as well.
    below = (pattern_font.size + 24 + 8 + 40
             + promise_font.size + 26 + code_font.size + 34)
    per_line = (H - 110 - 130 - below) // len(names) - 6
    widest = max(names, key=len)
    name_font = f(SANS_B, min(fit(SANS_B, widest, W - 128, 190).size,
                              per_line))

    block_h = len(names) * (name_font.size + 6) + below
    y = max(110, (H - block_h) // 2 + 20)

    for line in names:
        d.text((64, y), line, font=name_font, fill=TEXT)
        y += name_font.size + 6
    d.text((64, y), "PATTERN", font=pattern_font, fill=ACCENT)
    y += pattern_font.size + 24

    d.rectangle([64, y, 260, y + 8], fill=GREEN)
    y += 40

    d.text((64, y), promise, font=promise_font, fill=TEXT)
    y += promise_font.size + 26

    box_w = int(code_font.getlength(code)) + 56
    d.rounded_rectangle([64, y, 64 + box_w, y + code_font.size + 34],
                        radius=14, fill=CODE_BG, outline=GREEN, width=4)
    d.text((92, y + 14), code, font=code_font, fill=GREEN)

    # Author credit, bottom right, out of the way of the name.
    af = f(SANS_B, 28)
    aw = int(af.getlength(AUTHOR)) + 44
    d.rounded_rectangle([W - 64 - aw, H - 86, W - 64, H - 32],
                        radius=27, outline=CYAN, width=3)
    d.text((W - 64 - aw // 2, H - 74), AUTHOR, font=af, fill=CYAN, anchor="ma")

    out = os.path.join(ROOT, GROUP[slug], slug + "-pattern",
                       "docs", "thumbnail.png")
    img.save(out, optimize=True)
    kb = os.path.getsize(out) // 1024
    print("wrote %s  (%dx%d, %d KB)"
          % (os.path.relpath(out, ROOT), W, H, kb))


def main():
    wanted = sys.argv[1:]
    for slug in META:
        if wanted and slug not in wanted:
            continue
        # META covers the whole series, including projects not built yet.
        if not os.path.isdir(os.path.join(ROOT, GROUP[slug],
                                          slug + "-pattern")):
            if wanted:
                print("%s: not built yet - skipped" % slug)
            continue
        render(slug)


if __name__ == "__main__":
    main()

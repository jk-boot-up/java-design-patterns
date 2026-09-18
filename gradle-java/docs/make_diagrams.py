#!/usr/bin/env python3
"""Render the Mermaid diagrams in a project's docs/ to PNG.

Every `docs/*-diagram.md` in this repository follows the same shape: some
prose explaining what the picture says, an `![...](images/<name>.png)` tag,
and then the Mermaid source in a `<details>` block underneath. The PNG is what
a reader sees on GitHub and in the generated HTML; the Mermaid is what the
next person edits.

Keeping those two in step used to be a command pasted out of the category
build spec and run by hand, which is exactly the arrangement that ends with a
diagram whose picture and source disagree. This script is that command, with
the palette and the scale factor written down once.

    python3 docs/make_diagrams.py platform-design-patterns
    python3 docs/make_diagrams.py platform-design-patterns/sidecar-pattern
    python3 docs/make_diagrams.py platform-design-patterns --force

Every Mermaid block in the file is rendered. The first becomes
`docs/images/<name>.png` and the rest are numbered from two —
`<name>-2.png`, `<name>-3.png` — in the order they appear, which is the order
the image tags in the document are expected to use. Most files hold one
diagram; `uml-diagram.md` holds one sequence per act, and every act needs a
picture, because the Mermaid source in a `<details>` block is only rendered by
GitHub and stays source everywhere else.

A PNG that is newer than its Markdown is left alone; `--force` re-renders
everything. Each render starts a headless browser and takes a few seconds, so
that default matters when the argument is a whole category.

Requires the Mermaid CLI. There is no global install: it is fetched through
`npx` on demand, which keeps the repository free of a `node_modules` nobody
asked for. The first run therefore needs a network connection.
"""

import glob
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MERMAID_CLI = "@mermaid-js/mermaid-cli@11"

#: The slide palette, so a diagram dropped into a video frame or an HTML page
#: sits on the same background it was drawn for.
BACKGROUND = "#0f172a"

#: Scale factor. At 1 the text is unreadable on a high-density display and
#: illegible in a video frame; 4 is the smallest that survives both.
SCALE = "4"

CONFIG = {"theme": "dark", "themeVariables": {"fontSize": "16px"}}


def mermaid_blocks(md):
    return re.findall(r'^```mermaid\n(.*?)^```', md, re.S | re.M)


def png_name(stem, index):
    """First diagram keeps the plain name; the rest are numbered from two.

    Numbering from two rather than one keeps every existing image tag, and
    every file name already committed, exactly as it was when a document that
    held one diagram grows a second.
    """
    return stem if index == 0 else "%s-%d" % (stem, index + 1)


def render(source, png, config_file):
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False) as f:
        f.write(source)
        mmd = f.name
    try:
        subprocess.run(
            ["npx", "-y", MERMAID_CLI, "-q",
             "-i", mmd, "-o", png,
             "-b", BACKGROUND, "-s", SCALE, "-c", config_file],
            check=True, stdout=subprocess.DEVNULL)
    finally:
        os.unlink(mmd)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if not args:
        sys.exit(__doc__.strip().split("\n\n")[0] + "\n\n"
                 "  usage: make_diagrams.py <category-or-project> [...] [--force]")

    files = []
    for a in args:
        base = a if os.path.isabs(a) else os.path.join(ROOT, a)
        files += sorted(glob.glob(os.path.join(base, "**", "docs", "*-diagram.md"),
                                  recursive=True))
    if not files:
        sys.exit("no docs/*-diagram.md found under: " + ", ".join(args))

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(CONFIG, f)
        config_file = f.name

    try:
        for md_path in files:
            docs = os.path.dirname(md_path)
            stem = os.path.basename(md_path)[:-3]

            blocks = mermaid_blocks(open(md_path).read())
            if not blocks:
                print("%-72s no mermaid block — skipped"
                      % os.path.relpath(os.path.join(docs, "images",
                                                     stem + ".png"), ROOT))
                continue

            for i, source in enumerate(blocks):
                png = os.path.join(docs, "images", png_name(stem, i) + ".png")
                shown = os.path.relpath(png, ROOT)
                if not force and os.path.exists(png) \
                        and os.path.getmtime(png) >= os.path.getmtime(md_path):
                    print("%-72s up to date" % shown)
                    continue

                os.makedirs(os.path.dirname(png), exist_ok=True)
                render(source, png, config_file)
                print("%-72s %d KB" % (shown, os.path.getsize(png) // 1024))
    finally:
        os.unlink(config_file)


if __name__ == "__main__":
    main()

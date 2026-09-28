#!/usr/bin/env python3
"""Take the Mermaid source out of every docs/*-diagram.md.

The diagrams in this repository are image files: `docs/images/<name>.png`
(and `<name>-2.png`, `-3.png`, ... for a document with several). Earlier
documents also carried the Mermaid source in a collapsed `<details>` block;
the repository no longer uses Mermaid, so this removes those blocks and makes
sure every diagram is shown as an image instead.

    python3 docs/strip_mermaid.py                 every category
    python3 docs/strip_mermaid.py structural      one category or project

For each Mermaid block, in order: if the document already shows the image it
was rendered to, the block (and its now-empty <details> wrapper) is deleted;
otherwise the block is replaced by an image tag for that file. A block whose
image does not exist is left alone and reported, so nothing is lost silently.
Run docs/make_diagrams.py first if anything is reported.
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r'^```mermaid\n.*?^```[ \t]*\n?', re.S | re.M)
EMPTY_DETAILS = re.compile(r'<details>\s*<summary>[^<]*</summary>\s*</details>[ \t]*\n?', re.S)


def image_name(stem, index):
    return stem if index == 0 else "%s-%d" % (stem, index + 1)


def strip(md_path):
    text = open(md_path).read()
    docs = os.path.dirname(md_path)
    stem = os.path.basename(md_path)[:-3]
    title = stem.replace("-", " ").capitalize()
    blocks = list(BLOCK.finditer(text))
    if not blocks:
        return 0, []
    out, pos, kept = [], 0, []
    for i, m in enumerate(blocks):
        name = image_name(stem, i)
        found = next((e for e in (".svg", ".png")
                      if os.path.exists(os.path.join(docs, "images", name + e))), None)
        out.append(text[pos:m.start()])
        pos = m.end()
        if found is None:
            out.append(m.group(0))
            kept.append(name)
        elif not re.search(r'\]\(images/%s\.(?:png|svg)\)' % re.escape(name), text):
            out.append("![%s%s](images/%s%s)\n" % (title, "" if i == 0 else " %d" % (i + 1),
                                                   name, found))
    out.append(text[pos:])
    new = EMPTY_DETAILS.sub("", "".join(out))
    new = re.sub(r'\n{3,}', "\n\n", new)
    if new != text:
        open(md_path, "w").write(new)
    return len(blocks) - len(kept), kept


def main():
    args = sys.argv[1:] or ["."]
    files = []
    for a in args:
        base = a if os.path.isabs(a) else os.path.join(ROOT, a)
        files += glob.glob(os.path.join(base, "**", "docs", "*-diagram.md"), recursive=True)
    removed, missing = 0, []
    for f in sorted(set(files)):
        if "/build/" in f:
            continue
        n, kept = strip(f)
        removed += n
        missing += ["%s -> images/%s" % (os.path.relpath(f, ROOT), k) for k in kept]
    print("%d mermaid blocks replaced by images" % removed)
    for m in missing:
        print("  no image yet: " + m)


if __name__ == "__main__":
    main()

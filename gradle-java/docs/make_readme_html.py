#!/usr/bin/env python3
"""Render a project's README.md as README.html, beside it.

GitHub renders Markdown and a browser does not. A reader who has cloned this
repository, or who is handed a directory rather than a URL, opens README.md in
a text editor and reads the pipes and hashes. The HTML twin exists for that
reader, and for the same reason `docs/spec.html` does: one source, two ways in.

    python3 docs/make_readme_html.py platform-design-patterns
    python3 docs/make_readme_html.py platform-design-patterns/sidecar-pattern

Every README.md found underneath each argument is converted, which includes the
`real/README.md` that a Tier 2 directory carries. Build outputs are skipped.

The Markdown-to-HTML converter is the one in `make_specs.py`, imported rather
than copied. That is deliberate: the two kinds of page then look identical,
inherit the same stylesheet, and a construct that renders correctly in a spec
renders correctly in a README. If a README grows a construct the converter does
not know, extend the converter rather than working around it here — it is a
small, readable function and it is the only Markdown implementation in the
repository.

**README.html is generated. Never edit it.** Edit README.md and run this.
"""

import html
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

#: Directories not to walk into. `build` and `.gradle` are output rather than
#: documents. `video` is skipped for a different reason: its README is a
#: maintainer's note about rendering a film, addressed to whoever next runs the
#: pipeline, and giving it a styled HTML twin would imply it is for readers.
SKIP = {"build", ".gradle", "node_modules", ".git", "video"}


def _make_specs():
    spec = importlib.util.spec_from_file_location(
        "make_specs", os.path.join(HERE, "make_specs.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MS = _make_specs()


def wrap(title, body, source):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
<main>
%s
</main>
<footer>
Generated from <code>%s</code> by <code>docs/make_readme_html.py</code> &mdash;
edit the Markdown, not this file.
</footer>
</body>
</html>
""" % (html.escape(title), MS.CSS, body, html.escape(source))


def readmes(base):
    found = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        if "README.md" in filenames:
            found.append(os.path.join(dirpath, "README.md"))
    return sorted(found)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: make_readme_html.py <category-or-project> [...]")

    paths = []
    for a in args:
        base = a if os.path.isabs(a) else os.path.join(ROOT, a)
        paths += readmes(base)
    if not paths:
        sys.exit("no README.md found under: " + ", ".join(args))

    # Register every page this run will produce before converting any of it.
    # A category README links to the project READMEs underneath it, and those
    # link back; without this, whichever page is written first would keep its
    # links pointing at Markdown because the twin did not exist yet.
    MS.PLANNED.update(p[:-3] + ".html" for p in paths)

    for md_path in paths:
        md = open(md_path).read()
        heading = re.search(r'^# (.+)', md, re.M)
        title = heading.group(1) if heading else os.path.basename(
            os.path.dirname(md_path))
        out = md_path[:-3] + ".html"
        MS.LINK_BASE = os.path.dirname(md_path)
        open(out, "w").write(wrap(title, MS.to_html(md), "README.md"))
        print("%-68s %d KB" % (os.path.relpath(out, ROOT),
                               os.path.getsize(out) // 1024))


if __name__ == "__main__":
    main()

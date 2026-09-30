#!/usr/bin/env python3
"""Render every Markdown file under a project or category as a themed HTML twin, beside it.

GitHub renders Markdown and a browser does not. A reader who has cloned this
repository, or who is handed a directory rather than a URL, opens README.md in
a text editor and reads the pipes and hashes. The HTML twin exists for that
reader, and for the same reason `docs/spec.html` does: one source, two ways in.

    python3 docs/make_readme_html.py platform-design-patterns
    python3 docs/make_readme_html.py platform-design-patterns/sidecar-pattern

Every .md found underneath each argument is converted (README, docs, YouTube
documents, diagrams, the `real/` directory of a Tier 2 project, video notes):
the rule is that every Markdown file has an HTML twin. Build outputs are
skipped. Each page offers Light, Dim and Dark themes; it follows the system
setting until the reader picks one, and remembers the choice.

The Markdown-to-HTML converter is the one in `make_specs.py`, imported rather
than copied. That is deliberate: the two kinds of page then look identical,
inherit the same stylesheet, and a construct that renders correctly in a spec
renders correctly in a README. If a README grows a construct the converter does
not know, extend the converter rather than working around it here — it is a
small, readable function and it is the only Markdown implementation in the
repository.

**The .html files are generated. Never edit them.** Edit the Markdown and run this.
"""

import html
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

#: Directories not to walk into: output and tool caches rather than documents.
SKIP = {"build", ".gradle", "node_modules", ".git", "__pycache__", "target"}


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
%s
</head>
<body>
%s
<main>
%s
</main>
<footer>
Generated from <code>%s</code> by <code>docs/make_readme_html.py</code> &mdash;
edit the Markdown, not this file.
</footer>
</body>
</html>
""" % (html.escape(title), MS.CSS, MS.THEME_HEAD, MS.THEME_BAR, body, html.escape(source))


def markdown_files(base):
    if os.path.isfile(base):
        return [base] if base.endswith(".md") else []
    found = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        found += [os.path.join(dirpath, f) for f in filenames if f.endswith(".md")]
    return sorted(found)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: make_readme_html.py <category-or-project> [...]")

    paths = []
    for a in args:
        base = a if os.path.isabs(a) else os.path.join(ROOT, a)
        paths += markdown_files(base)
    if not paths:
        sys.exit("no .md found under: " + ", ".join(args))

    # Register every page this run will produce before converting any of it.
    # A category README links to the project READMEs underneath it, and those
    # link back; without this, whichever page is written first would keep its
    # links pointing at Markdown because the twin did not exist yet.
    MS.PLANNED.update(os.path.normpath(p[:-3] + ".html") for p in paths)

    for md_path in paths:
        md = open(md_path).read()
        heading = re.search(r'^# (.+)', md, re.M)
        title = heading.group(1) if heading else os.path.basename(
            os.path.dirname(md_path))
        out = md_path[:-3] + ".html"
        MS.LINK_BASE = os.path.dirname(md_path)
        open(out, "w").write(wrap(title, MS.to_html(md), os.path.basename(md_path)))
        print("%-68s %d KB" % (os.path.relpath(out, ROOT),
                               os.path.getsize(out) // 1024))


if __name__ == "__main__":
    main()

"""Register projects that describe themselves in a pattern.toml.

Older projects are listed by hand in the tables of make_specs.py,
make_youtube_docs.py and make_thumbnails.py. A project made with
tools/patternkit instead carries a `pattern.toml` at its root, and each
generator calls one function here to add it to its tables, so a new project
needs no edits to any generator.
"""

import glob
import os
import tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def projects():
    """(category, slug, parsed pattern.toml) for every self-describing project."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*", "*-pattern", "pattern.toml"))):
        data = tomllib.loads(open(path).read())
        p = data["project"]
        out.append((p["category"], p["slug"], data))
    return out


def _order(order):
    have = {s for _, s in order}
    for cat, slug, _ in projects():
        if slug not in have:
            order.append((cat, slug))


def register_specs(order, names, meta):
    _order(order)
    for _, slug, d in projects():
        names.setdefault(slug, d["project"]["title"])
        s = d["spec"]
        meta.setdefault(slug, dict(
            purpose="\n" + s["purpose"].strip() + "\n",
            nongoals=list(s["nongoals"]),
            problem="\n" + s["problem"].strip() + "\n",
            roles=[tuple(r) for r in s["roles"]],
            requirements=list(s["requirements"]),
        ))


def register_youtube(order, meta):
    _order(order)
    for _, slug, d in projects():
        p = d["project"]
        meta.setdefault(slug, {"title": p.get("youtube_title", p["title"]),
                               "tags": list(p.get("youtube_tags", []))})


def register_thumbnails(meta, group):
    for cat, slug, d in projects():
        p = d["project"]
        meta.setdefault(slug, (list(p["thumb_lines"]), p["tagline"], p["thumb_code"]))
        group.setdefault(slug, cat)

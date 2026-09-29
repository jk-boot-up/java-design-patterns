#!/usr/bin/env python3
"""Write the repository's front door and coverage list from what exists on disk.

    python3 gradle-java/docs/make_index.py

Produces, at the repository root:
  index.md / index.html         every project, grouped by category, with links
  docs/design-patterns-catalog.md
                                the patterns this course means to cover, marked
                                covered, planned (being built) or pending

A project is any gradle-java/<category>/<slug>-pattern/ with a README.md.
Framework or infrastructure versions (slugs that extend a plain one, such as
retry-with-resilience4j) are listed under their plain-Java project. Never edit
the outputs by hand: add a project, then re-run this.
"""

import html
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
GRADLE = os.path.dirname(HERE)
REPO = os.path.dirname(GRADLE)

spec = importlib.util.spec_from_file_location("pattern_catalog", os.path.join(HERE, "pattern_catalog.py"))
CAT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CAT)


def taglines():
    """Short one-liners from the thumbnail table, e.g. "Never wait forever"."""
    src = open(os.path.join(HERE, "make_thumbnails.py")).read()
    return dict(re.findall(r'^    "([a-z0-9-]+)": \(\[[^\]]*\],\s*\n?\s*[\'"](.+?)[\'"],', src, re.M))


def readme_summary(text):
    """The first prose paragraph of a README, as plain text, one sentence."""
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if not p or p[0] in "#|-*>!<" or p.startswith("```"):
            continue
        p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
        p = re.sub(r"[*_`]", "", " ".join(p.split()))
        m = re.match(r"(.+?[.!?])(\s|$)", p)
        return (m.group(1) if m else p)[:160]
    return ""


def pattern_toml_tagline(path):
    f = os.path.join(path, "pattern.toml")
    if os.path.exists(f):
        import tomllib
        return tomllib.loads(open(f).read()).get("project", {}).get("tagline", "")
    return ""


def projects():
    """{category: [(slug, title, summary, dir)]} for every project on disk."""
    tags, found = taglines(), {}
    for cat in sorted(os.listdir(GRADLE)):
        cdir = os.path.join(GRADLE, cat)
        if not os.path.isdir(cdir) or cat == "docs":
            continue
        for name in sorted(os.listdir(cdir)):
            pdir = os.path.join(cdir, name)
            readme = os.path.join(pdir, "README.md")
            if not name.endswith("-pattern") or not os.path.exists(readme):
                continue
            slug = name[:-len("-pattern")]
            text = open(readme).read()
            h1 = re.search(r"^# (.+)$", text, re.M)
            title = re.sub(r"\s+Pattern$", "", h1.group(1)).strip() if h1 else slug
            summary = pattern_toml_tagline(pdir) or tags.get(slug) or readme_summary(text)
            found.setdefault(cat, []).append((slug, title, summary, pdir))
    return found


def base_of(slug, plain):
    """The plain-Java project a framework version belongs to, or None."""
    cands = [p for p in plain if slug != p and slug.startswith(p + "-")]
    return max(cands, key=len) if cands else None


def anchor(title):
    """The id GitHub gives a heading: lower case, spaces to hyphens, punctuation dropped."""
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def rel(path):
    return os.path.relpath(path, REPO)


def links(pdir, html_page):
    out = []
    for label, md, htm in (("README", "README.md", "README.html"),
                           ("animation", "docs/animation.html", "docs/animation.html"),
                           ("spec", "docs/spec.md", "docs/spec.html")):
        target = htm if html_page else md
        if os.path.exists(os.path.join(pdir, target)):
            out.append("[%s](%s)" % (label, rel(os.path.join(pdir, target))))
    return " · ".join(out)


def status(found):
    """{category: (planned names, pending names)} and overall counts, from the catalogue."""
    have = {s for rows in found.values() for s, *_ in rows}
    per, counts = {}, {"covered": 0, "planned": 0, "pending": 0}
    for cat, _, _, items in CAT.CATEGORIES:
        planned = [n for s, n in items if s not in have and s in CAT.PLANNED]
        pending = [n for s, n in items if s not in have and s not in CAT.PLANNED]
        counts["covered"] += sum(1 for s, _ in items if s in have)
        counts["planned"] += len(planned)
        counts["pending"] += len(pending)
        per[cat] = (planned, pending)
    return per, counts


def index_markdown(found, html_page=False):
    order = [c[0] for c in CAT.CATEGORIES]
    cats = sorted(found, key=lambda c: order.index(c) if c in order else len(order))
    names = {c[0]: (c[1], c[2]) for c in CAT.CATEGORIES}
    total = sum(len(v) for v in found.values())
    out = ["# Design Patterns in Java — Index", "",
           "Every project in this repository: %d projects in %d categories. Each is a "
           "self-contained Gradle Java project with runnable code, tests, written notes, "
           "diagrams, an animated walkthrough and a narrated video, taught through one "
           "online store. Framework and real-infrastructure versions are listed under "
           "the plain-Java project they build on." % (total, len(cats)), "",
           "What is covered and what is still to come: "
           "[docs/design-patterns-catalog.md](docs/design-patterns-catalog.md).", "",
           "Generated by `gradle-java/docs/make_index.py` — do not edit by hand.", ""]
    per, counts = status(found)
    out += ["## Status", "",
            "| ✅ Covered | 🔨 Being built | ⏳ Still to come | Total in the catalogue |",
            "| ---: | ---: | ---: | ---: |",
            "| %d | %d | %d | %d |" % (counts["covered"], counts["planned"], counts["pending"],
                                       sum(counts.values())), "",
            "Each category below ends with what it is still missing; the full list with "
            "links is in [docs/design-patterns-catalog.md](docs/design-patterns-catalog.md).", "",
            "| Category | Projects | Being built | Still to come |", "| --- | ---: | ---: | ---: |"]
    all_cats = cats + [c for c, *_ in CAT.CATEGORIES if c not in cats]
    for c in all_cats:
        planned, pending = per.get(c, ([], []))
        t = names.get(c, (c,))[0]
        link = "[%s](#%s)" % (t, anchor(t)) if c in found else t
        out.append("| %s | %d | %d | %d |" % (link, len(found.get(c, [])), len(planned), len(pending)))
    for c in cats:
        title, blurb = names.get(c, (c, ""))
        rows = found[c]
        plain = [s for s, *_ in rows if not base_of(s, [r[0] for r in rows])]
        out += ["", "## %s" % title, ""]
        if blurb:
            out += ["*%s.*" % blurb, ""]
        out += ["| Pattern | In one line | Open |", "| --- | --- | --- |"]
        by = {r[0]: r for r in rows}
        for s in plain:
            slug, t, summ, pdir = by[s]
            out.append("| **%s** | %s | %s |" % (t, summ, links(pdir, html_page)))
            for v in sorted(r for r in by if base_of(r, plain) == s):
                _, vt, vs, vdir = by[v]
                out.append("| ↳ %s | %s | %s |" % (vt, vs, links(vdir, html_page)))
        planned, pending = per.get(c, ([], []))
        if planned:
            out += ["", "**🔨 Being built:** " + ", ".join(planned) + "."]
        if pending:
            out += ["", "**⏳ Still to come:** " + ", ".join(pending) + "."]
    for c, title, blurb, items in CAT.CATEGORIES:
        if c in found:
            continue
        planned, pending = per[c]
        out += ["", "## %s" % title, "", "*%s.* No project yet." % blurb, ""]
        if planned:
            out += ["**🔨 Being built:** " + ", ".join(planned) + ".", ""]
        if pending:
            out += ["**⏳ Still to come:** " + ", ".join(pending) + "."]
    return "\n".join(out) + "\n"


def catalog_markdown(found):
    have = {s for rows in found.values() for s, *_ in rows}
    covered = pending = planned = 0
    out = ["# Design Patterns — What Is Covered and What Is Pending", "",
           "The patterns this course means to cover, by category. **✅ Covered** has a "
           "project (framework versions noted); **🔨 Planned** is being built now "
           "([plan](new-patterns-plan.md)); **⏳ Pending** is still to come.", "",
           "Generated by `gradle-java/docs/make_index.py` from "
           "`gradle-java/docs/pattern_catalog.py` and the projects on disk.", ""]
    body = []
    for cat, title, blurb, items in CAT.CATEGORIES:
        rows = found.get(cat, [])
        listed = {s for s, _ in items}
        body += ["", "## %s" % title, "", "*%s.*" % blurb, "",
                 "| Pattern | Status | Project |", "| --- | :---: | --- |"]
        for slug, name in items:
            versions = sorted(s for s, *_ in rows if s.startswith(slug + "-"))
            if slug in have:
                covered += 1
                pdir = next(r[3] for r in rows if r[0] == slug)
                extra = " (+ %s)" % ", ".join(v[len(slug) + 1:] for v in versions) if versions else ""
                body.append("| %s | ✅ Covered | [%s](../%s)%s |" % (name, slug, rel(pdir), extra))
            elif slug in CAT.PLANNED:
                planned += 1
                body.append("| %s | 🔨 Planned | |" % name)
            else:
                pending += 1
                body.append("| %s | ⏳ Pending | |" % name)
        # Projects that exist but are not in the catalogue list are still counted.
        plain = [s for s, *_ in rows if not base_of(s, [r[0] for r in rows])]
        for s in plain:
            if s not in listed:
                covered += 1
                pdir = next(r[3] for r in rows if r[0] == s)
                body.append("| %s | ✅ Covered | [%s](../%s) |" % (s.replace("-", " ").title(), s, rel(pdir)))
    total = covered + planned + pending
    out += ["| Covered | Planned | Pending | Total |", "| ---: | ---: | ---: | ---: |",
            "| %d | %d | %d | %d |" % (covered, planned, pending, total)]
    return "\n".join(out + body) + "\n"


def to_html(md, title):
    spec = importlib.util.spec_from_file_location("make_specs", os.path.join(HERE, "make_specs.py"))
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    ms.LINK_BASE = REPO
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n<main>\n%s\n</main>\n"
            "</body>\n</html>\n" % (html.escape(title), ms.CSS, _ids(ms.to_html(md))))


def _ids(body):
    """Give each heading the same id GitHub would, so #links work in the HTML too."""
    return re.sub(r"<h([23])>(.*?)</h\1>",
                  lambda m: '<h%s id="%s">%s</h%s>' % (m.group(1), anchor(html.unescape(re.sub("<[^>]+>", "", m.group(2)))),
                                                     m.group(2), m.group(1)), body)


def main():
    found = projects()
    open(os.path.join(REPO, "index.md"), "w").write(index_markdown(found))
    open(os.path.join(REPO, "index.html"), "w").write(
        to_html(index_markdown(found, html_page=True), "Design Patterns in Java — Index"))
    os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
    open(os.path.join(REPO, "docs", "design-patterns-catalog.md"), "w").write(catalog_markdown(found))
    n = sum(len(v) for v in found.values())
    print("index.md, index.html: %d projects; docs/design-patterns-catalog.md written" % n)


if __name__ == "__main__":
    main()

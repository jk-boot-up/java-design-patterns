"""Turn a project's pattern.toml into its README, docs, diagrams, animation and scenes.

Every sentence comes from pattern.toml; this module only lays it out, the same
way for every project, so the teaching text is written once and nothing is
copied by hand between files.
"""

import json
import re
import tomllib
from pathlib import Path

from . import diagrams

JUNIT = "5.10.2"
VOICE = "Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice)"


# ------------------------------------------------------------ helpers ----

def load(project_dir):
    return tomllib.loads((Path(project_dir) / "pattern.toml").read_text())


def ul(items):
    return "\n".join("- " + i for i in items)


def ol(items):
    return "\n".join("%d. %s" % (n, i) for n, i in enumerate(items, 1))


def para(text):
    return text.strip() + "\n"


def java_tree(pdir, package):
    """The source layout with each file's one-line purpose, from its Javadoc."""
    src = pdir / "src" / "main" / "java" / "com" / "jk" / "explore" / package
    rows = []
    files = sorted(src.rglob("*.java"), key=lambda f: (len(f.relative_to(src).parts) > 1, str(f.relative_to(src))))
    for f in files:
        m = re.search(r"/\*\*(.*?)\*/", f.read_text(), re.S)
        doc = " ".join(m.group(1).replace("*", " ").split()) if m else ""
        first = re.split(r"(?<=[.!?])\s", doc, maxsplit=1)[0].rstrip(".")
        rows.append((str(f.relative_to(src)), first))
    width = max((len(n) for n, _ in rows), default=10) + 2
    lines = ["src/main/java/com/jk/explore/%s/" % package]
    for i, (n, w) in enumerate(rows):
        lines.append("%s %s%s" % ("└──" if i == len(rows) - 1 else "├──", n.ljust(width), w))
    return "```\n" + "\n".join(lines) + "\n```"


def test_count(pdir):
    tests = list((pdir / "src" / "test").rglob("*.java"))
    n = sum(len(re.findall(r"@(?:Test|ParameterizedTest|RepeatedTest)\b", f.read_text())) for f in tests)
    return n, sorted(f.stem for f in tests)


def gradle_version(pdir):
    props = (pdir / "gradle" / "wrapper" / "gradle-wrapper.properties").read_text()
    m = re.search(r"gradle-([\d.]+)-", props)
    return m.group(1) if m else "wrapper"


# ------------------------------------------------------------- README ----

def readme(d, pdir):
    p, r = d["project"], d["readme"]
    slug, title = p["slug"], p["title"]
    n_tests, test_classes = test_count(pdir)
    acts = d["act"]
    diagram_md = {x["name"]: x for x in d["diagram"]}

    def embed(name, caption):
        return "![%s](docs/images/%s.png)" % (caption, name) if name in diagram_md else ""

    out = ["# %s Pattern" % title, "", java_tree(pdir, p["package"]), "",
           "**%s**" % p["bold"], "", para(r["intro"])]
    if p.get("domain_note"):
        out += ["> **Why this domain:** " + p["domain_note"].strip(), ""]
    out += ["## The idea in everyday terms", "", para(r["analogy"]),
            "## The scenario", "", para(r["scenario"]),
            "## Run", "", *([para(r["run_note"])] if r.get("run_note") else []),
            "```bash", "./gradlew run", "```", "",
            "The demo tells the story in %d acts, each printing exact numbers that the tests check:" % len(acts), "",
            "| Act | What it shows |", "| --- | --- |"]
    out += ["| %d. %s | %s |" % (i, a["title"], a["summary"]) for i, a in enumerate(acts, 1)]
    out += ["", "## Test", "", "```bash", "./gradlew test", "```", "",
            ("%d tests in %s. " % (n_tests, ", ".join("`%s`" % c for c in test_classes)))
            + " ".join(r.get("test_note", "Every number the demo prints is asserted, and nothing depends on the "
                                          "clock, so every run gives the same result.").split()), "",
            *(["## What the simulation got right, and what it left out", "", para(r["twin"])] if r.get("twin") else []),
            "## Technologies and versions", "",
            "| Technology | Version | Used for |", "| --- | --- | --- |",
            "| Java | 21 | the code (toolchain set in `build.gradle`) |",
            "| Gradle | %s (wrapper) | build and run, nothing to install |" % gradle_version(pdir),
            "| JUnit | %s | the tests |" % JUNIT]
    for t in r.get("technologies", []):
        out.append("| %s | %s | %s |" % tuple(t))
    out += ["| videokit | repository tool | the narrated video and animation: %s |" % VOICE, "",
            "## Learning Material", "",
            "| Document | What it is for |", "| --- | --- |",
            *(["| [Dependencies](docs/dependencies.md) | what the framework and infrastructure are, and why they are here |"]
              if "dependencies" in d.get("docs", {}) else []),
            "| [Problem statement](docs/problem-statement.md) | the situation and what the project must show |",
            "| [Prerequisites](docs/prerequisites.md) | what you need to know first |",
            "| [%s, explained](docs/%s-pattern-explained.md) | the acts in prose |" % (title, slug),
            "| [Session guide](docs/session.md) | a one-hour lesson with exercises |",
            "| [Animated walkthrough](docs/animation.html) | the acts step by step, narrated |",
            "| [Spec](docs/spec.md) | what this project must be true of |", ""]
    for name, heading in (("architecture-diagram", "The pattern in one picture"),
                          ("class-diagram", "Where each piece sits"),
                          ("data-flow-diagram", "How the data moves"),
                          ("sequence-diagram", "Who calls whom, in order")):
        if name in diagram_md:
            out += ["### " + heading, "", diagram_md[name].get("caption", "").strip(), "",
                    embed(name, diagram_md[name]["title"]), ""]
    out += ["### Video", "",
            "`video/%s-pattern-explained.mp4` (with `.m4a` audio and `.srt` subtitles) is built by "
            "`video/build_video.sh`. Rendered media is not committed." % slug, "",
            "## What it costs", "", ul(r["costs"]), "",
            "## When this is too much", "", para(r["too_much"]),
            "## Where you have already met this", "", ul(r["met_before"]), "",
            "## Where this sits", "", para(r.get("where", "This project is in [%s](..)." % p["category"]))]
    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------- docs ----

def problem(d):
    p, x = d["project"], d["docs"]["problem"]
    return "\n".join(["# Problem Statement", "", "## The scenario", "", para(x["scenario"]),
                      "## The naive version", "", para(x["naive"]),
                      "## What this project must deliver", "", ul(x["deliver"]), ""])


def prerequisites(d):
    x = d["docs"]["prerequisites"]
    return "\n".join(["# Prerequisites", "", "## Required", "", ul(x["required"]), "",
                      "## Explicitly not required", "", ul(x["not_required"]), "",
                      "## What you will need", "",
                      "- A Java 21 JDK. The Gradle wrapper downloads everything else.",
                      *(["- " + n for n in x.get("install", [])]),
                      "- About an hour for the session guide.", ""])


def session(d):
    p, x, acts = d["project"], d["docs"]["session"], d["act"]
    per = max(5, 35 // max(1, len(acts)))
    times = ["| 0:00 | The problem and the analogy | 10 min |"]
    t = 10
    for i, a in enumerate(acts, 1):
        times.append("| 0:%02d | Act %d: %s | %d min |" % (t, i, a["title"], per))
        t += per
    times.append("| 0:%02d | Exercises | %d min |" % (t, max(10, 60 - t)))
    return "\n".join(["# Session Guide — %s Pattern" % p["title"], "", "## Learning Objectives", "",
                      "By the end of the session you can:", "", ul(x["objectives"]), "",
                      "## Timetable", "", "| Start | Topic | Time |", "| --- | --- | --- |", *times, "",
                      "## Walkthrough", "", para(x["walkthrough"]),
                      "## Exercises", "", ol(x["exercises"]), ""])


def explained(d):
    p, x, acts = d["project"], d["docs"]["explained"], d["act"]
    out = ["# %s, Explained" % p["title"], "", "## The pattern in one sentence", "", para(x["sentence"]),
           "## The %d acts" % len(acts), ""]
    for i, a in enumerate(acts, 1):
        out += ["### %d. %s" % (i, a["title"]), "", para(a["detail"])]
    out += ["## The verdict", "", para(x["verdict"]),
            "## How to recognise this in code you did not write", "", ul(x["recognise"]), "",
            "## Where you have already met this", "", ul(d["readme"]["met_before"]), ""]
    return "\n".join(out)


def dependencies(d):
    """docs/dependencies.md, for framework and infrastructure versions of a pattern."""
    x = d["docs"]["dependencies"]
    out = ["# Dependencies", "", para(x["intro"])]
    for name, text in x["what"]:
        out += ["## What %s is" % name, "", para(text)]
    out += ["## Why this project uses them", "", para(x["why"]),
            "## What to install", "", para(x.get("install_note", "Only a JDK, version 21, and a running Docker. "
                                               "Gradle downloads the rest, and the versions are pinned:")),
            "| Tool | Version |", "| --- | --- |"]
    out += ["| %s | %s |" % tuple(v) for v in x["versions"]]
    out += ["", "## What it costs", "", ul(x["costs"]), ""]
    return "\n".join(out)


def diagram_docs(d, pdir):
    """docs/images/*.png and the diagram .md files (uml-diagram.md collects the uml ones)."""
    title, docs = d["project"]["title"], pdir / "docs"
    (docs / "images").mkdir(parents=True, exist_ok=True)
    uml = []
    for x in d["diagram"]:
        diagrams.render(x, docs / "images" / (x["name"] + ".png"))
        if x["name"].startswith("uml-diagram"):
            uml.append(x)
            continue
        kind = x["name"].replace("-diagram", "").replace("-", " ").title()
        (docs / (x["name"] + ".md")).write_text("\n".join([
            "# %s Pattern — %s Diagram" % (title, kind), "", para(x.get("caption", "")),
            "![%s](images/%s.png)" % (x["title"], x["name"]), "", para(x.get("prose", ""))]))
    if uml:
        out = ["# %s Pattern — UML Sequence Diagrams" % title, ""]
        for i, x in enumerate(uml, 1):
            out += ["## %d. %s" % (i, x["title"]), "", para(x.get("caption", "")),
                    "![%s](images/%s.png)" % (x["title"], x["name"]), ""]
        (docs / "uml-diagram.md").write_text("\n".join(out))
    return len(d["diagram"])


# ---------------------------------------------------------- animation ----

def animation(d, pdir):
    p, a = d["project"], d["animation"]
    template = (Path(__file__).with_name("animation_template.html")).read_text()
    boxes = "\n".join(
        '      <div class="row" id="row-%s">\n        <div class="name">%s</div>\n'
        '        <div class="job">%s</div>\n      </div>' % (b[0], b[1], b[2]) for b in a["boxes"])
    steps = [dict(label="Act %d — %s" % (i, s["title"]), narration=_spoken(s),
                  rows=s.get("rows", {}), console=[list(c) for c in s.get("console", [])])
             for i, s in enumerate(d["act"], 1)]
    html = (template.replace("__TITLE__", p["title"]).replace("__SUBTITLE__", a["subtitle"])
            .replace("__BOXES__", boxes).replace("__STEPS__", json.dumps(steps, indent=1, ensure_ascii=False))
            .replace("__ROW_IDS__", json.dumps([b[0] for b in a["boxes"]])))
    (pdir / "docs" / "animation.html").write_text(html)
    return len(steps)


# ------------------------------------------------------------- scenes ----

ORDINAL = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]


def _spoken(act):
    """The animation's words for an act: its own narration, or its video speech without pauses."""
    if act.get("narration"):
        return act["narration"]
    return " ".join(re.sub(r"\[\[slnc \d+\]\]", " ", act["speech"]).split())


def _act_scenes(d):
    """One console slide per act, built from what the demo printed and the act's speech."""
    out = []
    for i, a in enumerate(d["act"], 1):
        lines = ["%s. %s." % (ORDINAL[i - 1].upper(), a["title"])] + ["  " + c[0] for c in a.get("console", [])]
        out.append(dict(key="act-%d" % i, kind="console", title="Act %s — %s" % (ORDINAL[i - 1], a["title"]),
                        body="\n".join(lines), narration=a["speech"]))
    return out


def _expand(d):
    """[[scene]] list with a kind = "acts" marker replaced by one slide per act, keys renumbered."""
    out = []
    for s in d["scene"]:
        out += _act_scenes(d) if s["kind"] == "acts" else [s]
    for n, s in enumerate(out, 1):
        s["key"] = "%02d-%s" % (n, re.sub(r"^\d+-", "", s["key"]))
    return out


def scenes(d, pdir):
    p = d["project"]
    d = dict(d, scene=_expand(d))
    lines = ['"""Scene definitions for the %s teaching video (generated from pattern.toml)."""' % p["title"],
             "", "SCENES = ["]
    for s in d["scene"]:
        body = s.get("body")
        lines.append("    dict(key=%r, kind=%r, title=%r,\n         body=%r,\n         narration=%r),"
                     % (s["key"], s["kind"], s["title"], body, " ".join(s["narration"].split())))
    poster = dict(d.get("poster", {}))
    for k in ("headline", "taglines"):
        if k in poster:
            poster[k] = [tuple(x) for x in poster[k]]
    video = dict(footer="%s Pattern  ·  Java 21" % p["title"], poster=poster or None,
                 highlight=d.get("highlight", {}))
    lines += ["]", "", "VIDEO = %r" % video, ""]
    (pdir / "video" / "scenes.py").write_text("\n".join(lines))
    return len(d["scene"])


def video_readme(d, pdir):
    p = d["project"]
    # The first line shows above YouTube's fold, so it must name the pattern
    # and say plainly what it is before any example.
    desc = p.get("youtube_description") or (
        "%s pattern in Java: %s" % (p["title"], p["bold"]))
    desc = " ".join(desc.split())
    (pdir / "video" / "README.md").write_text("\n".join([
        "# %s Pattern — Teaching Video" % p["title"], "",
        "A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.", "",
        "| File | What it is |", "| --- | --- |",
        "| `%s-pattern-explained.mp4` | the video, 1920×1080 |" % p["slug"],
        "| `%s-pattern-explained.m4a` | audio only |" % p["slug"],
        "| `%s-pattern-explained.srt` | subtitles |" % p["slug"],
        "| `poster.png` | the opening frame |", "",
        "**Narration:** %s. Scenes are generated from `../pattern.toml` into `scenes.py`." % VOICE, "",
        "Suggested description:", "", "> " + desc, ""]))


def all_docs(pdir):
    d = load(pdir)
    slug = d["project"]["slug"]
    docs = pdir / "docs"
    docs.mkdir(exist_ok=True)
    (pdir / "README.md").write_text(readme(d, pdir))
    (docs / "problem-statement.md").write_text(problem(d))
    (docs / "prerequisites.md").write_text(prerequisites(d))
    (docs / "session.md").write_text(session(d))
    (docs / ("%s-pattern-explained.md" % slug)).write_text(explained(d))
    if "dependencies" in d.get("docs", {}):
        (docs / "dependencies.md").write_text(dependencies(d))
    n_diag = diagram_docs(d, pdir)
    n_steps = animation(d, pdir)
    n_scenes = scenes(d, pdir) if d.get("scene") else 0
    video_readme(d, pdir)
    return "README + 4 docs, %d diagrams, %d animation steps, %d scenes" % (n_diag, n_steps, n_scenes)

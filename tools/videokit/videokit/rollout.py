"""Bringing every project into line with AUDIO-VIDEO-SPEC.md, one at a time.

    videokit.sh rollout status            refresh ROLLOUT-REPORT.md, print totals
    videokit.sh rollout next [n]          the next n projects whose script needs rewriting
    videokit.sh rollout extract <slug>    the narration, compactly, for rewriting
    videokit.sh rollout apply <slug> <file>
                                          write a rewritten script into scenes.py,
                                          switch the project to videokit, queue its build
    videokit.sh rollout worker            build queued projects one by one (run it in
                                          the background; it waits for new work)

Progress is saved after every step in tools/videokit/rollout-state.json and
summarised in ROLLOUT-REPORT.md at the repository root, so the work can stop
and resume in any later session.

The rewrite file for `apply` is plain text, one block per scene:

    == 01-poster
    Hello, and welcome. [[slnc 400]] This video explains ...
    == 02-partner
    ...
"""

import ast
import fcntl
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path

from . import narrate
from .project import REPO, Project

STATE = REPO / "tools" / "videokit" / "rollout-state.json"
REPORT = REPO / "ROLLOUT-REPORT.md"
LAUNCHER = REPO / "tools" / "videokit" / "videokit.sh"
STAGES = ("script", "video", "animation")

TOML = """\
# Voice for this video (AUDIO-VIDEO-SPEC.md): Kokoro, open source (Apache 2.0),
# US female, a touch slower than normal for teaching.
[voice]
engine = "kokoro"
voice = "af_bella"
speed = 0.9
"""

SHIM = """\
#!/usr/bin/env bash
#
# Builds this project's teaching video with the shared videokit library:
# slides, narration, the mp4/m4a/srt, poster.png, then the YouTube document
# and spec. Everything specific to this video is in scenes.py (script and
# slide settings) and videokit.toml (voice).
#
#   ./build_video.sh              everything
#   ./build_video.sh build        the video only, no docs
#   ./build_video.sh narrate      one stage (see: {launcher} help)
#
set -euo pipefail
cd "$(dirname "$0")"
exec {launcher} "${{1:-all}}" . "${{@:2}}"
"""


# ---------------------------------------------------------------- state ----

def projects():
    """Every project with a video, in a stable category/name order."""
    return [Project(p.parent) for p in sorted(REPO.glob("gradle-java/*/*-pattern/video/scenes.py"))]


def load():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for p in projects():
        state.setdefault(p.slug, {"group": p.dir.parent.name,
                                  **{k: "pending" for k in STAGES}})
    return state


def save(state):
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1, sort_keys=True))
    tmp.replace(STATE)
    write_report(state)


def mark(slug, **fields):
    # The worker and `apply` both update the state; the lock keeps one
    # writer's change from being lost under the other's.
    with open(STATE.with_suffix(".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = load()
        state[slug].update(fields, updated=time.strftime("%Y-%m-%d %H:%M"))
        save(state)


def claim():
    """Atomically take the next queued project for building, or None."""
    with open(STATE.with_suffix(".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = load()
        queued = [s for s, v in sorted(state.items(), key=lambda kv: (kv[1]["group"], kv[0]))
                  if v.get("video") == "queued"]
        if not queued:
            return None
        state[queued[0]].update(video="building", updated=time.strftime("%Y-%m-%d %H:%M"))
        save(state)
        return queued[0]


def write_report(state):
    rows = sorted(state.items(), key=lambda kv: (kv[1]["group"], kv[0]))
    total = len(rows)

    def count(stage, value):
        return sum(1 for _, v in rows if v.get(stage) == value)

    icon = {"done": "✅", "pending": "⏳", "queued": "🕒", "building": "🔨", "failed": "❌"}
    out = ["# Rollout Report", "",
           "Progress of bringing every project into line with "
           "[`AUDIO-VIDEO-SPEC.md`](AUDIO-VIDEO-SPEC.md). Updated automatically by "
           "`tools/videokit/videokit.sh rollout`; last update %s." % time.strftime("%Y-%m-%d %H:%M"),
           "", "| Stage | Done | Queued | Failed | Pending | Total |",
           "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for stage, label in (("script", "Narration rewritten (simple, audio-first, third-person credit)"),
                         ("video", "Video + audio rebuilt with the sample 03 voice"),
                         ("animation", "Animation narration + step play/pause, self-contained")):
        done, failed = count(stage, "done"), count(stage, "failed")
        queued = count(stage, "queued") + count(stage, "building")
        out.append("| %s | %d | %d | %d | %d | %d |" % (
            label, done, queued, failed, total - done - failed - queued, total))
    complete = sum(1 for _, v in rows if all(v.get(s) == "done" for s in STAGES))
    out += ["", "**%d of %d projects complete, %d remaining.**" % (complete, total, total - complete), ""]

    group = None
    for slug, v in rows:
        if v["group"] != group:
            group = v["group"]
            out += ["", "## %s" % group, "", "| Project | Script | Video | Animation | Note |",
                    "| --- | :---: | :---: | :---: | --- |"]
        out.append("| %s | %s | %s | %s | %s |" % (
            slug, *(icon.get(v.get(s, "pending"), v.get(s)) for s in STAGES),
            v.get("note", "")))
    REPORT.write_text("\n".join(out) + "\n")


# ------------------------------------------------------------- scripts ----

def extract(slug):
    """The narration and slide text of every scene, compactly."""
    p = Project.locate(slug)
    lines = ["# %s  (%d scenes)" % (p.slug, len(p.scenes))]
    for s in p.scenes:
        body = s.get("body")
        if isinstance(body, (list, tuple)):
            body = " / ".join(x for x in body if x)
        body = re.sub(r"\s+", " ", str(body or ""))[:300]
        lines += ["== %s | %s | %s | slide: %s" % (s["key"], s["kind"], s["title"], body),
                  s["narration"]]
    return "\n".join(lines)


def parse_rewrite(text):
    blocks, key = {}, None
    for line in text.splitlines():
        m = re.match(r"==\s*([\w-]+)", line)
        if m:
            key = m.group(1)
            blocks[key] = []
        elif key:
            blocks[key].append(line)
    return {k: re.sub(r"\s+", " ", " ".join(v)).strip() for k, v in blocks.items()}


def _narration_spans(source):
    """(key, start, end) source offsets of each scene's narration value."""
    tree = ast.parse(source)
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line.encode()))
    raw = source.encode()

    def pos(lineno, col):
        return offsets[lineno - 1] + col

    spans = []
    for node in ast.walk(tree):
        pairs = []
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "dict":
            pairs = [(k.arg, k.value) for k in node.keywords]
        elif isinstance(node, ast.Dict):
            pairs = [(getattr(k, "value", None), v) for k, v in zip(node.keys, node.values)]
        d = dict(pairs)
        if "key" in d and "narration" in d and isinstance(d["key"], ast.Constant):
            v = d["narration"]
            spans.append((d["key"].value, pos(v.lineno, v.col_offset),
                          pos(v.end_lineno, v.end_col_offset), v.col_offset))
    return raw, spans


def _literal(text, indent):
    """A narration string as a parenthesised run of <=60-char literals."""
    lines = textwrap.wrap(text, 60, break_on_hyphens=False, break_long_words=False)
    pad = " " * (indent + 4)
    body = "\n".join(pad + repr(l + (" " if i < len(lines) - 1 else ""))
                     for i, l in enumerate(lines))
    return "(\n%s\n%s)" % (body, " " * indent)


def apply(slug, rewrite_file):
    p = Project.locate(slug)
    new = parse_rewrite(Path(rewrite_file).read_text())
    keys = [s["key"] for s in p.scenes]
    if sorted(new) != sorted(keys):
        raise SystemExit("rewrite keys differ from scenes: missing %s, extra %s" % (
            sorted(set(keys) - set(new)), sorted(set(new) - set(keys))))
    narrate.check_wording([{"key": k, "narration": t} for k, t in new.items()])

    path = p.video_dir / "scenes.py"
    raw, spans = _narration_spans(path.read_text())
    for key, a, b, col in sorted(spans, key=lambda s: -s[1]):
        # The value's span excludes grouping parentheses around it; take in
        # every such layer, so the new literal replaces them rather than nesting.
        while True:
            i, j = a - 1, b
            while i >= 0 and raw[i:i + 1] in b" \t\r\n":
                i -= 1
            while j < len(raw) and raw[j:j + 1] in b" \t\r\n":
                j += 1
            if raw[i:i + 1] == b"(" and raw[j:j + 1] == b")" and raw[i - 1:i] != b"t" \
                    and not raw[:i].rstrip().endswith(b"dict"):
                a, b = i, j + 1
            else:
                break
        # Indent continuation lines to where the old value's line began.
        line_start = raw.rfind(b"\n", 0, a) + 1
        indent = len(raw[line_start:a]) - len(raw[line_start:a].lstrip())
        raw = raw[:a] + _literal(new[key], indent).encode() + raw[b:]
    path.write_bytes(raw)
    switch_to_videokit(p)
    mark(p.slug, script="done", video="queued", note="")
    return p


def switch_to_videokit(p):
    """videokit.toml for the voice, build_video.sh as a thin call to the library."""
    (p.video_dir / "videokit.toml").write_text(TOML)
    launcher = os.path.relpath(LAUNCHER, p.video_dir)
    shim = p.video_dir / "build_video.sh"
    shim.write_text(SHIM.format(launcher=launcher))
    shim.chmod(0o755)


# -------------------------------------------------------------- worker ----

def worker(idle_minutes=180):
    """Build queued projects one at a time; wait for more; stop when idle."""
    idle_since = time.time()
    while True:
        if (REPO / "tools/videokit/.stop").exists():
            print("worker: stop file found, stopping")
            return
        slug = claim()
        if slug is None:
            if time.time() - idle_since > idle_minutes * 60:
                print("worker: idle, stopping")
                return
            time.sleep(30)
            continue
        t = time.time()
        r = subprocess.run([str(LAUNCHER), "all", slug], capture_output=True, text=True)
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
        if r.returncode == 0:
            m = re.search(r"(\d+:\d\d), audio continuous", r.stdout)
            mark(slug, video="done", note="%s runtime" % (m.group(1) if m else "?"))
        else:
            mark(slug, video="failed", note=tail[0][:120].replace("|", "/"))
        print("worker: %s %s (%.0fs)" % (slug, "done" if r.returncode == 0 else "FAILED",
                                         time.time() - t), flush=True)
        idle_since = time.time()


def animations():
    """Voice and wire every project's animation.html that is not done yet."""
    from . import animation
    for p in projects():
        if load()[p.slug].get("animation") == "done":
            continue
        if (REPO / "tools/videokit/.stop").exists():
            print("animations: stop file found, stopping")
            return
        t = time.time()
        try:
            msg = animation.build(p)
            mark(p.slug, animation="done")
            print("animations: %s %s (%.0fs)" % (p.slug, msg, time.time() - t), flush=True)
        except (Exception, SystemExit) as e:
            mark(p.slug, animation="failed", note=str(e)[:120].replace("|", "/"))
            print("animations: %s FAILED %s" % (p.slug, e), flush=True)


# ----------------------------------------------------------------- cli ----

def main(args):
    cmd = args[0] if args else "status"
    if cmd == "status":
        state = load()
        save(state)
        for stage in STAGES:
            n = sum(1 for v in state.values() if v.get(stage) == "done")
            print("  %-9s %3d / %d done" % (stage, n, len(state)))
    elif cmd == "next":
        n = int(args[1]) if len(args) > 1 else 1
        state = load()
        todo = [s for s, v in sorted(state.items(), key=lambda kv: (kv[1]["group"], kv[0]))
                if v.get("script") != "done"]
        print("\n".join(todo[:n]))
    elif cmd == "extract":
        print(extract(args[1]))
    elif cmd == "apply":
        p = apply(args[1], args[2])
        print("%s: script applied, video queued" % p.slug)
    elif cmd == "worker":
        worker()
    elif cmd == "animations":
        animations()
    else:
        raise SystemExit(__doc__)

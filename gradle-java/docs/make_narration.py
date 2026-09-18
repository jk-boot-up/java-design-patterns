#!/usr/bin/env python3
"""Write `video/narration.md` for a project from its `video/scenes.py`.

The narration script and the video are built from the same source -- the
`narration` field of each scene -- so the readable script cannot drift from
what the narrator actually says. The only transformation is removing the
`[[slnc N]]` pause directives, which are instructions to macOS's `say` and
mean nothing to a reader.

An existing `narration.md` is never overwritten without `--force`. Several of
the earlier projects have a hand-written script carrying production notes that
are not in `scenes.py`, and regenerating those would throw that work away.

Usage:
    python3 docs/make_narration.py                    # every project
    python3 docs/make_narration.py api-gateway        # one project
    python3 docs/make_narration.py --force retry      # replace an existing one
"""

import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORIES = ("creational", "structural", "behavioural",
              "micro-services-design-patterns", "platform-design-patterns")

PAUSE = re.compile(r"\s*\[\[slnc \d+\]\]\s*")


def load_scenes(path):
    spec = importlib.util.spec_from_file_location("scenes", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SCENES


def title_of(scene):
    """The heading a scene contributes, which is its slide title."""
    return scene.get("title") or scene["key"]


def render(scenes, pattern_name):
    out = ["# %s Pattern — Video Narration Script" % pattern_name, ""]
    for i, scene in enumerate(scenes, start=1):
        out.append("## %d. %s" % (i, title_of(scene)))
        out.append("")
        out.append(PAUSE.sub(" ", scene["narration"]).strip())
        out.append("")
    return "\n".join(out)


def projects():
    for category in CATEGORIES:
        base = os.path.join(ROOT, category)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if name.endswith("-pattern"):
                yield category, name[:-len("-pattern")]


def main():
    args = sys.argv[1:]
    force = "--force" in args
    wanted = [a for a in args if not a.startswith("--")]
    for category, slug in projects():
        if wanted and slug not in wanted:
            continue
        video = os.path.join(ROOT, category, slug + "-pattern", "video")
        scenes_py = os.path.join(video, "scenes.py")
        if not os.path.exists(scenes_py):
            continue
        path = os.path.join(video, "narration.md")
        if os.path.exists(path) and not force:
            print("%-22s kept (already written; --force to replace)" % slug)
            continue
        scenes = load_scenes(scenes_py)
        # The pattern's display name is the poster's title, which is already
        # the one a human chose for it.
        name = scenes[0].get("title") or slug
        with open(path, "w") as fh:
            fh.write(render(scenes, name))
        print("%-22s narration.md  (%d scenes)" % (slug, len(scenes)))


if __name__ == "__main__":
    main()

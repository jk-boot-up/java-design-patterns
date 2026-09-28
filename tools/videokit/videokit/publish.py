"""Regenerate the shared documents that are derived from a finished video.

These generators live in gradle-java/docs and each takes project slugs:
the narration script (from scenes.py), the YouTube document (chapters come
from the SRT) and the project spec (runtime and loudness from the MP4).
"""

import subprocess

STEPS = (
    ("narration.md", "make_narration.py", ["--force"]),
    ("youtube.md", "make_youtube_docs.py", []),
    ("spec", "make_specs.py", []),
)


def run(project, log):
    """Run each generator for this project. Returns the names that ran."""
    tools = project.docs_tools()
    if tools is None:
        return []
    done = []
    for name, script, flags in STEPS:
        if not (tools / script).exists():
            continue
        r = subprocess.run(["python3", str(tools / script), *flags, project.slug],
                           cwd=tools.parent, capture_output=True, text=True)
        log.write("$ %s %s\n%s%s\n" % (script, project.slug, r.stdout, r.stderr))
        if r.returncode:
            raise RuntimeError("%s failed:\n%s" % (script, r.stderr[-2000:]))
        done.append(name)
    return done

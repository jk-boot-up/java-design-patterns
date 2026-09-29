"""patternkit: make a new pattern project from one pattern.toml.

    patternkit.sh scaffold <category> <slug> <package> <MainClass>
                                   new project directory, Gradle build, voice settings,
                                   and a starter pattern.toml
    patternkit.sh docs  <slug>     README, docs/*.md, diagrams, animation.html, scenes.py
    patternkit.sh build <slug>     docs, then ./gradlew test, thumbnail, README.html,
                                   video + audio + animation narration, spec, YouTube doc
                                   and the root index
    patternkit.sh index            regenerate index.md / index.html / the catalogue

Output is one line per step; full tool output goes to <project>/build/patternkit.log.
"""

import shutil
import subprocess
import sys
from pathlib import Path

from . import generate

REPO = Path(__file__).resolve().parents[3]
GRADLE = REPO / "gradle-java"
DOCS = GRADLE / "docs"
VIDEOKIT = REPO / "tools" / "videokit" / "videokit.sh"
PY = Path.home() / ".cache" / "videokit" / "venv" / "bin" / "python"
TEMPLATE = GRADLE / "structural" / "adapter-pattern"

BUILD_GRADLE = """plugins {
    id 'java'
    id 'application'
}

group = 'com.jk.explore'
version = '1.0-SNAPSHOT'

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation platform('org.junit:junit-bom:5.10.2')
    testImplementation 'org.junit.jupiter:junit-jupiter'
    testImplementation 'org.junit.jupiter:junit-jupiter-params'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

application {
    mainClass = 'com.jk.explore.%s.%s'
}

test {
    useJUnitPlatform()
}
"""

VOICE_TOML = """# The approved voice (amy-slow): Piper, open source (MIT), US female,
# slower than normal with longer pauses, for beginners listening without a screen.
[voice]
engine = "piper"
voice  = "en_US-amy-medium"
speed  = 0.8

[pacing]
sentence_gap = 0.7
pause_scale  = 1.5
"""

BUILD_VIDEO = """#!/usr/bin/env bash
# Builds this project's video with the shared videokit library (see video/videokit.toml).
set -euo pipefail
cd "$(dirname "$0")"
exec ../../../../tools/videokit/videokit.sh "${1:-all}" . "${@:2}"
"""

ANIMATION_AUDIO = """#!/usr/bin/env bash
# Narration clips for animation.html, from the shared videokit library.
set -euo pipefail
cd "$(dirname "$0")/.."
exec ../../../tools/videokit/videokit.sh animation . "$@"
"""


def project_dir(slug):
    hits = sorted(GRADLE.glob("*/%s-pattern" % slug))
    if len(hits) != 1:
        raise SystemExit("patternkit: %s project %r" % ("no" if not hits else "more than one", slug))
    return hits[0]


def scaffold(category, slug, package, main_class):
    p = GRADLE / category / (slug + "-pattern")
    if p.exists():
        raise SystemExit("patternkit: %s already exists" % p)
    (p / "src/main/java/com/jk/explore" / package).mkdir(parents=True)
    (p / "src/test/java/com/jk/explore" / package).mkdir(parents=True)
    (p / "docs").mkdir()
    (p / "video").mkdir()
    for f in ("gradlew", "gradlew.bat"):
        shutil.copy2(TEMPLATE / f, p / f)
    shutil.copytree(TEMPLATE / "gradle", p / "gradle")
    (p / "settings.gradle").write_text("rootProject.name = '%s-pattern'\n" % slug)
    (p / "build.gradle").write_text(BUILD_GRADLE % (package, main_class))
    (p / "video/videokit.toml").write_text(VOICE_TOML)
    (p / "video/build_video.sh").write_text(BUILD_VIDEO)
    (p / "docs/make_animation_audio.sh").write_text(ANIMATION_AUDIO)
    for f in ("video/build_video.sh", "docs/make_animation_audio.sh"):
        (p / f).chmod(0o755)
    cat_readme = GRADLE / category / "README.md"
    if not cat_readme.exists():
        name = category.replace("-design-patterns", "").replace("-", " ").title()
        cat_readme.write_text("# %s Patterns\n\nThe projects in this category are listed, with links, in the "
                              "repository [index](../../index.md).\n" % name)
    shutil.copy2(Path(__file__).with_name("pattern_template.toml"), p / "pattern.toml")
    text = (p / "pattern.toml").read_text()
    (p / "pattern.toml").write_text(text.replace("__SLUG__", slug).replace("__CATEGORY__", category)
                                    .replace("__PACKAGE__", package).replace("__MAIN__", main_class))
    return p


def run(log, *cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    log.write("$ %s\n%s%s\n" % (" ".join(str(c) for c in cmd), r.stdout, r.stderr))
    if r.returncode:
        raise SystemExit("patternkit: failed: %s\n%s" % (" ".join(str(c) for c in cmd),
                                                        (r.stdout + r.stderr)[-1500:]))
    return r.stdout


def build(slug, media=True):
    p = project_dir(slug)
    (p / "build").mkdir(exist_ok=True)
    with open(p / "build" / "patternkit.log", "a") as log:
        print("  docs      " + generate.all_docs(p))
        out = run(log, p / "gradlew", "-q", "test", "run", cwd=p)
        print("  gradle    tests pass; demo printed %d lines" % len(out.splitlines()))
        run(log, PY, DOCS / "make_thumbnails.py", slug, cwd=GRADLE)
        print("  thumbnail docs/thumbnail.png")
        run(log, "python3", DOCS / "make_readme_html.py", p.relative_to(GRADLE), cwd=GRADLE)
        print("  html      README.html")
        if media:
            run(log, VIDEOKIT, "all", slug)
            print("  video     video, audio, subtitles, narration.md, youtube.md, spec")
            run(log, VIDEOKIT, "animation", slug)
            print("  animation narration clips + player")
        else:
            run(log, "python3", DOCS / "make_specs.py", "--no-measure", slug, cwd=GRADLE)
            print("  spec      docs/spec.md + spec.html (video not built yet)")
        run(log, "python3", DOCS / "make_index.py", cwd=REPO)
        print("  index     index.md, index.html, docs/design-patterns-catalog.md")


def main(argv):
    if not argv or argv[0] in ("help", "-h"):
        print(__doc__.strip())
        return
    cmd, rest = argv[0], argv[1:]
    if cmd == "scaffold":
        print(scaffold(*rest))
    elif cmd == "docs":
        print(generate.all_docs(project_dir(rest[0])))
    elif cmd == "build":
        build(rest[0], media="--no-media" not in rest)
    elif cmd == "index":
        subprocess.run(["python3", str(DOCS / "make_index.py")], check=True)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])

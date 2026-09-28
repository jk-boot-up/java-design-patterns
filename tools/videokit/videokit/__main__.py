"""Command line.

    videokit.sh all       <project>   slides, narrate, video, subtitles, docs
    videokit.sh build     <project>   the same without docs
    videokit.sh <stage>   <project>   one stage: slides | narrate | video | subtitles | docs
    videokit.sh animation <project>   voice docs/animation.html; add narration + step play/pause
    videokit.sh clean     <project>   delete build/, including the narration cache
    videokit.sh samples   <text-file> <out-dir> <engine:voice[@pace]>...
    videokit.sh voices                list the Kokoro voices
    videokit.sh rollout ...           bring every project up to AUDIO-VIDEO-SPEC.md (rollout help)

Options: --force (re-voice every scene), --keep (keep intermediates).
<project> is a project directory, its video/ directory, or its slug.
"""

import sys

from . import pipeline, samples
from .project import Project


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    for f in flags:                       # --version=amy-slow: a named alternative build
        if f.startswith("--version="):
            import os
            os.environ["VIDEOKIT_VERSION"] = f.split("=", 1)[1]
    args = [a for a in argv if not a.startswith("--")]
    if not args or args[0] in ("help", "-h"):
        print(__doc__.strip())
        return
    cmd, rest = args[0], args[1:]
    opts = dict(force="--force" in flags, keep="--keep" in flags)

    if cmd == "rollout":
        from . import rollout
        rollout.main(rest)
        return
    if cmd == "samples":
        text = open(rest[0]).read()
        for p in samples.render(text, rest[1], rest[2:]):
            print("  " + str(p))
        return
    if cmd == "voices":
        from .tts.kokoro import KokoroEngine
        print(" ".join(KokoroEngine().voices()))
        return

    if cmd == "animation":
        from . import animation
        for target in rest or ["."]:
            project = Project.locate(target)
            print("%s: %s" % (project.name, animation.build(project, opts["force"])))
        return

    stages = {"all": pipeline.ORDER, "build": pipeline.BUILD_STAGES}.get(cmd, (cmd,))
    if cmd != "clean" and not set(stages) <= set(pipeline.ORDER):
        raise SystemExit("videokit: unknown command %r (try: help)" % cmd)
    if not rest:
        raise SystemExit("videokit: which project?")
    for target in rest:
        project = Project.locate(target)
        if cmd == "clean":
            pipeline.clean(project)
            print("%s: cleaned" % project.name)
            continue
        print(project.name)
        pipeline.run(project, stages, **opts)


if __name__ == "__main__":
    main(sys.argv[1:])

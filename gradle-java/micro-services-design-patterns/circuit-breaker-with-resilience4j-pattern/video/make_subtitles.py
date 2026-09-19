#!/usr/bin/env python3
"""Generate an SRT subtitle file for the Layered Architecture pattern video.

Timings are measured from the *encoded scene clips*, not from the raw
narration audio. The clips run slightly longer than the speech they contain
(encoder frame alignment), and timing against the raw audio would let that
difference accumulate into tens of seconds of caption drift by the end.

Each scene's narration is split into caption-sized cues and spread across
that scene's measured duration.

Usage:
    python3 make_subtitles.py [build_dir] [output.srt]

Requires the per-scene clips, so run it from build_video.sh (or with
KEEP_INTERMEDIATE=1) while those still exist.
"""

import os
import re
import subprocess
import sys

from scenes import SCENES

# Roughly one line of readable caption; YouTube shows ~2 lines at a time.
MAX_CHARS = 84
TAIL_PAD = 0.9  # matches the apad in build_video.sh


def duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", path,
    ])
    return float(out.strip())


def spoken_text(text):
    """Drop the embedded speech commands `say` understands.

    The narration carries `[[slnc NNN]]` pause markers for pacing. They are
    instructions to the synthesiser, not words, so they must never reach the
    captions.
    """
    return re.sub(r"\s+", " ", re.sub(r"\[\[[^\]]*\]\]", " ", text)).strip()


def split_cues(text, max_chars=MAX_CHARS):
    """Split narration into caption-sized chunks, preferring sentence ends."""
    sentences = re.findall(r"[^.!?]+[.!?]?", spoken_text(text))
    cues, cur = [], ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(cur) + len(s) + 1 <= max_chars:
            cur = (cur + " " + s).strip()
            continue
        if cur:
            cues.append(cur)
        # a single sentence longer than the limit -> break on words
        while len(s) > max_chars:
            cut = s.rfind(" ", 0, max_chars)
            cut = cut if cut > 0 else max_chars
            cues.append(s[:cut].strip())
            s = s[cut:].strip()
        cur = s
    if cur:
        cues.append(cur)
    return cues


def ts(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def main():
    build = sys.argv[1] if len(sys.argv) > 1 else "build"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "circuit-breaker-with-resilience4j-pattern-explained.srt"

    blocks, index, clock = [], 1, 0.0

    for scene in SCENES:
        clip = os.path.join(build, "scene-" + scene["key"] + ".mp4")
        if not os.path.exists(clip):
            sys.exit(
                "missing %s\nRun ./build_video.sh with KEEP_INTERMEDIATE=1 so the\n"
                "scene clips are still present when subtitles are generated."
                % clip
            )

        scene_total = duration(clip)
        # Captions cover the spoken portion; the tail of the clip is silence.
        speech = max(scene_total - TAIL_PAD, 0.1)
        cues = split_cues(scene["narration"])

        # Spread cues across the spoken part in proportion to their length,
        # leaving the trailing pad silent.
        total_chars = sum(len(c) for c in cues) or 1
        t = clock
        for cue in cues:
            span = speech * (len(cue) / total_chars)
            blocks.append(
                "%d\n%s --> %s\n%s\n" % (index, ts(t), ts(t + span), cue)
            )
            index += 1
            t += span

        clock += scene_total

    with open(out_path, "w") as fh:
        fh.write("\n".join(blocks))

    print("subtitles -> %s  (%d cues, %s total)" % (out_path, index - 1, ts(clock)))


if __name__ == "__main__":
    main()

#!/usr/bin/env bash
#
# Builds this project's teaching video with the shared videokit library:
# slides, narration, the mp4/m4a/srt, poster.png, then the YouTube document
# and spec. Everything specific to this video is in scenes.py (script and
# slide settings) and videokit.toml (voice).
#
#   ./build_video.sh              everything
#   ./build_video.sh build        the video only, no docs
#   ./build_video.sh narrate      one stage (see: ../../../../tools/videokit/videokit.sh help)
#
set -euo pipefail
cd "$(dirname "$0")"
exec ../../../../tools/videokit/videokit.sh "${1:-all}" . "${@:2}"

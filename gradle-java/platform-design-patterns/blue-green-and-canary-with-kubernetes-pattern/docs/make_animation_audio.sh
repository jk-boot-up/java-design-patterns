#!/usr/bin/env bash
# Narration clips for animation.html now come from the shared library, in the
# project's own voice. See AUDIO-VIDEO-SPEC.md at the repository root.
set -euo pipefail
cd "$(dirname "$0")/.."
exec ../../../tools/videokit/videokit.sh animation . "$@"

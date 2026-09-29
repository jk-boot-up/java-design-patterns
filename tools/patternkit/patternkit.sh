#!/usr/bin/env bash
# Launcher for patternkit, run in videokit's Python environment (Pillow, fonts).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -x "$HOME/.cache/videokit/venv/bin/python" ] || "$HERE/../videokit/videokit.sh" help >/dev/null
PYTHONPATH="$HERE:$HERE/../videokit" exec "$HOME/.cache/videokit/venv/bin/python" -m patternkit "$@"

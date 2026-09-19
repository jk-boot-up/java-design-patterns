#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-6.m4a
#
# Requirements: macOS (for `say`) and ffmpeg.
#
set -euo pipefail

cd "$(dirname "$0")"

OUT=audio
VOICE="${VOICE:-Samantha}"
RATE="${RATE:-145}"

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

narrate() {
cat <<'EOF'
Act one. With no settings, the executor has eight core threads and a queue with no bound. That is the trap from the hand-built project, as a default.
Act two. The caller is the main thread. The work ran on a pool thread named task-1. One annotation replaced the hand-built class.
Act three. All eight workers are stuck on a slow step. A thousand more orders arrive, and all thousand wait in the queue. None is refused.
Act four. Two threads and a queue of three. Two orders run and three wait. The sixth is refused with a TaskRejectedException, thrown to the caller at once.
Act five. A method calls another async method through this. It runs on the main thread. The proxy was skipped, and nothing complained.
Act six. One thread. The packing task asks the same pool to print a label, and waits. The label task is queued behind it, so it starves.
EOF
}

i=0
while IFS= read -r line <&3; do
    i=$((i + 1))
    printf '%s' "$line" > "$OUT/.step-$i.txt"
    say -v "$VOICE" -r "$RATE" -o "$OUT/.step-$i.aiff" -f "$OUT/.step-$i.txt"
    ffmpeg -y -loglevel error -i "$OUT/.step-$i.aiff" \
        -c:a aac -b:a 128k -ar 44100 -ac 1 "$OUT/step-$i.m4a"
    rm -f "$OUT/.step-$i.aiff" "$OUT/.step-$i.txt"
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/step-$i.m4a")
    printf 'step-%d.m4a  %5.1fs\n' "$i" "$dur"
done 3< <(narrate)

echo
echo "Wrote $i clips to $OUT/"

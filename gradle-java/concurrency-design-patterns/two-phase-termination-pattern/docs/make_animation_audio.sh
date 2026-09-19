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
Act one. The shop closes the ledger while order one is half written. Only line one was written. The order is left half written.
Act two. Stop is requested while order one is half written and order two is waiting. The worker finishes order one, all three lines, starts nothing else, and ends. Nothing is half written.
Act three. A stop request that only sets a flag does nothing to a worker waiting for an order: it is still waiting. With an interrupt to wake it, the worker ends.
Act four. The worker is interrupted while waiting, and its cleanup still runs, because it is in a finally block.
Act five. The worker is stuck in something that ignores the request. After two hundred milliseconds it has not ended, and is still alive. Phase two has a time limit, and what comes next is a decision, because Java gives no safe way to force a thread to stop.
Act six. Stopped with five orders still waiting: one finished, five pending. Those five were accepted from customers and not done. A stop needs a policy, and shutting down took as long as the order in progress.
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

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
Act one. An order of three lines is picked by one person, one line after another: three steps in a row, while the other pickers stand idle.
Act two. The order becomes three parts, each with the order's id, its own number, and how many there are in all. That is what lets them be put back.
Act three. Suppose the pickers finish in the order three, one, two. Nothing guarantees the parts come back in the order they went.
Act four. Part three arrives, then part one, and the aggregator waits. Part two arrives, and the order is complete, in its original line order.
Act five. Parts one and three arrive, and part two's picker has gone home. After twenty nine minutes nothing has expired. After thirty, the aggregator gives up, with two of three lines and part two named as missing.
Act six. A thousand orders each missing one part means a thousand orders held in memory. A part delivered twice is counted once. And two orders with the same id would be mixed into one, so the id must be unique.
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

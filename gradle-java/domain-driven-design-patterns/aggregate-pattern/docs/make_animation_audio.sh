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
Act one. With a public list, a line of minus three mugs goes in. The same machine goes on two lines, and the total passes five thousand pounds. A line is even added after the order was placed.
Act two. Every operation goes through the root. Nought mugs, and eleven mugs, are refused. Five more of the same, making eleven, are refused. A total over a thousand pounds is refused. A change after placing is refused, and an empty order cannot be placed.
Act three. The list of lines seen from outside is read-only, and a line has no public constructor, so no line exists that the order has not checked.
Act four. Three orders that hold the whole customer load the customer three times. Three that hold only an id load none.
Act five. Two clerks read the same order and each add a line. The first save is accepted. The second is refused, because the order changed since it was read.
Act six. If one aggregate holds the customer and all their orders, two clerks changing different orders collide. With one aggregate per order, both saves are accepted.
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

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
Act one. The find call with mugs, twenty five hundred, true, true and ten gives the blue mug and the big mug. With the two booleans the other way round, it gives three mugs, including one that is not in stock. Both compile. Which is in stock, and which is the sort? You must count the arguments to know.
Act two. Search, category mugs, under twenty five hundred, in stock, cheapest first, first ten. The same answer as the long call, and every part names itself.
Act three. Category only: green tea. Under a thousand, any category: the blue mug, and green tea. And the order of the optional parts does not matter.
Act four. A query that never changes: cheap gives the blue mug, dear gives three mugs, and the base still gives four. A query that changes itself: cheap and dear give the same three mugs. They are the same object. The cheap query was spoiled by the dear one.
Act five. At the start, the only thing offered is category. Then, under. Then, cheapest first, in stock, or run. A call out of order does not compile.
Act six. Under minus five was accepted, and nothing complained. It failed at run, saying the price limit is below zero. The mistake and the report are on different steps of one long line. A debugger cannot stop between the calls of one chain, and a stack trace names the line, not the step. And it is a small language that someone designed: this one has seven methods to learn, and to keep.
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

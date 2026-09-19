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
Act one. Two mugs are ordered: sixteen pounds, and the stock falls to eight. The whole action is one method.
Act two. The card is declined after the stock was taken. The transaction undoes the stock change, so the stock is back to ten and no order exists.
Act three. The bulk discount moved from ten items to five. One script was told. Seven mugs cost fifty pounds forty when placed, and fifty six pounds when the same order is amended.
Act four. The pricing moves into one helper function that both scripts call. They agree again, and the design is still procedural.
Act five. The first script has three decisions, so eight paths. After a year of new rules it has seven decisions, so a hundred and twenty eight paths, and every rule went in the middle of one method.
Act six. A month end job that adds up the orders is a dozen lines, read once and changed rarely. That is a script at its best.
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

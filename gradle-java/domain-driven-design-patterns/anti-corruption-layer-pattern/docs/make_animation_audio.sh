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
Act one. Four features each read the old record directly, so four places have learnt that Y means in stock, and D means discontinued.
Act two. The adapter turns each old record into a stock level, with a real number and a meaning. No code crosses the layer.
Act three. A quantity of twelve X fails deep in a report with no sku in the message. The layer refuses it at the door, naming the sku and the problem.
Act four. The old system starts sending H for on hold. The four features each guess. The page says in stock, and the basket allows it. The layer decides once: on hold, and it cannot be bought.
Act five. The old row has seven fields. The shop uses four. The layer drops three, and any feature that later needs one has to extend the layer and the shop's model.
Act six. The shop speaks four availability words of its own. Replace the old system, and only the adapter changes.
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

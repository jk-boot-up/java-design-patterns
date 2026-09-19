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
Act one. Prices as doubles: three stamps give three point three, then a long tail of zeros and a three. Ten pounds and ten dollars add up to twenty, with no complaint.
Act two. With whole pence, three stamps come to exactly three pounds thirty. Pounds plus dollars is refused, with a clear message.
Act three. Three separate objects of five pounds collapse to one in a set. A class that compares by identity keeps all three. Five pounds and five dollars are not equal.
Act four. A mutable price shared by two orders lets one order's discount change the other's price. With values, each discount makes a new amount and the original is untouched.
Act five. Three methods take an email as a string. Two check it, and the third does not, so a bad address is stored. An EmailAddress cannot be built wrong, so no method that receives one ever checks.
Act six. Ten pounds split three ways by rounding loses a penny. Allocation gives the odd penny to the first share, and the shares add to exactly ten pounds.
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

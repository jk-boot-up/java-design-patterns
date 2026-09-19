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
Act one. The catalog renamed price cents to price, and released. Checkout, two mugs: the order failed. It was found in production, by a customer.
Act two. Checkout's contract: price cents, an integer, and sku, a string. Reports' contract: sku, a string. Each lists only the fields it reads, and their types.
Act three. The catalog's real answer is checked against both contracts. No problems. Safe to release.
Act four. The same check on the renamed release reports: checkout expects price cents, an integer, and it is missing. The build fails, and it names the consumer and the field.
Act five. A release that adds a stock field: no problems. And the rename again, per consumer: checkout, one problem; reports, none. Reports never used that field.
Act six. A release that now sends pounds, not pence, in the same field: no problems. It passes. Checkout, two mugs: total thirty two, where it should be thirty two hundred. A contract checks the shape, and not the meaning. And every consumer must keep its contract up to date, or the check protects nobody.
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

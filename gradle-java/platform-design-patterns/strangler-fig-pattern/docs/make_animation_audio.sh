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
Act one. Twenty-six weeks with no real traffic, then a cutover. One of four capabilities is faulty on Monday, and the only rollback takes all four back.
Act two. Every capability starts on legacy. Pricing moves first. An order goes through, priced by the new code and served by legacy for the rest. The checkout never stops.
Act three. Legacy serves. The new pricing is called too and compared. It disagrees on 29 of 201 orders: VAT rounding, and exactly fifty pounds. Found before any customer paid differently.
Act four. New payment misbehaves on a large order. One switch flips payment back to legacy. Pricing never moved back.
Act five. Stock moved to the new service. It says 395. The legacy table its reports read says 400. Two tables claim to be the truth.
Act six. Budget goes elsewhere after quarter two. Two of four moved, forever. That costs 115 a quarter: more than all legacy, more than all new.
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

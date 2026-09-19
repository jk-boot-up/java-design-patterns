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
Act one. Premium, gift wrap, and both: four classes for two features. A third feature would need eight. A premium gift order is ninety six hundred. And an order cannot change its class once it exists.
Act two. One order class. With no rule, ten thousand. With premium, nine thousand. With gift wrap, ten thousand six hundred.
Act three. The customer joins the premium plan while shopping. The same order object: ten thousand, then nine thousand.
Act four. Premium then gift wrap: ninety six hundred, the same as the class made for both. Classes added: none.
Act five. Gift wrap is three hundred for each item, so it must look at the order it was called for. Two items: ten thousand six hundred. Three items: ten thousand nine hundred. That is why the order passes itself in: the helper is a different object, and does not know which order it is helping.
Act six. One total made three calls to helpers, where inheritance made none: one more hop for every helper. To look like a helper with four methods, the order had to write four forwarding methods that only pass the call on. And a helper knows nothing of its owner unless it is told.
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

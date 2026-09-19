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
Act one. One Customer class has twelve fields, and each department uses only a handful. Every department depends on all of them.
Act two. Is Ada active? Sales says yes, she bought lately. Shipping says yes, a parcel is on its way. Support says no, she has no open ticket. Each is right in its own context.
Act three. Sales has a buyer, Shipping a recipient and Support a contact, each with four fields. None knows the others' types. They share only the customer id.
Act four. Sales renames Ada and publishes a fact. Until it is delivered, Shipping still has the old name. After delivery, Shipping updates its own recipient, and never sees a buyer.
Act five. A test scans the source and finds no import of one context's types by another. Shipping can change its own model freely.
Act six. Ada's name is stored three times. Between a rename and its delivery, two contexts disagree. And every context needs its own translator for every event it cares about.
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

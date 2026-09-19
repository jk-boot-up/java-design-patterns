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
Act one. Checkout, renewal and gift card each build the provider's request and read its codes. Three network calls. The gift card top up forgot the currency field, and nobody has noticed.
Act two. The shop asks twice through the gateway. The first is approved and the second declined, and checkout has no field name and no result code in it.
Act three. A fake gateway, told what to answer, gives approved, declined and unavailable, with no network calls at all.
Act four. The gateway retries a single timeout once, so the shop is told paid, after two network calls. After two timeouts it says unavailable. The rule lives in one class.
Act five. The same checkout runs on Acme and on a second provider with a completely different client. It was given a different gateway, and was not changed.
Act six. Acme can hold a payment and capture part of it later, and the interface has only charge. Adding it means a new method on the interface and on all three gateways, and BetaPay cannot do it at all.
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

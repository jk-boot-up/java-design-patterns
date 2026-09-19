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
Act one. The answer arrived on the fifth look. Five looks were made, and four of them found nothing. And the caller could do nothing else in that time.
Act two. The charge is requested, and the caller goes on. The caller does other work. Then the callback runs: order one, paid.
Act three. One callback, told the result. Order one was paid: ship it. Order two was declined: ask for another card.
Act four. The first callback threw an error. The gateway went on, and order two was paid. The error was recorded: order one, the mail server was down. The one who asked never sees that exception, because it happened in someone else's call.
Act five. Remembering the order in a field: both callbacks say order two. Each callback holding its own order id: order two paid, order one paid. The answers came in the other order, and each is right.
Act six. Pay, then reserve, then ship: three callbacks, each inside the one before, three levels deep. The lines run in one order, but are written in another: in the code, the line that asks stock is written below the block that ships, and it runs first. Every level needs its own handling for a failure. And each answer arrives with no stack that shows who asked.
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

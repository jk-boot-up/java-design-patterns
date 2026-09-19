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
Act one. The order service calls inventory, email and analytics itself. It knows three services by name, and a fourth means editing it.
Act two. The order service publishes once, and all three subscribers get the event. A fourth, loyalty points, is added, and gets the event. The order service was not changed.
Act three. Five orders are published. Email handles all five, and analytics only one, with a backlog of four. Analytics catches up later, without holding up email or the publisher.
Act four. Email asks only for placed orders and gets one. Analytics asks for everything and gets a placed and a cancelled event.
Act five. Three orders were published before loyalty joined, and one after. A live subscriber sees only the last. One that reads from the start sees all four, because the log was kept.
Act six. Email is down when the order is placed, and the publisher is told nothing. When it comes back it catches up, because its place in the log was kept. The publisher still cannot ask whether the email went out.
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

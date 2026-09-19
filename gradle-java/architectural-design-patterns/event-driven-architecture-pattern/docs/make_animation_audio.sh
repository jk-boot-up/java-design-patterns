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
Act one. The order service calls shipping and waits. Shipping is down. The order is not accepted. A customer lost an order because a service they never see was down.
Act two. The order service appends the event at position zero, and finishes. It has no reference to inventory or shipping. Both read the log, and both act.
Act three. Shipping is down. Three orders are accepted anyway. Shipping has planned nothing, and is three events behind. When it comes back, it catches up, and plans all three.
Act four. Analytics is added after two orders. It reads the log from the start, and sees both. The order service was not touched.
Act five. The order is accepted, and stock in the warehouse is still ten. It should be nine. After inventory reads the log, it is nine. For a moment, the two disagree. The system is eventually consistent, not consistent at every instant.
Act six. The same event is delivered twice. Without a duplicate check, stock is eight. With one, it is nine, which is right. And the flow of an order is now spread over several services. To see it, you read the log, not one piece of code.
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

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
Act two. The order service sends the event to Kafka, which gives it offset zero, and it finishes. It has no reference to inventory or shipping. Both read the topic, and both see the order.
Act three. Shipping read the first order, and then went down. Three more orders were accepted. Shipping is three events behind, as the broker counts it. Shipping came back and caught up, from where it stopped. It has now planned four orders, and is none behind.
Act four. Analytics is added after two orders. It reads the topic from the start, and sees both. The order service was not touched. Kafka keeps the events, so a new service can be built from history.
Act five. The order is accepted, and stock in the warehouse is still ten. It should be nine. After inventory reads the topic, it is nine. For a moment, the two disagree. The system is eventually consistent, not consistent at every instant.
Act six. The same event is delivered twice, as Kafka may after a missed commit. Without a duplicate check, stock is eight. With one, it is nine, which is right. The flow of an order is now spread over several services, so to see it, you read the topic, not one piece of code. And a broker is another system to run.
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

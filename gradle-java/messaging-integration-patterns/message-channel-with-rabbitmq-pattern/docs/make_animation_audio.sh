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
Act one. The warehouse system is down for maintenance. Checkout calls it directly, three times, and all three checkouts fail. The shop cannot sell while another system is away, even though selling does not need the warehouse to answer yet.
Act two. A RabbitMQ broker is now running in a container. Checkout sends three pick orders to a queue and carries on without waiting. The warehouse is listening, and is handed each order once. When it has finished, nothing is left waiting.
Act three. Now the warehouse is not running at all, so no receiver exists anywhere. Checkout sends three orders and none of them fail. The broker holds all three. When the warehouse starts up afterwards, it works through them in the order they went in.
Act four. A picker takes order one and crashes before saying it is done. The broker had kept its own copy, so it puts the order back, and one is waiting again. A second picker is handed the same order, marked as seen before, and says done. Only then does the broker forget it. Two deliveries, one order picked, none waiting.
Act five. Two queues, both kept by the broker across a restart, each given the same three orders. One queue's messages are marked to be written to disk; the other's are held in memory only. The broker program is stopped and started again. Both queues come back. One still holds three orders. The other holds none.
Act six. The warehouse stays down, and a queue with room for five is given eight. It has been told to refuse rather than quietly drop the oldest, and checkout asks for a receipt on every send. Five are accepted and three refused, and checkout hears about every refusal. The sender now learns only that the broker took a message. And the broker is a third system to run: one container, for one shop and one warehouse.
EOF
}

i=0
while IFS= read -r line <&3; do
    i=$((i + 1))
    printf '%s' "$line" > "$OUT/.step-$i.txt"
    say -v "$VOICE" -r "$RATE" -o "$OUT/.step-$i.aiff" -f "$OUT/.step-$i.txt"
    ffmpeg -y -loglevel error -i "$OUT/.step-$i.aiff" \
        -af "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11" \
        -c:a aac -b:a 128k -ar 44100 -ac 1 "$OUT/step-$i.m4a"
    rm -f "$OUT/.step-$i.aiff" "$OUT/.step-$i.txt"
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/step-$i.m4a")
    printf 'step-%d.m4a  %5.1fs\n' "$i" "$dur"
done 3< <(narrate)

echo
echo "Wrote $i clips to $OUT/"

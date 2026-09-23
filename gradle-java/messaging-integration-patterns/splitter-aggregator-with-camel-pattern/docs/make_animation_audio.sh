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
Act one. One worker takes the whole basket and walks all three warehouses, one line after another: three steps of work on one thread. The basket comes to two hundred and eighty three pounds and forty two pence, and while that worker walks, the other two warehouses stand idle.
Act two. The split step sends out one message for each line. Camel numbers the pieces itself and copies the order number onto every one of them. That number is the only thing that will put them back together.
Act three. The warehouses answer third, first, second. The aggregator does not care. It files each arrival under the place it says it is, so the answer comes out in the customer's own line order. Camel says the reason it finished was size: three messages arrived and three were expected.
Act four. Now Glasgow is closed. Its message reaches the warehouse and stops there, and nothing downstream is told. Two shipments reach an aggregator whose only condition is a count of three. Two is not three, so no answer comes out, one order sits open, and nothing will ever change that.
Act five. The same thing happens to a second aggregator, and this one also has a deadline: six hundred milliseconds, looked at every hundred. A background checker watches the clock. When the deadline passes it ends the wait, with nobody asking. Camel's word for the reason is timeout, not size. The answer carries two of three shipments, names Glasgow as the one that never came, and comes to two hundred and sixty five pounds and ninety seven pence.
Act six. A thousand orders each short of one shipment means a thousand orders held in the aggregator's memory, and a restart throws all of them away. Then the surprise: completion by size counts messages, not distinct pieces. Deliver the Reading shipment twice and the order is declared finished with only two of its three lines. The duplicate check is yours to write, and it is the difference between charging two hundred and sixty five pounds and charging five hundred and fifteen.
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

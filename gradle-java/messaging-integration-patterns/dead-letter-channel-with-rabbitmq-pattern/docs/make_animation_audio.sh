#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-8.m4a
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
Step one. Four orders are on a queue with no rule written on it. The second has an address nothing can read. The worker takes it, fails, refuses it, and asks for it back. The broker puts it at the head of the line again.
Step two. Over twelve turns, eleven go to the same unreadable order. Only the first order was handled. Two good orders are still waiting, and they will wait for ever.
Step three. The same four orders, on a queue declared with a rule. The rule names an exchange to send a dead order to, and a queue is tied to that exchange. Nothing has died yet. The rule is just sitting there.
Step four. The worker gives each order three deliveries. On the third failure it refuses the unreadable order for good. Now the worker does nothing more. The broker takes the order out of the queue and puts it on the parked queue. The two good orders behind it go through.
Step five. The parked order comes back with a note attached, written by the broker. The note says which queue it died in, how many times it has died, and one word for the reason: rejected. The order itself is exactly what the shop sent.
Step six. Two more orders die and no worker touches either. One sat in a queue with a time limit of five hundred milliseconds and nobody read it. The reason is expired. The other was in a queue that holds two orders when a third arrived, so the broker pushed the oldest out. The reason is maxlen.
Step seven. An operator finds the cause and fixes the address parser. The parked order is published back onto the working queue and goes through. It is handled last, behind the orders that were behind it, and the broker's note does not travel with it.
Step eight. Forty orders, half of them unreadable. Twenty are shipped and twenty are parked, and every one of the forty was paid for by a customer. The working queue reports nothing waiting, so every dashboard shows the shop healthy. The loss is in the parked queue, and nothing tells anyone to look at it.
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

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
Act one. A sale sends 100 orders at once. Checkout puts each one on a queue on Amazon SQS, played by LocalStack. SQS takes at most 10 orders in one request, and when sent 11 it says so. So the burst goes as 10 requests of 10, and SQS reports 100 orders waiting and 0 in flight. Nobody was refused, and SQS will keep an order nobody takes for 345600 seconds, which is 4 days.
Act two. The packing service asks for 11 at once, and SQS refuses: it hands out between 1 and 10. It takes 10. For a moment SQS reports 90 waiting and 10 in flight, which means taken but not yet finished. The packer packs the 10 and only then deletes them. Round after round the depth falls: 90, 80, 70, and so on down to 0. 100 packed in 10 rounds, never more than 10 at once.
Act three. SQS hides a taken order for a while, then hands it out again. That time is called the visibility timeout, and it is 30 seconds unless you set it. This queue's is 2 seconds. A packer takes order 2001 and stops before it finishes. SQS reports 0 waiting and 1 in flight, and a second packer asking at once is given 0 orders. Once the 2 seconds have passed, order 2001 comes back, handed out 2 times. SQS never knew the first packer stopped. It only knew the time ran out.
Act four. Packer A takes order 3001 and needs longer than 2 seconds. The time runs out, and packer B is given order 3001 too. Both pack it and both delete it, so the customer gets two parcels for one order. Next, packer A takes order 3002 and, before its time runs out, tells SQS it is still working: hide it 10 seconds more. Packer B asks SQS to hold its question open for 3 seconds, past the old timeout, and is given 0 orders. Order 3002 is packed 1 time.
Act five. 100 orders on a queue with a 2 second timeout. The packer takes 10, finishes 3, and its process stops. SQS reports 90 waiting and 7 in flight. Nothing is lost; the 7 are only hidden. When the timeout runs out they come back, 97 waiting, and a new packer drains the queue. Packed 100, lost 0, packed twice 0. SQS handed 7 orders out a second time. The queue outlived the process reading it.
Act six. Asked for a queue that holds at most 50 orders, SQS answers that it does not know the setting. Orders arrive at 15 a round and the packer does 10, for 20 rounds. SQS refused none, and 100 are waiting, and growing. Nothing warns you: the depth is a number you ask SQS for, and act on. Sending, taking and deleting 100 orders 10 to a request costs 30 requests; one at a time, 300. And because a taken order can come back, packing one twice must do no harm.
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

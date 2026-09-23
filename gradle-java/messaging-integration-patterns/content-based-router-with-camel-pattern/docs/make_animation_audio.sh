#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-6.m4a, for the Content-Based Router with Camel animation.
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
Act one. There is no router. All six orders are put on the warehouse's own queue, and the warehouse sorts out what it can. It ships the three physical ones and can do nothing with the other three: two gift cards and a subscription. So the warehouse grows an if for every kind of order.
Act two. A Camel route reads the orders queue and asks four questions in order: high value, digital, express, physical. The first yes decides. Order one goes to express shipping. Orders two and four go to digital delivery. Order three, worth twelve hundred pounds, goes to fraud review. Order six goes to standard shipping. Order five, the subscription, is claimed by no question and takes the otherwise branch to manual review.
Act three. One digital gift card, worth fifteen hundred pounds, goes through two routes with the same four questions in two orders. With the value question asked first, it goes to fraud review. With it asked last, the digital question says yes first, and it goes to digital delivery. Camel does not warn you when the order changes.
Act four. A subscription order, and every question says no. With an otherwise branch it lands in manual review. With no otherwise branch the route simply ends, tells the broker the order was handled, and the broker deletes it. Messages left anywhere in the shop: zero. With an otherwise branch named for the problem, it lands on a queue called unclaimed, where somebody can look at it.
Act five. A fifth question is added, for orders from the European Union, asked after the other four. No sender and no receiving queue is touched. An EU subscription that used to go to manual review now goes to the tax check. Order six, a parcel from the EU, still goes to standard shipping, because the physical question says yes first.
Act six. The bill. The sender calls parcels goods instead of physical, and order nine lands in manual review without a word. The fraud branch is broken: Camel tries it three times, then puts the order on the errors queue, which holds one. And there is something to run: one container, one exchange and ten queues.
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

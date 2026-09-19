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
Act one. Ten in stock, and two orders, for three and for four, read the stock at the same moment. It should be three left, and it is not. One of the two reservations was lost.
Act two. Four threads each send a thousand reservations to an inventory of four thousand. Stock left: zero. There is no lock in the inventory.
Act three. Reserving three of five is answered with a reserved message. Reserving three more is answered with an out of stock message, saying two are left. No exception crossed between the two.
Act four. The inventory actor has no public method that returns its stock. The only way to learn it is to ask, and the answer is a copy.
Act five. A message the actor cannot handle fails, the sender is told, and the actor is restarted. The next message is handled. One bad message did not stop the actor. The restart put the stock back to its starting value.
Act six. Two actors that each ask the other and wait for the answer never get one. There are no locks, and still a deadlock. A restart forgets state, messages are copied, mailboxes can grow, and finding where a message went takes tools.
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

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
Act one. Five services that each tell the other four when an order is placed need twenty wires between them, and every wire is an address that can be wrong or down. Add a sixth service and it needs ten more.
Act two. Checkout publishes an order placed event under the name store dot orders dot placed, and returns. It is told nothing about who was listening. Email, the warehouse and analytics each see the order. Five services with one connection each: five wires, not twenty.
Act three. Checkout publishes four events: an order placed, that order cancelled, a payment taken, and stock running low. A listener for the exact name gets one. A listener with a star, which stands for one part of the name, gets two. A listener with an arrow, which stands for the whole rest of the name, gets all four.
Act four. The email service's handler throws: the mail server timed out. The warehouse, on a connection of its own, still reserves the stock. Checkout is never told, because publishing had already returned before either of them ran.
Act five. Nobody is listening. Checkout publishes order ORD-1, and the bus drops it. No error, no record, and nowhere to read it back from. The warehouse then starts listening and checkout publishes ORD-2. The first event the warehouse ever receives is ORD-2, so ORD-1 was never coming. Telling this bus is never confirmed. Asking is: a request with nobody listening comes back at once, saying there are no responders.
Act six. Who reacts to an order being placed? Nothing in checkout says, and checkout cannot find out. Only the server knows, and it has to be asked on a second port: three listeners. Analytics stops listening but keeps its connection open: two. All three services close their connections: none, because closing a connection takes every listener on it. The bus is now a program of its own to run and to watch, and it keeps nothing, so a subscriber that is down has missed the event for good.
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

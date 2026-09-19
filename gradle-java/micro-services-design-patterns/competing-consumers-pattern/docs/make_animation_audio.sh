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
Act one. Six slow jobs: with one consumer, one is in progress and five wait. With three consumers, three are in progress and three wait. The consumers do not talk to each other.
Act two. A thousand orders and four consumers: handled a thousand times, and a thousand different orders. None twice, none missed.
Act three. Orders one, two and three are published in that order, but one's consumer is slow, so they finish as two, three, one. If order two depends on order one, that is a bug.
Act four. A consumer fails on the first attempt. The message is given back, and another attempt succeeds. It was not lost.
Act five. A consumer charges the card and crashes before saying it finished, so the message returns and the card is charged again: two charges. A consumer that remembers what it has done charges once.
Act six. Six consumers share a database that lets two in at a time. Two are inside, and four are waiting for a place, so four of six are doing nothing useful.
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

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
Act one. The picker asks again and again whether an order has come. Before any order arrives it has asked more than a million times, keeping a processor busy for nothing.
Act two. The picker's thread is waiting, using no processor, and has asked nothing. An order arrives, the picker is woken, and takes it.
Act three. Two pickers wait and one order arrives. With the guard checked by if, both wake, and one takes nothing. With while, the second picker looks again, finds nothing, and goes back to waiting.
Act four. The order was already there, and its notification came and went. A picker that waits without looking first sleeps, though the order is waiting. A picker that checks the guard first takes it at once.
Act five. With no order coming, the picker gives up after a hundred milliseconds and gets nothing. With an order there, it takes it at once.
Act six. Twenty pickers wait, and one order arrives. Notify all wakes all twenty, one takes it, and nineteen go back to sleep. And a thread waiting for something nobody will send waits forever.
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

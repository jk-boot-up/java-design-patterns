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
Act one. The query broke, and the code that would close the connection was after it. Connections still open: one. Repeat that on every failure, and the pool runs dry.
Act two. The same failure: the query broke. Connections opened: one. Still open: none. The closing is in one place, in a finally block, and cannot be forgotten.
Act three. A string came out: the rows for an order. A number came out: fifteen. Still open: none.
Act four. Two purchases of three thousand from a credit of five thousand: the second failed, with not enough credit. The balance afterwards is five thousand. The first purchase was undone too. One purchase of three thousand that works leaves two thousand.
Act five. Receipt sent, in five ticks. And a failing job: the mail server timed out, and it was still measured: nine ticks.
Act six. The caller let the connection out of the block, and used it later: connection one is closed. The block cannot stop that. The caller's code is now inside a lambda: it cannot return early, and it cannot throw a checked exception without help. And with two resources the blocks nest, one inside the other, so the real work drifts to the right.
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

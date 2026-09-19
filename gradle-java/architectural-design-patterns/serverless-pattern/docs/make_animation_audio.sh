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
Act one. One hundred ticks, three orders. The bill is two hundred. It was paid for a hundred ticks, and used for three orders.
Act two. The same three orders, each running a send receipt function. Three calls, and a bill of three. Between orders nothing runs, and nothing is paid for.
Act three. Before any order, no instances. Five orders at the same moment: five instances, five cold starts. Ten ticks later, with no orders: no instances again.
Act four. The extra wait: first call, five ticks. A call soon after, none. A call after a long quiet, five ticks. The first call after a quiet time is slow, because an instance must be started for it.
Act five. Two calls in a row: the instance remembers two, and the outside store two. After the quiet time: the instance remembers one, and the outside store three. What is kept in the function is gone. Anything that must last goes in a store outside.
Act six. In a hundred ticks, with three calls, functions cost three and the server two hundred. With three hundred calls, functions cost three hundred, and the server two hundred. Paying per call is cheap when quiet, and dear when busy all the time. And a job of twenty ticks against a limit of fifteen does not finish. Long work does not fit.
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

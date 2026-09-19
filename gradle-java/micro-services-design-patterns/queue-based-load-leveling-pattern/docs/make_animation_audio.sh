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
Act one. A hundred orders arrive at once and the service takes ten. Ninety are refused, on the busiest moment of the shop's day.
Act two. The same hundred orders, through a queue: all hundred are processed, none refused, and the worker never did more than ten a tick. The burst was spread over ten ticks.
Act three. The first order waited nothing. The last waited nine ticks. On average an order waited four and a half.
Act four. Fifteen arrive a tick and the worker does ten. An unbounded queue reaches five hundred waiting and keeps growing. A queue limited to fifty refuses four hundred and sixty, and no wait is longer than four ticks.
Act five. A worker of ten clears the burst with a longest wait of nine. A worker of twenty halves it to four. Serving the peak with no queue would need a worker of a hundred, idle almost all day.
Act six. The process holding an in-memory queue stops at tick three. Thirty orders were processed and seventy were waiting, and are lost, though the customers were told they were accepted.
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

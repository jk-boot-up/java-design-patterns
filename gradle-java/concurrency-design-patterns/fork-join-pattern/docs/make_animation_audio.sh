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
Act one. Adding up a hundred thousand order totals in a loop gives four hundred and ninety nine million eight hundred and thirty eight thousand pence, on one thread.
Act two. The job is split in halves until a piece is ten thousand or fewer. That gives sixteen pieces added directly and thirty one tasks in all, and the same total as the loop.
Act three. A pool of four workers, sixteen pieces, each held until four are running at once. The most running at the same moment is four.
Act four. With a threshold of a hundred thousand there is one piece, which is just the loop. Ten thousand gives sixteen, a hundred gives a thousand and twenty four, and one gives a hundred thousand pieces and nearly two hundred thousand tasks, which is mostly the cost of making tasks.
Act five. Four equal pieces could give four times the speed. If one piece costs eighty five and the others five each, the best possible speedup is one point one eight, because the job waits for the big piece.
Act six. A pool of two workers and eight pieces that each wait on something slow run only two at once, so six pieces wait. Fork-join is for work that uses the processor. And splitting twenty items to single items makes thirty nine tasks to add up twenty numbers.
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

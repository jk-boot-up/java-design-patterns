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
Act one. In the earlier project's price units, a server costs two a tick. A hundred ticks with three orders costs two hundred. It was paid for a hundred ticks, and used for three orders.
Act two. The function is uploaded to a real Lambda API, and run for each of three orders. Three receipts are sent, and the bill at one per call is three. Between orders nothing has to be running, and nothing is paid for.
Act three. Before any order, no copies are running. Five orders at the same moment: five distinct copies answered, and five containers are running. Five quiet seconds later, with no orders: none are running.
Act four. The first call after a quiet time took several hundred milliseconds, and the call right after it, a few. The cold call was slower. The first call had to start a container for the function, and the second found it running.
Act five. A call to the copy that is running: it has handled three calls. After the quiet time, a different copy answers, and it has handled one. What the first copy kept in its variables went with it. Anything that must last goes in a store outside.
Act six. In the earlier project's price units, in a hundred ticks, with three calls, functions cost three and the server two hundred. With three hundred calls, functions cost three hundred, and the server two hundred. Paying per call is cheap when quiet, and dear when busy all the time. And a job that needs six seconds, with a limit of three, fails: the platform says the task timed out.
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

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
Act one. The supplier never answers, and the product page's thread waits, with no limit on for how long. The customer is looking at a spinner.
Act two. With a limit of a hundred milliseconds, the page shows stock unknown, try again shortly, and loads without the number it could not get.
Act three. The caller gave up, but the call at the supplier had only started. Later the supplier finishes it anyway, with nobody waiting.
Act four. On a typical hundred calls, a limit of fifty milliseconds lets fifty four succeed, a hundred lets ninety, and only three seconds lets all one hundred. Too tight fails healthy calls. Too loose holds a thread for seconds.
Act five. Three calls in a row, each allowed a second, could take three seconds. One budget of a second shared by all three answers the first, cuts off the second, and skips the third, for one second in total.
Act six. A payment call times out, and the customer is told it failed. The provider then completes the charge anyway. A timeout says only that you stopped waiting.
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

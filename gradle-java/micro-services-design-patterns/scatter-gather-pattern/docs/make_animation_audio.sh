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
Act one. Four suppliers answer in eighty, a hundred and twenty, two hundred and nine hundred milliseconds. Asked in turn, the page waits thirteen hundred.
Act two. Asked together, the same four make the page wait for the slowest: nine hundred milliseconds.
Act three. All four suppliers are being asked at the same moment. With a deadline of five hundred milliseconds, three quotes are gathered and Delta, too slow, is left out. The best of three is shown, and the page waits five hundred, not nine hundred.
Act four. The page shows the best of two of three suppliers. The one that did not answer, Delta, would have been cheaper, at nine ninety. A partial answer is honest only if it says it is partial.
Act five. Beta is down. The page gets the other two quotes, and names Beta as missing, with the reason. One failure did not fail the page.
Act six. One page view becomes four supplier calls, so a thousand views make four thousand. And if each supplier is quick ninety nine times in a hundred, asking four and waiting for all means only ninety six pages in a hundred are quick, and with ten suppliers, ninety.
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

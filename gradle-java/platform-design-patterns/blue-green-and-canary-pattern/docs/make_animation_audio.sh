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
Act one. Stop version one, install version two, start version two. Ten requests arrive while it is down. Of a hundred requests, ten failed.
Act two. Version two is started beside version one, and tried with a test order. It is fine. Version one served fifty requests meanwhile. The switch is one setting. After it, version two serves the next fifty. Of a hundred requests, none failed.
Act three. Version two has a bug with big orders. Fifty requests on version two, five failed. One setting sends traffic back to version one, which was never stopped. The next fifty requests, none failed.
Act four. Five percent of traffic goes to the buggy version two. Of two hundred requests, version two got ten, and failed two. Had all two hundred gone to version two, twenty would have failed. A few customers found the bug, not everyone.
Act five. Steps of five, twenty five, fifty and a hundred percent, with a gate at five percent failures. The buggy version two is halted after one step, with twenty percent failing, and traffic goes back to version one. The good version two goes through all four steps, and ends at a hundred percent.
Act six. Two full copies run during the switch: capacity twenty instead of ten. And version two wrote five orders in a new format before we went back. Version one can read none of them. Both releases share one database, so a release that changes the data cannot be switched back safely.
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

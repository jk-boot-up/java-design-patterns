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
Act one. Gift wrap goes live by deploying it: one deploy. It has a bug, so taking it away is another: two deploys. Each deploy ships every other change waiting in the branch too.
Act two. Gift wrap is in the deployed code, and flagd has it off. An order of five thousand costs five thousand. The flags file is edited, and flagd notices by itself: no deploy, no restart. The same order costs fifty three hundred.
Act three. A ten percent rollout, decided by flagd's own hash of the customer. Of a hundred customers, about a tenth got it. Then only two named testers: of a hundred customers, two got it.
Act four. Gift wrap has a bug. With twenty percent on, about a fifth of a hundred orders failed. One edit to the file turned it off. Of a hundred orders, none failed. No deploy.
Act five. Flagd is up, and an order of five thousand costs fifty three hundred. Flagd is stopped, and it costs five thousand. The order still works, and every feature falls back to off.
Act six. A shop with five flags would have thirty two possible combinations. The tests usually run one. Flagd is another process to run and keep up, and every flag check is a network call: this demo made hundreds. And a flag that is settled and still in the file is an if that nobody needs. Flagd does not remove it for you.
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

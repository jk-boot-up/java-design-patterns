#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-7.m4a
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
Act one. Twelve pick orders are waiting, and one picker takes them one at a time. One is being picked and eleven wait. Put three pickers on the same queue and three are being picked, nine wait. Then three pickers share three hundred orders. All three hundred are picked, each a different order. Every picker did some, and none did more than half. The exact split is the broker's choice, and it changes from run to run.
Act two. Twelve orders are waiting. A slow picker starts first, and nobody has set a limit on how many orders it may hold. RabbitMQ calls that limit prefetch, and its default is no limit. So the broker hands the slow picker all twelve at once, and nothing is left waiting. A fast picker joins a moment later and is handed nothing. It stands idle while the slow picker works through all twelve.
Act three. The same slow and fast pickers, now with a limit. With a prefetch of ten, and twenty orders, each is handed ten. The fast one picks its ten and then stands idle with the queue empty, while the slow one still holds ten. With a prefetch of one, the slow picker holds one, and the fast one picks the other nineteen.
Act four. Picker A may hold five, and is handed five. It picks orders one and two and says done for each. It reserves the stock for order three, and then it crashes before saying done. The broker puts back every order it handed over and never heard done for: three of them. Picker B is handed orders three, four and five, and all three are marked as seen before, though only order three had been started. Eight deliveries for five orders, and order three's stock reserved twice.
Act five. The same crash, but picker A told the broker to count each order as done the moment it is handed over. RabbitMQ calls that automatic acknowledgement. The queue is already empty before the crash. Picker A picks two and crashes on order three. Nothing goes back. Three orders are lost.
Act six, the bill. Order thirteen crashes every picker that takes it. Three pickers, three deliveries, marked as seen before on two, picked none, and it is waiting again. The broker cannot tell a poison order from a slow one. Every picker must be safe to run twice. And prefetch is a number somebody has to choose, because left unset, one picker took twelve of twelve while another stood idle.
EOF
}

i=0
while IFS= read -r line <&3; do
    i=$((i + 1))
    printf '%s' "$line" > "$OUT/.step-$i.txt"
    say -v "$VOICE" -r "$RATE" -o "$OUT/.step-$i.aiff" -f "$OUT/.step-$i.txt"
    ffmpeg -y -loglevel error -i "$OUT/.step-$i.aiff" \
        -af "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11" \
        -c:a aac -b:a 128k -ar 44100 -ac 1 "$OUT/step-$i.m4a"
    rm -f "$OUT/.step-$i.aiff" "$OUT/.step-$i.txt"
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/step-$i.m4a")
    printf 'step-%d.m4a  %5.1fs\n' "$i" "$dur"
done 3< <(narrate)

echo
echo "Wrote $i clips to $OUT/"

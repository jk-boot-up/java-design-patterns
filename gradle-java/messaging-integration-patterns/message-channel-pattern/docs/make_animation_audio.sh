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
Act one. With the warehouse down, three orders are placed and all three checkouts fail. The shop cannot sell while another system is away, though selling does not need it to answer yet.
Act two. Checkout sends three messages and carries on. The warehouse then takes them, each once, in order.
Act three. The warehouse is down, and checkout sends three messages, and none fail. When the warehouse comes back, it works through them in order.
Act four. A message has headers, such as priority and correlation, that can be read without opening the body. A router or receiver can decide from the envelope alone.
Act five. The pick orders channel refuses a refund request. A receiver never has to ask what kind of message it was given.
Act six. If the warehouse stays down, a channel of five fills, and three more are refused. The sender no longer learns whether the order was picked, only that the message was accepted. Sent five, received none.
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

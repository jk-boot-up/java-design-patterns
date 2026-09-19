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
Act one. The order code saves the order, reserves stock, then sends the email, which fails. The order is saved and stock reserved, but the caller is told it failed, and analytics never counts it.
Act two. Placing the order records one event, order placed, with the id, the customer and the total. Asking again returns nothing, because the events were handed over.
Act three. Saving the order keeps its event, and nothing reacts yet. A relay then delivers the event to stock, email and analytics, in turn.
Act four. With the mail server down, only the email reaction fails. Stock and analytics still run. The event waits for email alone, and when the server is back the next relay sends just that one.
Act five. Placing and then cancelling records two events, in that order. Each is a record with the data in it, and no reference to the order.
Act six. If the process stops after the save and before the relay, nothing has reacted, but the event was saved with the order. After a restart the relay delivers it, and nothing is lost.
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

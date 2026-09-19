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
Act one. Gift wrap is asked for, and the checkout does not support it. The total is unchanged. To add it, edit the checkout, test all of it again, and release all of it.
Act two. The core has two plugins, member discount and shipping fee. A total of ten thousand becomes ninety five hundred. The core knows one interface, and nothing about discounts or fees.
Act three. Gift wrap is registered while the system is running. It is started, and the total is ninety eight hundred. Then it is taken away again, stopped, and the total goes back to ninety five hundred. The core was not changed.
Act four. The loyalty points plugin throws an error. The core records it, and carries on. The other plugins still ran, and the total is ninety five hundred.
Act five. Discount then fee gives ninety five hundred. Fee then discount gives ninety four fifty. The same two plugins, a different price. The core cannot know which is right.
Act six. The interface offers one thing: adjust a total. Plugins want more: the customer's country, and a line on the receipt. If the interface grows, every plugin feels it. If it does not, plugins reach around the core. And a customer's total is now decided by whichever plugins are installed, in some order.
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

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
Act one. The order service calls inventory, email and analytics, each by name, and each handles order one. It works, but the order service now knows three services by name, and a fourth, loyalty points, means editing it.
Act two. Redis is running in a container. Inventory, email and analytics each subscribe on a connection of their own. The order service publishes order one once, and Redis answers three receivers. Then loyalty points starts as a second Java process. Order two is published, Redis answers four, and the loyalty process prints order two and exits cleanly. The order service was not changed.
Act three. Only email is listening, and three orders are published. Redis answers one, one and one. Loyalty starts listening, and order four is published to two receivers. Email saw all four orders. Loyalty saw only order four. Redis stored none of them: the number of keys in its database is zero.
Act four. Email subscribes to the exact name orders dot placed. Analytics subscribes to orders dot star, which matches every name starting with orders. A placed order reaches two receivers. A cancelled order reaches one. Email got the placed order, and analytics got both.
Act five. Redis keeps a pile of unread messages for each listener, with a limit. Out of the box it is thirty two megabytes, or eight megabytes for sixty seconds. The demo lowers it to one megabyte. Analytics stops reading, and orders go out in rounds of one thousand until Redis acts. More than ten thousand orders later, Redis cuts analytics off, and its counter of listeners cut off reads one. The first order reached two receivers, the last reached one. Email received every one. Analytics got some of them, not all, and the rest are gone.
Act six. Email is down when order one is placed, and Redis tells the order service zero receivers. When email comes back it gets nothing, because there is nothing to catch up from. The count says how many connections were listening, not which ones, and not whether any finished the work. And Redis is a separate program to run: one container and two Java processes.
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

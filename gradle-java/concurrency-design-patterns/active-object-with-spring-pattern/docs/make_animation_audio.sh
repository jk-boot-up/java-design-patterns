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
Act one. Four callers send five thousand restocks each. The total is exactly twenty thousand. The stock is a plain int with no lock, because one thread owns it.
Act two. The worker is busy, and callers send ten thousand messages. All wait, none is refused. With a mailbox of three, the fourth waiting message is refused.
Act three. The worker has read the stock and is holding it. A caller adds five through this, on its own thread. The worker then writes zero plus ten. Final stock: ten, not fifteen.
Act four. A restock of five is waiting behind a slow message. A direct getter says zero. A read sent as a message, behind the restock, says five.
Act five. A failing message fails its future, later. The stack belongs to the inventory thread, and the calling method appears nowhere in it.
Act six. Every message costs fifty microseconds of work. One caller and four callers get the same rate, about nineteen thousand a second. The ceiling is the worker.
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

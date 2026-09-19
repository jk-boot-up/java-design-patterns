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
Act one. Clerk A takes the lock. Clerk B asks and is refused, told that A holds it. B never starts an edit that could be lost.
Act two. A raises the price and lets go. B then takes the lock, reads the new price, and saves the stock count on top of it. Nothing is overwritten.
Act three. While A edits, B tries once a minute and is refused three times, and has done nothing useful in that time.
Act four. A goes to lunch without letting go. B is refused at once, and again after ten minutes. After sixteen minutes the lock expires and B gets it. When A comes back, A's save is refused.
Act five. A holds the mug and needs the tea. B holds the tea and needs the mug. Neither can move. If everyone takes locks in the same order, one gets both, and the other holds nothing and waits.
Act six. One lock on the whole catalogue stops B editing a different product. A lock per product lets both work. Smaller locks mean less waiting, and more locks to forget or deadlock on.
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

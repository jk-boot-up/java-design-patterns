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
Act one. Both clerks read the same row. Clerk A saves a new price. Clerk B saves the stock count, and writes the whole row, with the old price. The price change is gone, with no error.
Act two. Clerk A saves and the row moves to version two. Clerk B's save, made against version one, is refused, and the price of twelve pounds survives.
Act three. Clerk B reloads the row, sees the new price, reapplies the stock count and saves. It takes two attempts, and both changes survive.
Act four. One clerk changed the price and another the stock. Different fields, but the second save is refused, because the version is per row.
Act five. Ten clerks add one to the same row. Nothing is lost and the stock is ten, but nineteen saves were attempted and nine refused, so nine of the ten did their work twice.
Act six. A user makes five changes over a long session, and on saving is told the row changed. All five changes are discarded, and the user learns it only now.
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

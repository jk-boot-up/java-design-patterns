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
Act one. One edit, and the autosave timer fires five times: five writes. Four of them wrote exactly what was already there.
Act two. The same five calls give saved once and nothing to save four times. One write.
Act three. A save is in progress, held in the write. A second call arrives and is told already saving, at once, without waiting. Only one write happens.
Act four. The customer changes two to three while a save runs. A draft that marks itself clean when the save ends loses the change. One with a version counter stays dirty, and the next save writes three.
Act five. Nothing edited gives nothing to save. Edited gives saved. A balk is an answer, not an error, so the caller can retry, ignore it, or tell the user.
Act six. The customer clicks Save while the autosave runs, and is told already saving. Their click did nothing, and their change waits for the next save. Balking is wrong where every request must be honoured.
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

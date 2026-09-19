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
Act one. One loop does five jobs. Six lines go in and three come out, and the three that were dropped left no trace of why.
Act two. The same job is five steps: parse, validate, price, tax, format. The price step on its own turns one parsed line into a priced one, with no need for the others.
Act three. Swapping the UK tax step for an EU one changes the total from nineteen twenty to nineteen thirty six. A new step is added in the middle, and no other step changed.
Act four. Three lines pass. Three are rejected, each with the step that dropped it and the reason, and the good lines carry on.
Act five. With ten thousand lines, streaming holds one item at once and running one stage at a time holds twenty thousand. The results are the same.
Act six. Steps that pass loose maps fail at run time when one calls a field qty and the next asks for quantity. Typed items catch that when compiling, but every step depends on the type before it. And an error appears in the step that noticed, not the one that caused it.
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

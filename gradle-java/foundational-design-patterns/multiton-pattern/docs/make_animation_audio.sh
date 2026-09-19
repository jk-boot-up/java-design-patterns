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
Act one. Two callers each made a UK warehouse. They are not the same object. One has stock ninety, the other a hundred. The shop now believes two different things about one warehouse.
Act two. Asked for the UK twice, it is the same object. Asked for the EU, it is a different one. Created so far: two.
Act three. One part of the shop reserved ten in the UK. Another part, asking for the UK, sees stock ninety. The EU warehouse has a hundred.
Act four. Asked for Mars, it is refused: no warehouse in Mars. Instances held: three.
Act five. Look first, create second, with no lock: both threads looked before either created. Not the same object, and two were created. With an atomic create if absent, eight threads at once get the same object, and one is created.
Act six. One test reserved thirty. The next test starts, and asks for the UK: stock seventy, not a hundred. State leaks from one test to the next. The instances live as long as the program does, and nothing ever lets one go. And any code can reach any warehouse from anywhere, so who changed the stock is hard to say.
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

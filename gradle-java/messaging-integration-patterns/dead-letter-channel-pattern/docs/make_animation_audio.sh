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
Act one. Four orders, one garbled. Only the first is handled. The garbled one is tried ten times and never succeeds, and orders three and four are stuck behind it.
Act two. After three attempts the garbled order is moved aside. Orders one, three and four are handled, nothing is waiting, and there is one dead letter.
Act three. The dead letter records the order, three attempts, the last error, and the channel it came from. The original message is kept exactly, so it can be looked at, and put back.
Act four. Order three fails once on a timeout and succeeds on the second try, so it is not dead-lettered. Only order two, which fails every time, is.
Act five. The parser is fixed and the dead letter is replayed. Order two is now handled, after three and four, and the dead letters are empty. Replay does not restore the original order.
Act six. Forty orders, half garbled: twenty dead letters, each an order a customer was told was accepted. The main channel looks healthy, with nothing waiting, and nothing tells anyone to look.
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

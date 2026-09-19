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
Act one. Three methods each take a customer they never use, so that the last can log it. Every new layer, and every new caller, has to pass it on.
Act two. The customer is set once at the door, and checkout, price and stock take no customer, yet the log says ada. After the request the context is cleared.
Act three. Two customers are handled at the same moment, both contexts set before either is read. Each log line names its own customer. They share the code and the static field, and not the value.
Act four. Request A sets ada and forgets to clear it. Request B, an anonymous visitor, runs next on the same pool thread, and is logged as ada. With the clear in a finally block, B is logged as nobody.
Act five. Ada's request hands the work to another thread, and the log says null. A thread created by ada's thread can inherit a copy, but a pool thread is created once and reused, so it does not have the current request's. Handing work on means handing the context on.
Act six. A method that reads the context has a dependency its signature does not show, and with none set it logs null. Every test has to set and clear the context. And a pool thread keeps what is left in it for as long as it lives.
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

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
Act one. The orders handler has no sign-in check, so a visitor who is not signed in receives ada's orders. The account handler checks, but logs only what it accepts, so neither request is logged.
Act two. Through the front controller, orders without a sign in is refused, and orders with one is served. Products, listed as public, needs neither. The check is written once.
Act three. An unknown page gets a four oh four and a wrong method a four oh five, both from the routing table, in one place.
Act four. The log has all three requests, including the refused one and the missing page, because logging is a filter that runs first.
Act five. A handler throws an error whose message contains a password. The customer sees a plain five hundred. The detail goes to the log only.
Act six. One filter with a bug in it makes every page return a five hundred at once. The front controller is the one place everything depends on.
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

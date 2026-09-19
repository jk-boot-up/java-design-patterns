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
Act one. The search can serve a hundred a second. A client sends a thousand, all are accepted, and nine hundred are beyond capacity, so everyone else waits behind them.
Act two. A bucket of ten, refilled at five a second, allows ten of a burst of twenty. A second later it allows five. After ten quiet seconds it is full again, and no fuller.
Act three. Five requests a second, evenly spaced, for a whole minute, are all allowed: three hundred of three hundred. A burst is tolerated up to the size of the bucket, and a sustained rate above the refill is not.
Act four. With one shared bucket, a greedy client takes all ten tokens and a polite client is refused. With a bucket each, the greedy client is held to ten, and the polite client is allowed.
Act five. An empty bucket refuses and says to retry after a thousand milliseconds. One millisecond early is refused, and at the stated moment the request is allowed.
Act six. Three servers each with their own bucket allow thirty, three times the limit. Ten thousand callers mean ten thousand buckets. And a real page that loads twelve things at once gets only ten.
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

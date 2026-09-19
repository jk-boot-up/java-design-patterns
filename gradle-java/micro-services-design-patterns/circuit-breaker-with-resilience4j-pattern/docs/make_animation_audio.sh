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
Act one. A healthy call passes through the closed breaker. One call reaches the service.
Act two. The service goes down. The window holds the last four calls, and the healthy one from act one is still in it. At the third failure the breaker opens, and the fourth call never reaches the service.
Act three. A hundred more page views send nothing to the service. The breaker refuses each one, and the fallback answers.
Act four. Half-open lets one call through. While the service is down the probe fails and the breaker opens again. Once the service is back, the probe succeeds and the breaker closes.
Act five. Bad requests for a product that does not exist are the caller's fault. One breaker ignores them and stays closed. The other counts them, and opens.
Act six. A method that calls its own protected method on this skips the proxy. All ten errors reach the caller, all ten calls reach the service, and the breaker never notices.
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

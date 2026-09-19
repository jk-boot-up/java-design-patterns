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
Act one. The locator asks Consul for the healthy payment gateways and gets two. Four orders are shared two and two. The checkout never knew an address.
Act two. Gateway-1's check fails, and all four orders go to gateway-2. It recovers and is used again. The checkout's code did not change.
Act three. A typo compiles and fails at run time. A lost notifier registration is found only after the customer was charged.
Act four. A caching locator remembers an address. The instance dies, and the cache still hands it out. The call fails. Consul was asked once. Faster, and wrong.
Act five. nginx in a Docker container is given the healthy instances once. The caller asks nothing. When an instance dies, nginx retries the next. Four of four still succeed.
Act six. Discovery is the strongest case for a locator. Even so, prefer to be given an address by the platform than to have every class ask.
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

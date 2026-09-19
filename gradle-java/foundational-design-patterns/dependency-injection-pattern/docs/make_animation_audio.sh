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
Act one. CheckoutService takes a discount policy, a payment gateway and a notifier. That is everything it needs, and the compiler checks it. It never looks anything up.
Act two. The whole application is built in nine lines of plain Java, in one place. A container is an optimisation of something you can write yourself.
Act three. Setter injection suits an optional collaborator. Field injection lets you build an invalid object, and needs reflection to fix it. Recommend constructor injection.
Act four. Eighty-six lines, written here. It reads constructor parameter types and builds the same graph as the hand wiring.
Act five. A missing bean, or a circular dependency, fails when the container starts. Better than a locator's first request, still not compile time.
Act six. Registry put things in a known place. Service Locator made a middleman. Dependency Injection stopped the asking. Constructor injection, by hand until it hurts.
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

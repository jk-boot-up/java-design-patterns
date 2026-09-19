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
Act one. Five components that each tell each other about orders need twenty references between them. A sixth needs ten more.
Act two. One post reaches inventory, email and analytics. Five components each hold one reference, to the bus: five references, not twenty. The poster holds no reference to any subscriber.
Act three. A subscriber for order placed hears only that. A subscriber for every order event hears both the placed and the cancelled.
Act four. Email fails, and analytics still hears the event. The failure is recorded. The poster does not see it: it posted, and carried on.
Act five. With no subscriber, an event is counted as dead, and nothing complains. With a subscriber for dead events, the unheard event arrives there.
Act six. Nothing in the code that posts an event says who reacts to it, though the bus can be asked. A thousand short-lived subscribers that never cancel are all still held. Cancelling leaves none. And a slow subscriber holds up the poster.
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

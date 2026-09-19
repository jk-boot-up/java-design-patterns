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
Act one. Every order gets a brand new thread, the same failure section forty-six measured, now seen from the packing team's side. Nothing caps how many pile up.
Act two. Two workers, genuinely bounded. What they pull from is not: an unbounded queue, built in behind the factory method, with no argument anywhere to change it.
Act three. One worker, a queue capacity of three, both chosen on purpose. A fourth order is refused on the spot, because the pool has no patience window built in.
Act four. Sizing is a real decision. Too few workers, and act two's backlog happens. Too many, and each one is a stack held open for nothing.
Act five. A task submits a second task to its own pool, then waits for it. With one worker, and that worker the one waiting, the second task can never run.
Act six. Virtual threads make act one's number nearly disappear. They change nothing about act three: a pool still bounds a resource, not a thread count.
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

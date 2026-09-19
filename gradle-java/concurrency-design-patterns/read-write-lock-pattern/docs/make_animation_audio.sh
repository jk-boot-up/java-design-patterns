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
Act one. With no lock, a reader lands between the writer's two steps. It sees the new amount with the old currency -- a price that never existed.
Act two. One lock around everything is correct. But two readers can never conflict, and this lock cannot tell them apart, so every reader queues behind every other reader.
Act three. Many readers now hold the lock together, and only a writer excludes everyone. Yet for a read this cheap, it is slower than the plain mutex.
Act four. A writer is genuinely queued, waiting. A reader that arrives later still slips past it. Nothing bounds how long the writer waits.
Act five. A thread holding the read lock asks for the write lock. The write lock waits for every reader to leave, including this thread. It waits on itself, forever.
Act six. Against a plain mutex and an immutable snapshot, the lock advertised for readers is the slowest. The snapshot needs no lock, and no readers to coordinate.
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

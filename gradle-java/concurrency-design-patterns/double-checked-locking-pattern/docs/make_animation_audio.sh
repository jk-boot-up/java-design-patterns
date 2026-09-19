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
Act one. Two threads ask together, and both see that the price list does not exist, so both build one. Two are built, and each thread holds a different one.
Act two. With the lock on every call, only one is built. But a thousand calls, long after it was built, take the lock a thousand times.
Act three. The same race builds one. The second thread waited for the lock, looked again, and found it built. A thousand calls take the lock once, and after that no call waits for anyone.
Act four. The field is volatile. Without it, the memory model lets one thread see the reference before it sees the object fully built. That failure cannot be produced on demand, so a test guards the rule.
Act five. Nothing is built before anyone asks. After two calls, one is built, and both calls get it. The JVM builds a class's static state once, when it is first used, so there is no lock and no volatile to write.
Act six. The double-checked version is twenty nine lines and the holder ten. Double-checked locking is ceremony with one way to be subtly wrong. It earns its place only where the holder cannot be used, for example when creation needs an argument. An uncontended lock is cheap.
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

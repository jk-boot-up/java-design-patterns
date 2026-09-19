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
Act one. Three lookups on the default pool are all in flight at once. On a pool of one thread, only one is. The annotation asked for concurrency and the pool decided.
Act two. A method returning a future carries its exception to the caller, with a trace that belongs to the pool thread. A void method's exception goes to nobody, only to a handler you must register.
Act three. The caller is working for customer seven. The async method asks whose order it is, and the answer is null. A task decorator that copies it across fixes it.
Act four. The caller waits two hundred milliseconds and gets a timeout. The task had not finished. Then it runs to the end anyway, and nobody is waiting.
Act five. cancel true reports true, and the future says cancelled. But the task ran to completion anyway. The thread was never told.
Act six. Three futures combine into a page with no blocking until the end. If the review service is down, one fallback at that step keeps the page. Without it, one failing lookup fails everything.
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

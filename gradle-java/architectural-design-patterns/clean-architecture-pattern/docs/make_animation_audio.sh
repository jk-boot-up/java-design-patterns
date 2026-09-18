#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-5.m4a
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
Act one. A class calling itself a use case is constructed with three concrete gateway types directly, not boundaries. It works, and it reaches straight out, skipping the boundary ring entirely.
Act two. A controller calls the use case's own boundary interface. The use case speaks only to interfaces it declared, and main wired four gateways to it by hand, with no container anywhere.
Act three. Save order sends control outward, to whichever gateway was wired in. The dependency, the type it is, points inward, at an interface the use case owns. Two directions, disagreeing on purpose.
Act four. A batch controller and a file-backed repository are added at the same time. Both depend on exactly what already existed. The use case box does not even flicker.
Act five. Source code dependencies point only inward. Widened to include the naive package, the rule goes red and names the class that broke it.
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

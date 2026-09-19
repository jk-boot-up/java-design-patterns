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
Act one. The order saved itself with a SQL statement. To change the storage, the order class, at the centre, must be edited.
Act two. Ring zero is the order, the order line, and the idea of a repository. Ring one is the pricing rules. Ring two is the use cases. Ring three is storage and screens. The rule: a class may refer to its own ring, or to a ring further in, never outward. Among the eight classes of the onion, violations: none.
Act three. The checker is pointed at the naive order. It reports: the naive order, in ring zero, refers to the SQL database, in ring three. The checker reads the fields, constructors and methods of each class, so the rule is tested, not just hoped for.
Act four. Stored in memory, the total is ten thousand eight hundred. Stored as a text record, the same. The record is the order id, the mug, two at sixty pounds, and a discount of twelve hundred. The use case, the rules and the order were not touched.
Act five. A small order is nine fifty. A big order is ten thousand eight hundred, ten percent off twelve thousand. No storage, no screen and no framework was used to check the rules. Through the outside, the same order gives the same total.
Act six. One order saved and read back through the outer ring costs two conversions. Every trip across a ring may copy the order into another shape. To place one order there are four classes in three rings, plus the repository idea. For a small program, that is a lot of ceremony. And the repository idea lives in the centre, so the centre knows that storage exists, though not how.
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

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
Act one. Three kinds, three classes, and they differ only in three numbers. A novel totals thirteen hundred. A gift card is a fourth kind. That is a fourth class, a new build, and a release.
Act two. One product class. A novel totals thirteen hundred, a laptop ninety six thousand, tea six twenty. Laptops can be returned after ten days, but not after twenty.
Act three. Types before: three. After: four. Classes added: none. A twenty five pound card totals twenty five hundred, and cannot be returned after one day.
Act four. Tax on tea is twenty, on coffee forty. Grocery tax is raised to ten percent, in one place. Tea is now forty, and coffee eighty.
Act five. An ebook states only its shipping: none. Its tax, zero, and its return days, thirty, come from book.
Act six. A typo, b o k, is found when the program runs. With a class for each kind, the typo would not compile. Laptops need a serial number checked, and a type holds data, not steps. A flag says so, but the code that checks it is still somewhere else. And every new difference between kinds is a new field, that the code must remember to read. The type has six fields already.
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

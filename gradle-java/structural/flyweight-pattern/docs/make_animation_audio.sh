#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice used in the
# teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-7.m4a
#
# Requirements: macOS (for `say`) and ffmpeg.
#
set -euo pipefail

cd "$(dirname "$0")"

OUT=audio
VOICE="${VOICE:-Samantha}"     # female US English voice, matches the video
RATE="${RATE:-165}"            # words per minute

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

# Narration for each step. Kept in the same order as STEPS in animation.html.
# These are spoken versions of the on-screen text, with a little more warmth
# and the key takeaway spelled out.
narrate() {
cat <<'EOF'
Listing L S T dash 1002 asks the factory for a SALE style. The cache is empty for SALE, so BadgeStyleFactory builds a brand new BadgeStyle, complete with its icon, its colours, and its artwork, and it caches that instance for next time.
The shared style now renders itself for this one listing, using L S T dash 1002's own id and no custom label. Notice that nothing about this particular listing gets stored on the style object itself.
A second listing, L S T dash 1003, also wants a SALE badge. This time the factory finds SALE already sitting in the cache, and it hands back the exact same BadgeStyle instance. No construction happens at all.
The very same BadgeStyle object renders again, this time with a different listing id and a custom label. styleFor SALE equals styleFor SALE is true. One object just served two completely different callers.
Now look at the naive path. NaiveListingBadge skips the factory entirely. Building one for L S T dash 1002 means rebuilding the icon, the colours, and the full sixty four kilobyte artwork completely from scratch.
Listing L S T dash 1003 needs an identical SALE design, so NaiveListingBadge pays that same full construction cost a second time. naive A equals naive B is false. Two SALE badges, two completely independent copies.
Now stretch this across a hundred thousand listings. The naive path pays that price for every single listing. The flyweight path only pays for every distinct badge type, four instead of a hundred thousand, and that is the entire savings in one sentence.
EOF
}

i=0
while IFS= read -r line; do
    i=$((i + 1))
    printf '%s' "$line" > "$OUT/.step-$i.txt"
    say -v "$VOICE" -r "$RATE" -o "$OUT/.step-$i.aiff" -f "$OUT/.step-$i.txt"
    ffmpeg -y -loglevel error -i "$OUT/.step-$i.aiff" \
        -c:a aac -b:a 128k -ar 44100 -ac 1 "$OUT/step-$i.m4a"
    rm -f "$OUT/.step-$i.aiff" "$OUT/.step-$i.txt"
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/step-$i.m4a")
    printf 'step-%d.m4a  %5.1fs\n' "$i" "$dur"
done < <(narrate)

echo
echo "Wrote $i clips to $OUT/"

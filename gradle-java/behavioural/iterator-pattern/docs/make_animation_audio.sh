#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-12.m4a
#
# Requirements: macOS (for `say`) and ffmpeg.
#
set -euo pipefail

cd "$(dirname "$0")"

OUT=audio
VOICE="${VOICE:-Samantha}"     # female US English voice, matches the video
RATE="${RATE:-145}"            # words per minute, the series standard

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

# Narration for each step. Kept in the same order as STEPS in animation.html.
# These are spoken versions of the on-screen text: numbers are written out,
# class names are spaced so the voice does not run them together, and the key
# takeaway is spelled out a little more plainly than the caption does.
narrate() {
cat <<'EOF'
Eight products live in the warehouse system, and it will only hand them over three at a time. You ask for page zero, then page one, and you know you have finished when a page comes back empty. There is no size, and no has more pages. This is the shape the pattern exists to hide.
For each product in catalogue. That is the entire call site. No page number, no stop condition, nothing to get wrong. Everything you are about to watch happens underneath this one line.
This is what the compiler does with that line. It calls iterator once, and gets back a fresh bookmark. Look at the pages. Not one has been fetched. Asking for an iterator costs nothing.
The loop asks: is there anything there? To answer, the iterator has to look, so it fetches page zero. This is the laziness the tests assert. The fetch happens on the first has next, not when the iterator was created.
The cotton t-shirt, twelve pounds. The iterator moves its own position along by one. Notice that the catalogue was not involved at all. It has dropped out of the conversation, and every message from here goes to the bookmark.
The socks, four pounds, the cheapest thing in the shop. Two products have come out, and exactly one page has been fetched. If the customer stops looking now, the warehouse is never asked for anything else.
Look at the bookmark. Page zero, item two. That is the whole state of the walk, and every bit of it is on the iterator. The catalogue holds what is in it, and nothing about who is reading. Get this split wrong and two readers share one bookmark.
The wool scarf, eighteen pounds. Page zero is now used up, and the loop is about to ask has next again. What happens next is the only interesting moment in the whole pattern.
Has next sees it has run off the end of page zero, so it fetches page one and says yes. The loop asked one question and got one answer. It has no idea a page boundary was just crossed, and that is precisely the point.
Lamp, mug, cushion, then page two brings the novel and the cookbook. Eight products, in order, out of a source that never once offered you all eight.
Has next fetches page three, gets an empty list, and returns false. The for each loop ends. Translating that empty page into a plain no is work the caller used to do by hand, in three different places, and got wrong in two of them.
Ask the catalogue for a second iterator and you get a second, independent position. One reader can be on page two while the other is still on page zero, because neither of them is stored on the book. That is what makes a loop inside a loop over the same catalogue simply work.
EOF
}

i=0
# The narration is read on file descriptor 3, not stdin. `say`, `ffmpeg` and
# `ffprobe` all read stdin when it is available, and one of them will happily
# swallow the first character of the next line if the loop feeds them from it.
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

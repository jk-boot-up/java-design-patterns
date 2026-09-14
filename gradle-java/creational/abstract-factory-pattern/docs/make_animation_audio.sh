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
Our checkout service is handed a British market factory, but it only ever sees it as a market factory. This is the single line in the whole program that names a market. Nothing after it does.
The client asks for the tax rules. Notice that the method takes no arguments. There is no market to pass in, because the market was decided when the factory was chosen. Back comes a value added tax calculator, typed only as a tax calculator.
The same factory is asked for a currency formatter, and it returns a pound formatter. The client could not have asked for dollars here, even if it wanted to. This object is a family member, and the family was already settled.
The third call returns a British postcode validator. Three objects, three interfaces, one factory. They have never met each other, and yet they match, because there is no code anywhere that could have made them not match.
The constructor ends, and the factory is never touched again. From here, the client talks only to the three interfaces. It checks the address first, and it does not know, or care, that this is a British postcode.
The tax calculator supplies both the rate and the word, V A T. The formatter turns the numbers into pounds. Read the checkout code and you will not find a single branch on the country. Every market specific word came from a product.
Now build the checkout with an American market factory instead. The same order, through the same unchanged code, produces sales tax in dollars. And a British postcode sent to the American market is turned away, because the validator came from the same family as the money. You pick a set, never a piece. That is the whole point of the pattern.
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

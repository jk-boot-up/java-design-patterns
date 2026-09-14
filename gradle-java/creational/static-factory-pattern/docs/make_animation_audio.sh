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
# and the key takeaway spelled out. Currency symbols are written out in words,
# because the synthesiser reads them poorly.
narrate() {
cat <<'EOF'
We want two kinds of discount. Ten percent off, and ten pounds off. Both are a single number, so both would be a constructor taking one double, and Java will not allow two constructors with the same signature. A constructor is named after its class, so there is nowhere to put the meaning.
So give the method a name instead. Discount dot percentage, of ten, says exactly what it means. Back comes a percentage discount, typed only as a discount. The caller asked for what it wanted, not for a class to build.
Discount dot amount off, of ten pounds, takes a single value too, and nobody could confuse the two. As constructors, these could never have existed side by side. As named methods, they sit together quite happily.
Discount dot none returns the very same object every single time, because a discount of nothing has no state worth copying. The word new is defined as making something new, so a constructor could never have done this.
Now ask for percentage of zero. You do not get a percentage discount of zero. You get the shared do nothing one instead. You asked for an outcome rather than a class, so the method was free to serve it however it liked, and nobody outside can tell the difference.
Discount dot for coupon reads a code from the storefront and returns whichever implementation fits. The best deal code builds a composite holding two other discounts, a class the caller could not have assembled itself, because it cannot name any of the three.
And the checkout applies whatever it is handed. Search it for the word new, for a branch on the kind of discount, or for any of those five class names, and you will find nothing at all. Every choice was made inside a factory method, long before this code ran. Remember the one sentence. A constructor cannot be named, and cannot refuse to allocate. A static factory method can do both.
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

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
CatalogDemo makes exactly one call: electronics dot total price. It has no idea how deep the tree underneath is, or how many children each node has.
Electronics loops over its children. The first one, Phone, is a Product, a leaf. It has no children of its own, so it simply returns its own price. That is the base case of the recursion.
The second child, Accessories, is itself a Category. Calling total price on it does not return an answer directly. It triggers the exact same method, one level further down.
Accessories loops over Case and Charger, both leaves. Each one answers immediately with its own price, exactly the way Phone did one level up.
Accessories' third child, Cables, is another Category. It recurses again, down to its one leaf child, U S B dash C Cable, which answers directly. The tree can nest as deep as it wants. This is still the same method.
Now that every child has answered, Accessories adds up Case, Charger, and Cables, and returns one number up to Electronics.
Electronics adds Phone's five hundred ninety nine ninety nine to Accessories' fifty nine ninety seven, and that single number is what CatalogDemo receives. No instanceof, anywhere, at any level.
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

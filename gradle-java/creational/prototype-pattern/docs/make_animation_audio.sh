#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice used in the
# teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-8.m4a
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
Master is a product listing already built by hand. Sku, title, description, category, brand, price, two images, two attributes, a shipping profile, a return window, a warranty. Assembling all of that once is the expensive part.
Java already offers object dot clone via cloneable, but it's protected, throws a checked exception that can never fire, and copies fields shallowly by default. Product listing implements prototype of product listing instead. One plain method, copy.
Copy calls the product listing constructor again, and that constructor always builds a brand new array list from whatever images list it was handed. The clone's image list is never the same object as master's.
Same reasoning, same constructor line. A brand new linked hash map, built fresh on every call. Mutate the clone's attributes and master's map is untouched, because they were never the same map.
Shipping profile is passed straight through, unchanged. It's safe because shipping profile is an immutable record. Nothing can mutate it out from under either listing, so there is nothing to protect by copying it.
White variant is master dot copy, with set sku, set title, an attribute change and a new image list applied afterwards. Master's images and master's attributes come back exactly as they were. The clone's edits never reach back into it.
Listing registry dot create of earbuds template never constructs a product listing itself. It looks up whatever was registered and calls copy on it. Call it twice, and you get two separate, independently mutable instances.
Registry dot create of does not exist throws a no such element exception before anything is cloned. A registry trades a compile time constructor name for a runtime string key, and this is the failure mode that trade brings with it.
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

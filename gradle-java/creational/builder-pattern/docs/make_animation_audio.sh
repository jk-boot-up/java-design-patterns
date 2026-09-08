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
Order id, customer id, items, shipping address, gift wrapped, gift message, coupon code, priority, notes. Nine positional parameters, most of them optional, and two of them booleans a compiler will happily let you swap without a word of complaint.
Purchase order dot builder, of order id and customer id, is the only way to a fresh builder, and it only asks for the two facts every order truly needs. Nothing has been assembled yet.
Add item of mug, then add item of book. Each call returns the very same builder, so the next call chains straight off the end of it. The order the items were added in is the order they will appear in.
Shipping address of home is a required piece too, but it still arrives through a named call rather than a fixed constructor slot. Build will refuse to proceed without it, but nothing stops you setting it first, last, or anywhere in between.
Gift message of happy birthday does two things. It stores the message, and it quietly sets gift wrapped to true, because a gift message on an unwrapped box makes no sense in this domain. That rule lives in exactly one place, the builder method, not scattered across every caller.
Coupon code of welcome ten could just as easily have come before the gift message, or before the shipping address. There is no fixed slot to get wrong, because there is no positional argument list at all.
Build asks two questions no earlier call could have honestly answered. Is there at least one item, and is there a shipping address. Only once both are true does it call the private purchase order constructor, which takes a snapshot of everything the builder held. Reuse the same builder for a second order, and the first one never changes underneath you.
Purchase order presets dot gift order plays the director role the Gang of Four book draws as its own interface, but it only ever calls the builder's public methods, never the purchase order constructor directly. Two orders built by hand fail on purpose. One with no items, one with no shipping address. Remember the one sentence. A constructor makes you decide the whole object in one call. A builder lets you decide it a piece at a time, and checks it is complete only when you say you are done.
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

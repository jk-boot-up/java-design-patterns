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
Checkout Service calls quote rate, ninety four one oh seven, three point five, on whatever Shipping Rate Provider it was constructed with. Right now that happens to be an Acme Shipping Adapter, but Checkout Service's code does not change based on that fact.
Before calling the adaptee, Acme Shipping Adapter converts the incoming weight from kilograms to pounds, the unit Acme Shipping S D K actually expects. This conversion lives in exactly one place in the whole codebase.
Acme Shipping Adapter calls fetch cost in cents on the Acme Shipping S D K it holds. This is the one seam where the two incompatible shapes meet. Everything past it is the adaptee's own problem.
Acme Shipping S D K computes a price in integer cents from a pound weight. It was never written with this adapter in mind. It is unmodified third party code doing exactly what it always did.
Acme Shipping Adapter divides the returned cents by one hundred, rounding half up to two decimal places, and hands Checkout Service a Big Decimal in the shape it originally asked for.
Construct Checkout Service with a Flat Rate Shipping Provider instead, a class written natively against Shipping Rate Provider, with no adapting involved at all. Checkout Service cannot tell the difference.
Exactly one class, Acme Shipping Adapter, ever imports Acme Shipping S D K. Every other class in this codebase, present or future, only ever depends on Shipping Rate Provider.
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

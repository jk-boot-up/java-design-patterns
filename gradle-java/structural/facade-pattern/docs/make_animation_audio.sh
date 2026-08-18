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
RATE="${RATE:-170}"            # words per minute

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

# Narration for each step. Kept in the same order as STEPS in animation.html.
# These are spoken versions of the on-screen text, with a little more warmth
# and the key takeaway spelled out.
narrate() {
cat <<'EOF'
The client, our demo class, builds an order request and makes a single call to place order. It has no idea that inventory, payment, shipping or email even exist.
The facade takes over. It receives the request, generates an order id, and it is now responsible for calling each subsystem in exactly the right order.
First, the stock is reserved. Inventory is always checked before anything else, so that if we cannot reserve the item, we stop right here and nobody is ever charged for something we cannot ship.
Only now, with the stock secured, does the facade charge the customer, and it keeps the payment id that comes back. Enforcing that ordering is exactly the kind of rule a facade exists for.
Next the warehouse is told to schedule the shipment, and it returns a tracking id which the facade holds on to for the confirmation.
Finally the confirmation email goes out, carrying the order id and the tracking id that the earlier steps produced.
And the three separate results are assembled into one order confirmation and handed back. The client sees one call and one object, and never the complexity underneath.
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

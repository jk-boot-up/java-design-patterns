#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-10.m4a
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
Flat rate, weight bands, distance, and the free over fifty campaign. Four completely different calculations, sharing nothing but the Shipping Cost Rule interface. Notice each one reads a different field of the shipment, and Flat Rate Rule reads none at all.
Shipping Rules dot by name, weight, turns a configuration value into an object. This is the only branch left in the whole design. It runs when the shop is configured, rather than on every order, and in a real store it would be a database row.
The rule arrives as a constructor argument. Checkout Service did not create it, cannot replace it, and has no way of asking which of the four it turned out to be.
An order arrives. Cardiff, six point five kilos, a hundred and eighty miles, sixty four pounds. The client calls quote with the whole shipment. It carries destination, weight, distance and subtotal, more than any single rule uses, which is exactly what keeps the interface stable when a new rule needs a field the others ignore.
One message: cost for shipment. This is the whole of Checkout Service's pricing logic. No if, no instance of, no enum. It asks the rule exactly once. Calling it twice would double charge the day somebody writes a rule that is not free of side effects.
Weight Banded Rule checks six point five kilos against its bands. Over one kilo, over five, under twenty. Twelve pounds. That band table lives in this class and nowhere else, and it has its own test that never goes near checkout.
The quote comes back. Sixty four pounds plus twelve pounds is seventy six. Checkout Service also asks the rule for its name, so the receipt can say which policy priced it. That second message is why the interface has two methods. Without it, the client would need a table mapping rules to display names, and that table is the deleted switch growing back somewhere new.
Marketing turns on free delivery over fifty pounds. A different rule is selected at the edge. One configuration value changes. Watch what happens to Checkout Service in the next two steps. Nothing.
The same order, the same messages, a different answer. Quote, then cost for, then name. Identical to steps four through seven. The rule reads the subtotal instead of the weight, sees that sixty four pounds is over the fifty pound threshold, and charges nothing.
That is the entire payoff of Strategy. The delivery charge went from twelve pounds to nothing, and not one line of Checkout Service was edited, recompiled or retested. Adding a fifth rule, locker collection say, is one new class implementing one interface. The switch did not move somewhere else. It is gone.
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

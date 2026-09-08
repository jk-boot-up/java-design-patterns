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
Six steps, and an order that is not a style choice. Every order this shop fulfils runs the same six: validate, reserve, charge, pack, dispatch, notify. Charging before reserving takes money for goods you cannot supply. Notifying before dispatching sends an email about a reference that does not exist yet. Hold on to that last one.
The hand-written digital route starts out fine. Naive Fulfilment has three methods, one per route, and each writes the whole sequence out for itself. The digital copy validates, decides there is nothing to reserve, takes the money, and has nothing to pack. Four steps in, and everything it has done is correct.
Then it emails the customer, fifth. The email quotes the dispatch reference. But dispatch has not run, so the reference is still the placeholder: not dispatched. Nothing throws. The email is composed, addressed and sent, and it contains nothing worth having.
And it issues the licence key sixth, to nobody. One line later the key is minted, and it is perfectly correct. The customer will never see it. Two lines are in the wrong order, in a sequence that exists nowhere except inside three method bodies, and nothing in the language, the compiler or the test suite knows those six calls have an order at all.
The same drift, in a different copy. The marketplace copy moved its charge above the seller confirmation. So a customer can be charged forty-two pounds and then told the seller will not supply it. The exception is correct, the refusal is correct, and the money has already gone. Two copies, two independent drifts, and neither was a difficult mistake to make.
Write the sequence once, and close it. Same six steps, same three routes, one change of shape. The sequence moves into a single method on an abstract base class, and that method is marked final. A route may decide how a step behaves. It may not decide when the steps run, and now that is not a rule anybody has to remember.
Validation runs first, and asks the route one question. Validate is private, so no route can replace it. The only say a route gets is answering a hook: does this route require a shipping address? The digital route answers no, and gets its addressless order through. Notice what it did not get. It cannot skip validation, and its orders still have to have lines and an email address.
Two required steps, filled in by the route. Reserve and charge are abstract, so every route must answer, because no default would be right for all of them. Holding stock in a warehouse and asking a marketplace seller to confirm have nothing in common but their place in the sequence. The digital route has nothing to reserve, and says so out loud rather than doing nothing quietly.
A step with a default, replaced by the one route that differs. Pack is not abstract. The base class already knows how to box and label an order, so the warehouse route says nothing at all about packing and gets that for free. The digital route overrides it, because there is nothing to put in a box. Choosing which steps deserve a default, and which must be answered, is most of the work of using this pattern.
Dispatch runs fifth, and mints the key. The digital route's dispatch generates a licence key and writes it onto the report as the dispatch reference. This is the step that, in the hand-written copy, ran last. Here it cannot: it is the fifth line of a method no subclass is able to override.
And notify runs sixth, with something to say. The email quotes the dispatch reference, exactly as the hand-written copy did, using the same two lines of code. This time the reference is there. Not because the author was more careful, but because the order is structural. No route, present or future, can put notify before dispatch.
The empty hook, a fourth route, and the honest cost. After fulfilment does nothing, and is called anyway, so the marketplace route has somewhere to post its commission without the base class knowing marketplaces exist. Click and collect is one new class and no edit to anything that already worked, and it gets the same six steps in the same order for free. What it costs is inheritance. Every route is welded to this base class and can extend nothing else, and a seventh step here lands on all four at once. Pay that when the order is what you are protecting, and compose strategies when it is not.
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

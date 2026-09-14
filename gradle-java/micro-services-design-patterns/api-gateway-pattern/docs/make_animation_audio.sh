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
One product page, four owners. The page for an espresso machine needs four answers: the name, the price, whether it is in stock, and the row of suggestions along the bottom. In a shop built out of services, those belong to four different teams. The obvious app asks all four itself, and it works. Every test you would think to write for it passes.
The first call costs two hundred milliseconds. A round trip from a phone on a train to the data centre and back is about that, and almost none of it is the work. It is the distance, the radio, and setting up a secure connection. The catalog service also checks the shopper's token before it answers.
And so do the next three. Price, stock, suggestions: three more round trips, three more token checks. Eight hundred milliseconds of a shopper looking at a half-drawn screen, and the same security decision made four times, in four different codebases.
Now the recommendations service goes down. The name arrived. The price arrived. The stock flag arrived. All three are thrown away with the error, because a row of suggestions nobody would miss did not answer. The shopper wanted to know what an espresso machine costs, and now they cannot find out.
So put one service in front of the four. The gateway is the only thing in the system that knows the product page is made of four parts. The app now makes one call, to one address, and gets back one object, already shaped the way the page wants to be drawn.
The token is checked once, at the edge. At one hundred milliseconds the gateway establishes who is calling, and nothing behind it has to ask again. One security decision, in one place, rather than four copies of it drifting apart in four codebases.
Behind the door, the calls are cheap. Catalog answers at one hundred and ten, pricing at one hundred and twenty, inventory at one hundred and thirty. These are calls inside the data centre, so each one costs about ten milliseconds rather than two hundred. The same four services; a different network.
Recommendations fails again, and this time the page survives. There is exactly one try and catch in the gateway, and it is wrapped around exactly this call. The catch writes the word degraded into the timeline and returns an empty list. The shopper gets the name, the price, the stock and no suggestions, in two hundred and forty milliseconds. Nobody tells them anything is wrong, because from where they are standing, nothing is.
But the catalog service failing is a different matter. This time the service that knows the product's own name is down, and the gateway does not degrade. It refuses, and the shopper is told in one hundred and ten milliseconds that the page cannot be shown right now. A product page with no product on it is not a degraded page. It is a blank one.
Here is what the gateway must never start doing. It joins, and it forwards. It does not price anything, apply a discount, or decide whether a product may be sold. A gateway that fills up with business rules becomes a bottleneck that owns no data and that nobody dares to change. That is the receptionist who starts deciding the room rate.
So the tests assert the cost, not the page. Both versions return the same page, so a test that checked the page would pass on either one and prove nothing. Instead the tests assert one remote call against four, one token check against four, and two hundred and forty milliseconds against eight hundred. They are exact numbers, because the clock is simulated.
One front door, and one place to decide. One crossing of the slow network, one token check, one address for the client to know, and one place where the question of what to do when a service does not answer finally has an owner. That last one is not in the textbook definition, and it is the half that earns its keep.
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

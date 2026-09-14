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
One ordinary page, owned by three services. A shopper opens one of their orders. The page shows the order reference, a line for each thing they bought with its name and its price, the total, and underneath, where the parcel has got to. Utterly unremarkable, except that three different services own those facts, and there is no database join any more. Orders knows what was bought. Catalog knows what a sku is actually called. Shipping knows where the parcel is.
So call all three, one after another. This is what everybody writes first, and it is three lines of entirely ordinary Java. Fetch the order. Ask Catalog for the names. Ask Shipping for the status. Be fair to it. There is no bug here. It returns exactly the right page, every test written against it passes, and a code review waves it through without a comment, because the cost is not in the code at all. The shopper waited two hundred and ten milliseconds. Thirty, plus sixty, plus a hundred and twenty, added up.
Where sixty of those milliseconds are hiding. Read the third call again. Shipping left at ninety milliseconds. But what does Shipping actually need? The order id. And the order id arrived at thirty. It sat and waited sixty milliseconds for Catalog's answer, and then never looked at it. That is not a bug anybody could point at in a diff. It is what a sequence of statements does, and it is why nobody ever notices the day a page got slower.
Send them together. But not all three. The fix is to stop waiting. Except notice what this page cannot do. It cannot send all three calls at zero milliseconds, because Catalog has to be told which skus to look up, and only Orders knows which skus are on the order. So the shape is one call, and then two together. Working out which calls genuinely depend on which is most of the job here, and it is exactly where the instinct to just parallelise everything comes unstuck.
Both leave at thirty, and the sum becomes a maximum. Catalog and Shipping now depart at the same instant. Catalog comes back at ninety, Shipping at a hundred and fifty, and the page is finished the moment the slower of the two lands. A hundred and fifty milliseconds instead of two hundred and ten. Nothing got faster. Shipping still takes its full hundred and twenty. What changed is that nobody is queuing. Sequential calls cost the sum of their latencies. Parallel calls cost the maximum.
Now Shipping stops answering. Here is the same outage, given to both versions. The sequential one fetches the order, gets the product names, then calls Shipping, and throws. And look at what goes down with it. The order and the names had already arrived, sitting in local variables, perfectly good. Both thrown away. The shopper is shown an error page assembled out of two correct answers that nobody looked at.
A branch that fails is parked, not propagated. The fan out does something different, and it is four lines. Each call runs inside a try, and when one throws, the exception is caught and parked on that branch rather than allowed to escape. Nothing else is disturbed. Catalog's answer is still there. The order is still there. And now the composer can ask, afterwards, one branch at a time, whether that particular absence is actually fatal.
Required or optional, and it is one method call. So which absences are fatal? That has to be decided in advance, and in this project it is not a config file and not an annotation. It is which of two methods the composer calls on a branch. One of them rethrows whatever was caught, and that is for data the page genuinely needs. The other substitutes a fallback, and that is for data the page can do without. One line per dependency, written deliberately by somebody who knows what the page is for.
The page goes out with a named hole in it. The shopper still sees what they bought, the quantities, and what it cost, because none of that was ever Shipping's to know. And where the delivery section would be, the page says it cannot check this right now, and lists delivery status as missing. That list matters. A page that quietly drops the delivery section looks exactly like a page for an order that has not shipped yet, and the shopper cannot tell the two apart.
And the fallback that would have been easy to write. There is a temptation here worth naming out loud. Instead of saying we cannot check, you could write in transit. It is nearly always true, it reads better, and nobody complains. Do not do it. A shopper who is told their parcel is in transit will not ring up about the one that never left. The page is allowed to say it does not know. It is not allowed to make something up, and there is a test in this project whose only job is to stop somebody being helpful here.
Orders goes down, and refusing is the right answer. Now the other direction. If Orders does not answer, the composer does not degrade anything. It throws, and the shopper gets an honest error. That is correct, not a gap in the pattern. A page with no order on it is not a partial page, it is a blank one. And because the failure happens before the fan out even exists, Catalog is never called at all. Being able to say this one is required is as much a part of the pattern as being able to degrade.
Why any of this matters. Availabilities multiply. This last one is arithmetic rather than code. Suppose each of these three services is up ninety nine point nine percent of the time. That is a good service. About forty three minutes of downtime a month. So how good is a page that needs all three? Not ninety nine point nine. The page is up only when all three are up at the same moment, and those probabilities multiply. Ninety nine point seven percent, which is a hundred and twenty nine minutes a month. Three excellent services make a page worse than any of them. And the way out is not better services. It is needing fewer of them.
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

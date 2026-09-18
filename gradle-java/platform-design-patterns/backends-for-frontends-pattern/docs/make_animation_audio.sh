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
# field names are spoken as English rather than as identifiers, and the key
# takeaway is spelled out a little more plainly than the caption does.
#
# One line per step, and the count must match the STEPS array. If you copied
# this file from another pattern, replace every line below before running it.
narrate() {
cat <<'EOF'
The shop sells one copper coffee maker. On a phone, the product screen draws six things: a title, a price, one photograph, a star rating, the number of ratings, and one line saying when the parcel arrives. On a desktop, the same product fills a page with fifteen, including the description, five photographs and three written reviews. Both are correct. They simply disagree about what a product is, and that disagreement is the whole of this pattern.
The obvious first design is to let the phone call the services itself. Each service owns its data and publishes its endpoint, so the phone asks all five. Five requests and five answers, every one of them crossing the customer's own connection, and they happen one after another rather than all at once, because you cannot ask pricing about a product until the catalog has said which product it is. On office wifi nobody notices. On a train, each one is a wait of its own.
Every one of those five responses arrives whole, because a service that publishes one endpoint publishes one shape. Twenty-nine fields land on the phone and six of them reach the screen. That is wasteful, but the waste is not the serious problem here. The serious problem is still the five round trips before a single pixel can be drawn.
So the shop puts one endpoint in front of the five services, and every client calls it. One round trip instead of five, which is a real win, and the pattern we end up with keeps it. But one endpoint publishes one document, and that document has to satisfy the fussiest client, so it grows into the union of everything anybody has ever needed. Seventeen hundred and fifty-five bytes arrive. Two hundred and twelve are drawn. Eighty-seven per cent is thrown away on arrival.
Now the obvious fix. Ask for only the fields you want. Add a field list to the query string, and the endpoint sends two hundred and twelve bytes instead of seventeen hundred and fifty-five. The size problem is solved, completely, by a query parameter. If this pattern were about payload size, the story would end here, with no new services to run and nothing left to explain.
And then the phone team asks for one line of text. Free delivery, arrives Friday. It does not exist in any service. Making it means asking inventory whether the item is in stock, asking the delivery rules what that means for tomorrow, looking at the clock, and joining the three into a sentence the designer wrote. Half an hour of work. But a new field on a shared endpoint is a change to a document that five other clients also receive, so it joins a queue behind work that has nothing to do with the phone. The phone team could have written it in an afternoon. They wait five weeks.
So give the phone its own backend, owned by the phone team. One call comes in from the device. Four calls go out inside the data centre: catalog, pricing, inventory and reviews. Recommendations is not called at all, because this screen has no related products strip. Then it builds six flat fields and sends a hundred and ninety-six bytes. The price arrives as a string with a pound sign already in it. The delivery promise arrives as a whole sentence.
The desktop store gets its own backend too, calling all five services and sending fifteen fields. Look at the delivery field on both sides. The phone was given a whole sentence. The desktop is given the bare date, because the desktop page has a delivery panel and wants the parts so it can lay them out itself. That is not an inconsistency waiting to be tidied up. Two backends over the same data, disagreeing about what a product is, is the pattern working.
Here are the three designs measured side by side, and the two right-hand columns are the point. The calls from the phone fall from five, to one, to one. The calls inside the shop barely move: five, five, four. The work did not go away. It moved off the customer's mobile connection and onto a data centre network where a call costs almost nothing. And the phone's document is eighty-nine per cent smaller than the shared endpoint's.
Now the bill, and there are three items on it. The first. The pricing team reviews the discount rule and adds a condition: a higher price may only be advertised as a saving if it was genuinely in force for long enough. For this product it went up eleven days ago, which does not qualify, and both backends are told so. The desktop reads the current rule and claims nothing. The phone runs a copy taken before the review, subtracts, and advertises twelve pounds off. Same product, same price, same second, and one of those screens is making a claim the shop is not allowed to make. Nothing throws. Nothing is logged. The only person who can see it is a customer with both screens open.
The second item. Every request needs four things done to it, whoever sent it: verify the customer's token, refuse traffic over the rate limit, terminate the encryption, and write the access log. If each backend does them itself, that is four jobs times two backends, eight copies of work that is identical by definition. A gateway in front does them once, and the count does not depend on how many backends there are. The line is one question. Does the code answer, what does this screen need? Then it belongs in a backend for that frontend. Does it answer, is this request allowed in at all? Then it belongs in front of all of them.
The third item. The shop has six clients: a phone app, a desktop store, a tablet app, a smart television app, an in-store kiosk, and a nightly partner feed. One backend each would be six. But the tablet shows the phone's six fields in a wider column, the kiosk is the desktop page with the basket hidden, and the feed is not a screen at all. Three of the six genuinely disagree about what a product is. Three do not. The test is not the device, and it is not the team. And every extra backend costs a pipeline, a place in the on-call rota, a dependency upgrade every time a shop service changes, and one more process to look at during an incident. Two backends is a pattern. Nine is a department.
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

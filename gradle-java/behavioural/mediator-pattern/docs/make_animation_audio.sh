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
A checkout page. Country, shipping method, gift wrap, the total, and the place order button. Change the country and the courier list has to change with it, gift wrapping may have to be withdrawn, the total moves, and the button may no longer be pressable. Four rules. The difficulty is never the rules. It is where you write them down.
The obvious place for, when the country changes, refill the couriers, is inside the country widget, because that is where the country changes. So it is given the shipping widget. Then gift wrap depends on the country too, so it gets that. And the total. And the button. Nine references, on a page with five controls.
And that is where the bugs come from. Change the country on that version and gift wrapping is withdrawn, but the tick is left behind, so the shopper pays two pounds for wrapping the warehouse will never do. The shipping method is cleared, but nobody re-checks the button, so the order goes through with no courier on it. Neither of those is a line of code you could review. Both are a line nobody wrote.
Now give them one thing to talk to instead. Every control holds the form, and the form holds every control. Five references instead of nine, and it stays five when a sixth control arrives. Aircraft near an airport work the same way. They do not negotiate with each other, they all talk to the tower, because the rules of the airspace need to be in one head.
The shopper picks the United Kingdom. Watch how far the country widget's involvement goes. It stores the string, it calls changed, and it stops. It does not know that a courier list exists.
The form works out what that means. The source was the country, so the form reshapes itself. The courier list is refilled with the two that serve the U K, and gift wrapping is offered, because the London warehouse can reach this order. Then it reprices, and re-checks the button, as it does after every single change.
Express shipping, six pounds. This time the source is not the country, so nothing is reshaped. Only the price and the button. Forty pounds of basket plus six of courier, and now that there is both a country and a method, the button comes alive.
And gift wrap it, please. Two pounds more. Forty eight. The tick box announced a change, the form added it up again, and nothing else on the page had to be told.
Then they change their mind, and send it to the States. This is the moment the tangled version got wrong twice. And the country widget's part in it is exactly what it was before. Store the string, say so, stop. It has no idea that anything is about to happen.
The form reshapes. The couriers are replaced by the international one, and the method the shopper had chosen is cleared with them, because Express is not on the new list. Gift wrapping is withdrawn, and the tick goes with it, in the same call. There is no method that does only half of that, so there is nothing to forget.
Then it reprices and re-checks, as it always does. Forty pounds. The basket, and nothing else, because nothing else is chosen. And the button goes back to disabled. Nobody worked out that clearing the courier ought to disable the button. The form simply re-asks that question after every change, whatever the change was. Cheap and always right beats clever and sometimes stale.
The same click, on the tangled version. Forty two pounds, two of them for gift wrapping that will not happen, and a button that will happily take an order with no courier on it. Same page, same click. The difference is not care, or skill. It is that on one of them, there is a single place where the answer to, what happens when the country changes, has to be written down.
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

#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-11.m4a
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
Inventory, email, analytics and the warehouse feed. Four completely unrelated reactions, sharing nothing but the Order Listener interface. Notice they do not even want the same events. Inventory ignores everything except shipping and cancellation, and analytics wants the lot.
They subscribe. Four calls to add Listener, and the direction matters: the subscribers attach themselves. Order now holds four Order Listener references and knows absolutely nothing else about them. Not their types, not what they do, not that a mail server is involved anywhere.
The order ships. Move to, shipped, builds an Order Event, carrying the order id, the status it came from, and the status it is going to, and sets its own status first. That order matters. A listener that does look at the order should see the world the event describes, not the one it replaced.
Inventory is told, and releases the reservation. One message: on status changed. The order is not calling a method named after inventory. It is calling the interface method on whatever happens to be first in the list.
Email is told, and writes to the customer. Exactly the same message to a completely different object. The wording of the shipping email lives in Email Listener and nowhere else, so marketing rewriting it touches one file, and it is not the file the payment team is editing.
Analytics is told, and counts it. Analytics wants every transition, including ones nobody has invented yet. Under the pattern that is a subscription and nothing else. Under the version that calls each system by name, it is a standing obligation on every method that ever changes a status, and the one that forgets is a hole in the funnel nobody notices for a quarter.
The warehouse feed writes its line, and move to hands back an empty list of failures. Four systems reacted to one status change, and Order still does not know what any of them did.
A fifth reaction, written after Order was compiled. Loyalty points on delivery. It is defined in the demo file, against nothing but the interface, and attached with one more add Listener call. Order was compiled long before this existed and did not need recompiling. That is the extension point being real, rather than a list of four.
Now the mail server times out. Email Listener throws, in the middle of the notification loop. This is the moment the naive design falls over. With four direct calls in a row and no try block, the order is already marked shipped, the stock is already released, and the two systems after email never run at all.
Order catches it, writes it down, and carries on. The exception is caught inside the loop, recorded as a Listener Failure against the listener's name, and the loop moves to the next subscriber. Analytics is still counted. The warehouse feed is still written. The parcel still gets picked.
That is the payoff, and here is what it cost. One announcement reached five independent systems, a broken one did not take the rest down, and Order was never edited. The honest cost is that reading move to now tells you nothing about what happens when an order ships. You have to find every add Listener call, and your development environment cannot help, because they are all typed as the interface. That is a real loss of legibility, traded for a real gain in independence.
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

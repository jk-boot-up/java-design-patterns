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
A basket with three products and a voucher: sixty five pounds. Its state is two things, the lines in it and the voucher code applied to it, and the ticket says add an undo button. Undo has to put back whatever the last change touched. It sounds like an afternoon's work.
The obvious attempt is to keep a before copy in a field. Save the list, and put it back when undo is pressed. Except that saved lines equals lines does not copy anything. It writes down where the list is, not what is in it, so the save and the live basket are the same list, and every later change edits both of them.
So undo empties the basket. It clears the live list, which is also the saved list, and then copies the now empty saved list back over it. The shopper presses undo and their basket is gone. And the voucher was never saved at all. Nobody decided that. It simply was not on anyone's mind, and there is no line of code you could review to find it.
Now do it properly. Ask the basket for a snapshot, because the basket is the only class that knows what its own state is. List dot copy of makes a real copy, taken at this moment, that nothing can reach afterwards. A photograph of the basket rather than a window onto it.
The snapshot goes onto the undo stack. The history can read the label, because label is public, so an undo menu can say, removed the laptop stand. Lines and voucher are package private, so only the basket can get the state back out. Undo works here without the history knowing that a basket contains anything at all.
The shopper removes the laptop stand by mistake. The live basket changes: three items, thirty one pounds. Now look at the snapshot. It has not moved. That is the whole difference between a copy and a reference, and it is one line of code wide.
Undo. The history pops the snapshot off the stack and hands it to the basket. That is its entire contribution. Hold this, and give it back later. It never looked inside, and it did not need to, because putting the basket back is the basket's job.
Only now is the envelope opened, and only by the basket. Restore calls lines and voucher on the snapshot. Those two methods are invisible from outside the package, so this is the one place in the whole program where a snapshot gives up what it is holding.
Both fields come back, because both were saved. Four items, the voucher, sixty five pounds. Lines and voucher travel together, because they are both state, and a snapshot is complete by definition. The naive version restored one of them and silently forgot the other.
And the snapshot survived being used. Restore read from it and left it exactly as it was. Nothing was consumed. That is why redo, or a branching history, is an addition later rather than a rewrite. The same snapshot could be restored again tomorrow.
Next month the basket grows a gift message. Add it to save, and to restore, and undo covers it. Two methods, in the class that already knew what the state was. Nothing outside the basket has to hear about the new field. Not the history, not the undo button, and not the tests for either.
And here is the same undo on the version without a snapshot. An empty basket, and a voucher that will not come back. Same shopper, same click. The difference is not care, or skill. It is that on one of them, the object that owns the state is the only one that copies it, and it copies all of it.
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

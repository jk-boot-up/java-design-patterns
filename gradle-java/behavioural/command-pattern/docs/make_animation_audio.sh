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
A cart that is not empty, which is the only interesting kind. Three headphones, a cable, a case, and a ten percent code the customer already applied. Every undo bug in this project needs a cart that had something in it before the edit arrived. Against an empty cart, the naive version and the pattern give the same answer.
The naive editor adds two, and writes down what it was asked. The cart goes to five, and the editor pushes a note: add, H one hundred, two. It is a perfectly honest record of the request. Read it back tomorrow and you will know exactly what the customer asked for.
And a better coupon replaces the old one. Black Friday goes on, and Welcome ten comes off, because a cart holds one coupon. The note for this edit says coupon, Black Friday. Nothing anywhere has written down the code that was just replaced.
Two undos, and the customer's cart is wrong. Undo pops the coupon note and clears the coupon, so a discount the customer never touched is gone. Undo again pops the add note and removes the line, so all five headphones vanish, including the three that were there before anybody asked for anything. The notes were never wrong. They simply never held the state that undo needed.
Now make the action an object. Same cart, same two edits, one change of shape. Instead of calling a method and scribbling a note beside it, we build an object: describe, execute, undo. That object can be stacked, read back, and asked to reverse itself. A method call can do none of those things.
Execute asks the cart what is there, before touching it. The first line of execute is the whole pattern: previous quantity equals cart dot quantity of H one hundred, which is three. It happens now, at run time, from the receiver. Not in the constructor, which was written before anyone knew what this cart held.
Then it makes the change, and the invoker files it. Five headphones, the same as before. Cart History pushes the command onto the undo stack and clears the redo stack, because taking a new action makes the old future unreachable. Neither line mentions headphones, quantities or coupons. Search Cart History for any of those words and it is not there.
The coupon command captures the one it is replacing. Apply Coupon Command does the identical thing one edit later: previous coupon equals whatever the cart had, which this time is Welcome ten. Nine times in ten that capture is null and looks pointless. The tenth time it is the difference between a correct undo and a customer quietly losing a discount.
Undo is a message, not a decision. Cart History pops the top command and sends it undo. It has no idea whether the cart is about to lose a line, gain one, or change a coupon. The command restores Welcome ten from the field it wrote down, and moves across to the redo stack.
And the second undo puts back three, not zero. Previous quantity was three, so undo does not remove the line. It writes the line back at three. That branch is chosen by a value the constructor never saw. This is the exact case the note and switch version got wrong four steps ago, and it is one field of difference.
Redo runs execute again, and captures again. The command comes off the redo stack and is executed a second time. It re-reads the cart, so previous quantity is worked out afresh rather than trusted from last time. That is why capturing during execute, and not once in the constructor, survives being undone and redone all afternoon.
A fifth kind of edit, and the log that came free. Gift wrapping is one new class implementing the interface, and Cart History runs it unchanged. It was compiled before that class existed. Meanwhile every edit can describe itself, so the audit trail is a list of strings you did not have to write. The honest cost is that four edits are now four classes, and every one of those inverses is yours to get right. The pattern gives you a place to put undo. It does not check that yours is correct.
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

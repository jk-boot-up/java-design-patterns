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
An online shop runs three promotions. Each one is a code, a percentage, and a rule about who qualifies. Written as Java, the first is four lines, and there is nothing wrong with it. The trouble is not the first promotion. It is the fourth, because by then each new one is written by copying the one above it.
The first copy gives money away. Save fifteen was meant to be a UK order over one hundred pounds. That it was UK only sat in the paragraph above the sentence somebody read, so no line of code was ever written for it. Every large overseas order now takes fifteen percent off.
The second copy withholds it. Free ship was copied from a welcome offer that retired last spring, and the first order check came along with it. A returning UK shopper with three items is offered nothing. Nobody reports that one, because a missing discount looks exactly like a shopper who did not qualify.
So write the rule as a sentence instead. Country is UK, and basket over one hundred. That is the offer, in the words it was written in, and it can live in a database or a spreadsheet rather than in a source file. The people who own the promotions can read it, which means they can check it.
The sentence becomes a tree of objects. An and rule, holding two leaves. This tree is not a description of the rule. It is the rule, the thing the checkout will actually obey. Two kinds of class, and that is the entire pattern: a leaf holds a value, and a connective holds other rules.
The first leaf asks the order one question. Country is asks the order for its country, compares it, and answers. One comparison, and no other rule inside it. That is a terminal expression, and every terminal in this project is about that size.
The second leaf asks a different one. Basket over asks for the basket total, and one hundred and twenty is more than one hundred. Notice that only the leaves ever touch the order. The connective above them never reads it at all, which is why it can be reused in a language it knows nothing about.
The connective adds nothing but a loop. Every part said yes, so the and rule says yes. Read it again and notice what is missing. It does not know what its parts are, whether they are leaves, or how deep the tree below it goes. It only ever asks. Put a whole other tree in either slot, and not one line of this changes.
And the tree can say what it is. Describe walks the same nodes and gives back the sentence. It is rebuilt from the objects the checkout obeyed, not remembered from the line that was read in, so the audit log and the code cannot drift apart. That is what makes, why did this order get fifteen percent off, a question the program can answer.
Here is the overseas order again, this time answered correctly. Country is says no, and the and rule stops there. Basket over is never even asked. Zero percent, which is what the offer always said. Same order, same shop. The only difference is that the rule is an object rather than a branch somebody copied.
It is Friday, and marketing wants one more. Basket over two hundred, or items at least ten. That shape appears nowhere in the code. It is an or rule, and the shop has never had one. Adding it is one line of text. No new class, nothing recompiled, and nothing deployed.
And a typo is refused on Wednesday. Basket ovr fifty. The parser does not guess. It names the phrase it cannot read, and refuses the promotion as it is being saved. Compare that with a mistyped Java condition, which is valid Java. It compiles, it ships, and it misprices an order on Friday, with nothing anywhere to object to it.
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

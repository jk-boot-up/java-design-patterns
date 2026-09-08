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
Four checks, in one method, in the order somebody typed them. Before an order is accepted we check it four ways. Is the address somewhere a courier goes. Can the warehouse pick every line. What does the risk model think. And will the card cover the total. Written the obvious way that is one method, four ifs, and an early return on each. Read it on its own and there is nothing wrong with it.
The third if answers, and the fourth never runs. This order is over the card limit, and it is also scoring ninety two out of a hundred for fraud. Both things are true. The card check is written above the fraud check, so the method returns with a card problem. Nobody chose that ordering. It is simply where somebody typed the line.
The customer tries another card, and it works. There was never anything wrong with the cards. The second one goes through, the order ships, and the score of ninety two was shouted into a method that had already returned. Nobody wrote this bug. It is a bug in the order that two correct lines are written in.
A boolean has no third answer. A different order, scoring sixty four. That is the middle band, the one where a person should look at it. This method answers with a true or a false, so the middle band has to become one of the two, and it becomes the cheap one. The shape of the answer decides what a check is allowed to say.
Variants are copies, and copies drift. Trade accounts are invoiced monthly, so the card check does not apply to them. Somebody copied the method and deleted the card check. In the same edit, the address check went too. Two desks are now on their way to Jersey, which no courier of ours covers. Nothing in the code says these two methods are related.
One class per check, and the order becomes wiring. Now each check is its own small class, with one method on it. A check either returns a decision, which stops the chain, or returns nothing, which passes the order to the next link. The sequence is no longer control flow inside a method. It is a list of objects that you can pass around, print, and have two of.
The first link decides, and three of them never run. A keyboard going to Jersey. The address link rejects it, and that is the end of the run. Look at what does not happen. The warehouse is not asked. The risk model is not called, and not billed for. The card is not checked. Work behind a decision does not merely become irrelevant. It does not happen at all.
The same order as step two, answered by a different link. The monitor on the two hundred and fifty pound card, scoring ninety two. Same order, same four checks, same program. The fraud link is wired above the card link, so fraud answers, the customer is told the truth, and the card link never runs. Nothing was rewritten. The links are in a different order, and that is all.
The third answer. The order scoring sixty four, the one the naive method accepted. The fraud link returns a referral, which stops the chain exactly the way a rejection does. A link with three answers instead of two costs nothing extra, because the chain does not look inside the decision. It only cares that there is one.
Swap two links, and the naive answer comes back. Here are the same four link classes, wired with the card check above the fraud check. The monitor is now rejected for the card again, exactly as the naive method rejected it. That is worth sitting with. The naive behaviour was never wrong. It was a setting that you could not change without editing the checks.
A variant flow is a subset, not a copy. The trade chain is the standard chain with the card link left out of the wiring. No check was copied, so no check could go missing, so the address link is still there, and the Jersey order is caught. And when every link stays silent, the chain still has to say something. That answer is an argument to the constructor, and there is no way to build a chain without it.
The bill, and when to write the four ifs instead. What it cost. A policy that read top to bottom in one method now lives across four check classes, a base class and a line of wiring. Asking which link rejected this needs a report, which four ifs never needed. And a link holds its own successor, so one instance belongs to one chain. Reach for this when the checks and their order are genuinely something you need to change. When they never change, write the four ifs, and this project agrees with you.
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

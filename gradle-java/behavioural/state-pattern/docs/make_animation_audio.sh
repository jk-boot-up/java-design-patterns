#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-13.m4a
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
Six requests, and an answer that depends on where the order is. An order can be asked to pay, pack, ship, deliver, cancel or refund, and the answer to every one of them depends on where the order currently is. Read the cancel row carefully. It is not a yes and a no. Cancelling a paid order refunds. Cancelling a packed one refunds and puts the stock back. Cancelling a shipped one is not a thing you can do at all.
The obvious first move: a status field, and a check in every method. Naive Order holds one enum and guards each method with a conditional. Be fair to it. It is short, the whole lifecycle is in one file, and every rule can be found by scrolling. The problem is not the enum. The problem is that the rules are written down once per method, and each copy is phrased in whichever direction its author found natural.
The screen is right. The third copy, the one written for the user interface, says a shipped order can only be delivered. That is correct. So the cancel button is never drawn, the agent never sees it, and everybody who looks at the application believes the rule is enforced.
And the endpoint accepts the call anyway. The cancel method was written as: anything that has not arrived yet can be cancelled. So it lists the three states where it refuses. It reads sensibly. It also quietly includes shipped, because shipped is not on that list. The parcel is on a van, the customer has their money back, and the shop has nothing to put on a shelf.
The second drift pays the customer twice. Refund originally accepted only delivered. Support asked for cancelled to be added, so they could sort out cancelled orders, and somebody obliged. But a cancel has already refunded. So the second refund is real money leaving a second time, and the ledger ends up ninety seven pounds and forty nine pence short of zero.
Invert the axis. Every one of those was a single condition, in a chain that was copied and then edited. Nobody was looking at the whole lifecycle, because the lifecycle is not anywhere. So stop writing one method for all states, and start writing one state for all methods. Give the condition a type.
Order holds a state, and every request refuses by default. The interface declares all six requests and gives every one of them a body that throws. A state does not list what it forbids. It lists what it allows, by overriding, and everything else refuses on its own. That single decision means a rule nobody thought to write is a refusal rather than an accident. It is the exact opposite of the enum, where a state left off a guard is a transition you did not mean to open.
Pay, and the state hands over to the next state. Placed State takes the money, and then, as the last thing it does, tells the order to become Paid State. That direction is the whole difference from Strategy. Nobody outside chose Paid State. The order arrived there as a consequence of what it just did, and the state named its own successor.
The same verb, doing genuinely different work. Now the order is packed, and cancel still runs. But it is not the same cancel. Paid State refunds. Packed State refunds and puts the stock back, because somebody has already taped a box shut. Three states, three different bodies for one word. In the enum version those are three branches of one method, and the day somebody merges them because they look nearly the same, the stock stops going back on the shelf.
Ship, and the list shrinks to one. Shipped State overrides deliver, and nothing else. Its allowed actions say deliver, and that answer comes from the same class that holds the methods. So the screen and the endpoint cannot disagree, because there is only one of them now.
The same cancel, refused, and no money moves. This is the request that broke the naive version. Shipped State does override cancel, but only to refuse it with a reason worth telling a human: it is already with the courier, so the customer must refuse delivery or return it. The state does not change, the ledger is not touched, and Order records the attempt in its history on the way past, before rethrowing it.
Delivered, refunded, and then finished. Deliver, then refund, and the order is refunded. That state overrides nothing at all, so it accepts nothing at all, and the refusal explains itself: it is final, and nothing more can happen to it. Not one line of code was written to forbid a second refund. The forbidding is the absence of the code.
An eighth state, and the bill. The demo declares an at locker state inside its own file, and Order, compiled without it, accepts it and refuses everything it did not override. That is the open closed argument, made concretely. Now the bill. Seven classes where there was one enum, and the transition table no longer exists anywhere you can read it. Adding a state means editing whichever state hands over to it. For a small, stable machine, an enum and a map of permitted transitions is often clearer, and you should use it. Reach for this one when the behaviour varies by state, not just the permissions.
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

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
A payment gateway that works nearly all the time. The shop takes card payments through somebody else's gateway, on the other side of the internet. About one call in five fails for a reason that has nothing to do with the payment. A dropped connection. A router that reset. The bank is fine, the money is there, and the request simply did not make the round trip. Every one of those failures is a shopper who filled a basket, entered a card, and got an error page. Most of them do not come back.
So try again. That is the whole idea. If the failure might not happen again, make the call a second time. Attempt one times out, and nothing is charged, because the request never arrived. Attempt two goes through, and a checkout that would have failed becomes a completed order. This much of the pattern is genuinely simple, and genuinely valuable.
Wait before trying again, and wait longer each time. The retrier does not go straight back in. It waits a hundred milliseconds before attempt two, and it would wait two hundred before attempt three. That is backoff, and the reason is not politeness. If the gateway is failing because it is overloaded, the thing that makes the next attempt succeed is the gateway getting some room. A caller that retries instantly is taking room away rather than giving it.
Those three extra milliseconds have a name. The wait was a hundred and three, not a hundred, and the difference is jitter. Every caller waits a slightly different amount. With one caller that looks like pointless noise. Now picture a thousand callers who all failed at the same instant and all wait exactly a hundred milliseconds. They come back as a single wave, at the same moment, and the stampede simply repeats itself on a timer. Spreading them across a band turns the wave into a trickle.
Not every failure is worth another go. The bank declines the card. That is not a network blip, it is an answer. No funds, wrong expiry, a block on the account, and every one of those reasons is still true a hundred milliseconds later. So the retrier throws it straight back to the shopper, in fifty milliseconds, after one attempt. Asking three times would cost two waits and produce exactly the same no.
Now the failure you cannot see. The request arrives. The card is charged. The reply is lost on the way home. Stop and ask what the caller sees. A timeout. The same timeout as before, byte for byte. There is no flag to check, no header to read, and no clever code that can tell a request lost on the way out from a receipt lost on the way back. That is not a gap in this project. It is a property of networks.
The loop everybody writes first charges twice. The naive checkout retries immediately, and it builds its request inside the loop, so attempt two carries a brand new key. The gateway has never seen that key, and a key it has never seen means, by definition, a new job. So it takes the money again. Eight hundred and ninety nine pounds and ninety eight pence, for one espresso machine.
And nothing went wrong. That is the problem. Read what is missing. No exception escaped. Nothing was logged as an error. The checkout returned a valid receipt and the order looks perfect. There is a whole test file written against this class and every test in it passes, including the one that asserts eight hundred and ninety nine pounds leaving a customer's account. A double charge does not announce itself with a failing test. It announces itself as a phone call, two days later.
So stop trying to tell the failures apart. The careful checkout does not attempt to work out what kind of failure it suffered. It makes the difference not matter. Before the first attempt it builds one request, carrying one key, derived from the order and nothing else. Not the attempt number. Not the clock. Not a random value. If any of those crept in, the two attempts would not be recognisably the same job.
The same key on every attempt, and the money moves once. Attempt one charges the card and the reply is lost, exactly as before. Attempt two carries the same key. The gateway looks the key up, finds that it has already charged it, and hands back the charge it made the first time rather than making a second one. The card was charged once. The caller never found out which kind of failure it had suffered, and never needed to.
Somebody has to keep the record. A key is only a promise, and a promise is worth nothing unless the other end remembers it. Inside the gateway there is one map, from key to receipt, and it is checked before any money moves. That map is the entire mechanism. Everything the caller does with keys works only because something at the far end keeps it, which means making an operation safe to repeat is work at both ends, and no retry loop can decide it for you.
Two decisions, and one line in the right place. Retry only the failures you recognise as temporary. Everything else is a definite answer, and persistence will not change it. Wait longer each time, because a struggling service needs room rather than traffic, and add jitter so that a thousand callers are not one wave. Then the half that costs real money. The dangerous failure is the reply lost after the work was done, the caller cannot detect it, and the only defence is a key built from the job and nothing else, outside the retry, before the first attempt.
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

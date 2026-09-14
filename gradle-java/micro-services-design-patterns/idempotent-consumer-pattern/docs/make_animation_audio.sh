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
# These are spoken versions of the on-screen text: column names are read out in
# words, class names are spaced so the voice does not run them together, and
# the key takeaway is spelled out a little more plainly than the caption does.
narrate() {
cat <<'EOF'
A customer checks out, and a message goes out saying the order was placed. The notification service receives it and queues a confirmation email. Then the acknowledgement back to the broker goes missing, and the broker, unable to tell whether the message was handled or lost, sends it again. That is not a fault. It is what at least once delivery means.
The obvious answer is to keep a set of the message ids you have already seen, and skip anything already in it. The second delivery arrives, the id is in the set, and it is skipped. One confirmation queued. This is the version everybody writes, and it is right about what to do, and wrong only about where to keep the evidence.
Same two deliveries, and this time the process restarts in between them. The set of seen ids lives in a field, in memory, so the restart empties it. The second delivery looks brand new, and a second confirmation is queued. The customer now has two identical emails for one order. The database survived the deploy. The set did not.
It would be comforting to call that a coincidence, but it is not one. A restart is one of the most common reasons an acknowledgement goes missing in the first place. So the redelivery and the wiped memory tend to arrive as a pair. The failure is not rare and unlucky. It is the ordinary case, waiting for your next deploy.
Now nothing restarts. The consumer queues the confirmation, and then dies before it gets round to remembering the id. The email is queued and the id is not recorded, so when the redelivery arrives the message looks new and a second email is queued. Two writes, two moments, and a gap between them.
Look at the two failures together, because they are the same failure. In one, the memory of having handled the message is in the wrong place, a field rather than a database. In the other, it is written at the wrong moment, after the work rather than with it. Doing the work and remembering that you did it are being treated as two things.
Here is the whole mechanism. Open a transaction. Queue the confirmation. Record the message id as handled. Commit. Two rows, one commit, and because it is one commit there is no instant where one exists without the other. The record now lives in the same database as the effect, and it is written in the same act.
Restart the process between the two deliveries, exactly as before. The redelivery arrives and the consumer asks the database, not its own memory, whether it has seen this id. It has. The message is ignored, nothing is written, and the customer has one email. The thing that survived the deploy is the thing doing the remembering.
Now kill the process before the commit. Nothing at all was written: no confirmation and no handled id. That sounds like a loss, but it is the opposite. Because nothing was written, the redelivery finds a message that genuinely has not been handled, does the work cleanly, and commits both rows. One email, from a delivery that failed once.
Put the result in one sentence. The broker promises only that the message will arrive at least once, and it kept that promise by sending it twice. The customer received exactly one email. The exactly once is real, and it lives in one ordinary database transaction on the receiving side.
Some handlers need none of this. Setting a shipment's status to shipped twice leaves it shipped. No store, no transaction, no expiry policy. And a handler that is not idempotent can often be rewritten into one that is. Add seventy loyalty points twice and the customer has a hundred and forty. Set the points for this order to seventy, and handling it twice gives seventy.
So: a redelivery changes nothing, a deploy cannot undo what the consumer knows, and a crash never leaves half done work. All three from one ordinary commit. What you pay is a table that grows with every message, and an expiry window, because the ids cannot be kept forever. After that window a genuine duplicate looks new again. The window is chosen, not derived.
EOF
}

i=0
# The narration is read on file descriptor 3, not stdin. `say`, `ffmpeg` and
# `ffprobe` all read stdin when it is available, and one of them will happily
# swallow the first character of the next line if the loop feeds them from it.
while IFS= read -r line <&3; do
  [ -z "$line" ] && continue
  i=$((i + 1))
  # The text goes via a file rather than an argument: `say` otherwise reads
  # from the loop's stdin and swallows the first character of the next line.
  printf '%s' "$line" > "$OUT/.step-$i.txt"
  say -v "$VOICE" -r "$RATE" -o "$OUT/step-$i.aiff" -f "$OUT/.step-$i.txt"
  ffmpeg -loglevel error -y -i "$OUT/step-$i.aiff" \
      -af "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11" \
      -c:a aac -b:a 128k "$OUT/step-$i.m4a"
  rm -f "$OUT/step-$i.aiff" "$OUT/.step-$i.txt"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/step-$i.m4a")
  printf 'step-%-2d %6.1fs\n' "$i" "$dur"
done 3< <(narrate)

echo
echo "$i clips in $OUT/"

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
A customer checks out. Two things have to happen: the order has to be saved, and the rest of the business has to be told so the confirmation email goes out. So the code saves the order, and then publishes a message. One order saved, one event delivered, one email sent. Nobody would question this in a review.
The order is committed. Then, before the publish, the process dies. A deploy landing mid request will do it. Now look at what is left. The order is in the database. It is real, and the customer will be charged for it. No message was ever sent, and no email will ever arrive.
Ask what would retry this, and sit with the silence. Nothing will, because nothing anywhere recorded that a message was owed. There is no failed send in a log. There is no error, because nothing errored. This is not a message that failed to send. It is a message that stopped existing.
The obvious answer is to publish first and save second. It does not close the gap; it moves it. Now a crash announces an order that does not exist. And wrapping both lines in a transaction does not help either, because a database transaction covers the database. It has no authority over a broker.
Here is the whole idea, and it is small enough to be disappointing. Write the message into your own database, as an ordinary row, in the same transaction as the order. Two rows, one commit. So there is no instant at which one exists without the other. And then the order service stops. It does not call the broker at all.
A separate process, the relay, sweeps the out tray. Read the unsent rows. Publish each one to the broker. Mark each one sent. That is three lines of work, and it happens later, in a different process, long after the customer has gone. The email goes out exactly as before.
Two customers check out while the broker is completely unreachable. Both checkouts succeed, because neither of them ever needed the broker. They wrote two rows to a database and went home. In the version we started with, a broker outage was a checkout outage. Here it is a queue getting longer.
The first sweep tries both messages and the broker refuses both, so nothing is marked sent and both rows stay where they are. The broker comes back, and the second sweep publishes them. Now go and look for the retry logic, because there is none. An unsent row is still an unsent row, and that is the entire mechanism.
The relay publishes a message. The broker takes it and the email goes out. And then the relay dies, before it can write down that it had sent it. The row is still marked unsent, because nothing ever marked it. So the relay restarts, finds the message still sitting there, and publishes it again.
Publishing and marking as sent are in two different systems, so there is a gap between them, which is the same gap this pattern was invented to close, reappearing inside the fix. What you can choose is the direction. Mark the row sent first, and a crash loses the message forever. Publish first, and a crash sends it twice. This pattern publishes first, on purpose.
The duplicate is not fixable here. It belongs to whoever receives the message. What this side owes them is the ability to spot it, and it provides exactly one thing: the message id was identical both times. Same id, same message, so a receiver that remembers which ids it has handled can throw the second one away.
Three promises and one refusal. The order and its announcement are one atomic act. Checkout keeps working when the broker does not. And every message is delivered eventually, without anybody writing a line of retry logic. In exchange: some latency, a relay to run, a table that grows, and the same message will sometimes arrive twice. Never lost, sometimes twice.
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

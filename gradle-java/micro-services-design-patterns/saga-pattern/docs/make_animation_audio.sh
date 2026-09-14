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
A checkout is five things, in five different places. A customer buys a kettle. Reserve the stock, take the payment, create the order, schedule the shipment, send the confirmation email. Five steps, and each one lives in a different service with its own database. Run them in order and it works: seventy pounds and ninety five pence, an order number, a parcel booked, an email sent. Two hundred and fifty milliseconds end to end.
Read the one line that makes the rest necessary. No transaction spanned any of that. Each step committed on its own, immediately. By the time the payment is taken, the stock reservation is already final and nothing is holding it open. By the time shipping is called, the money has already left the customer's account. There is no single thing you can roll back, because there was never a single thing.
The courier refuses, and the try block shrugs. No courier covers the delivery address. The fourth call throws. The code that made all four calls has them inside one try block, so the catch runs, writes a line to a log, and returns null. Now count what is left behind: the card has been charged seventy pounds ninety five, a kettle is still reserved, the order says confirmed, and no parcel exists. The customer has paid for something that will never be sent, and nothing anywhere failed.
At transactional covers its own database and nothing else. This is the misconception worth being blunt about. That annotation wraps the method in a transaction on the database this service owns. It has no reach into the stock service's database, none into the payment service's, and none at all over the card network. Rolling back a transaction that never touched the money does not bring the money back. There is a technology that spans all five, called two phase commit, and almost nobody uses it, because every participant holds a lock while it waits for the others, and one slow courier then stops the shop.
A step that carries its own undo. Here is the whole mechanism. Every step is an object with four things on it: a name, an execute, a compensate, and a question, can this be compensated at all. Reserve stock, release stock. Take the payment, refund it. Create the order, cancel it. If that shape feels familiar, it is the Command pattern's execute and undo under different names. One difference matters enormously: an in memory undo always works, and a compensation is a call to somebody else's service that can be refused.
Forward, keeping a list. The orchestrator runs the steps in order, and after each one succeeds it writes that step down. Stock reserved, note it. Payment taken, note it. Order created, note it. Nothing here is held open or locked; every one of those is committed and final the moment it returns. The list is not a transaction. It is a record of what will have to be undone if the next call goes wrong.
The same refusal, and this time it is walked backwards. No courier covers the delivery address, exactly as before. The orchestrator stops going forward and starts walking its list in reverse. Cancel the order. Refund the payment. Release the stock. Three undos, in the opposite order to the three steps that succeeded, and then an outcome saying so: compensated, the customer owes nothing.
In reverse, because later steps lean on earlier ones. The order is cancelled before the money is refunded. Do it the other way round and there is a moment where finance is looking at a confirmed order with no payment against it. The stock is released last, because the reservation is what made every step after it legal in the first place. Reverse order is not neatness; it is the only order in which each undo is safe.
Now look at the ledger, because it has two lines. This is the part most explanations leave out. The payment ledger does not show nothing. It shows a charge of seventy pounds ninety five, and a refund of seventy pounds ninety five. Two lines, not zero. The net is zero and the history is not. The customer watched the money leave their account and come back, may well ring up to ask why, and in a real shop the card network keeps its fee. A rollback leaves no trace. A compensation is a new fact that cancels out an old one. Compensation is not rollback.
What if the refund fails as well? Sit with that question before the answer, because it is genuinely uncomfortable. The payment service does not answer. The money cannot be given back. Two things happen, and both are deliberate. The unwinding carries on regardless, so the order is still cancelled and the stock is still released, rather than leaving more broken than it had to. And the outcome says so out loud: there are three answers, not two, and the third is needs human help. The shop is holding money it is not entitled to, and the one useful thing left is telling somebody.
And some steps cannot be undone at any price. Move the confirmation email earlier, before the shipment is booked, and run the same failure. Everything unwinds correctly. The order is cancelled, the money is refunded, the stock goes back. And the customer is sitting there holding an email that says their order is confirmed, which it is not. There is no unsend. There is no compensate that can help. The only fix available is a second email apologising, which is, once again, a new fact rather than an erasure.
What you get, and what you hand over for it. A saga gets you this: each step commits on its own so nothing holds a lock across a network, a failure leaves the shop consistent rather than half finished, and when it cannot be fixed automatically somebody is told rather than nobody. You hand over three things for it. The undo leaves a trace, two lines in a ledger and a confused customer. The undo can itself be refused, which is why there are three outcomes and not two. And anything that cannot be undone at all has to go last, after everything that might fail.
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

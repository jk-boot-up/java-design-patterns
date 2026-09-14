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
The page, composed on every view. A customer opens their order history page. It is assembled from two services: ask Orders what this customer bought, which comes back as product codes and quantities with no names on it; then ask Catalog what those codes are called, once, for all of them; then stitch the two answers together. That is API Composition, done properly. The catalog call is batched. There is no loop. Ninety milliseconds, and two live service calls.
Be fair to this, because it is current and it is safe. Notice what composing gives you, because the rest of this is the story of handing it back. What you read is true right now, because it was fetched a moment ago from the services that own it. And you may sell from it: if it says a kettle is available, a kettle was available when you asked. Nothing here is eventually anything. The only thing wrong with it is the bill.
The same page, again, and again, and again. An order is placed once. Its page is opened by the customer, then from the confirmation email, then by a support agent, then by the customer's phone, then again next week. The underlying facts changed once. The shop paid to discover them a thousand times. Three views here cost two hundred and seventy milliseconds and six service calls, and every one of them rebuilt a page identical to the last.
The tempting fix: put a cache in front of it. Everybody reaches for the same thing, and it works. The first view composes and is stored; every view after that is free. Reads are suddenly cheap, and the shop stops calling Catalog for a page it has already built. This is not a straw man. It is a real cache with a real expiry, and there is a passing test that proves the second view costs nothing.
Catalog renames the kettle. The catalog team renames it from Stainless Steel Kettle to Brushed Steel Kettle. It is their product and their name. Somewhere an event goes out announcing it. The cache is not listening, because a cache cannot listen. It is not a subscriber; it is a box that remembers what it was handed. It now holds a name that stopped being true, and it does not know.
The only thing that will ever fix it is a timer. This is the sentence to take away. A cache is a copy that cannot know it is wrong. Nothing about the world can correct it: not the rename, not the event, not the team who made the change. The only correction available is the clock running out, five minutes from now. And you cannot tune your way out of that. A short expiry throws away the savings you bought the cache for, and a long expiry means being confidently wrong for longer. There is no free setting.
So let the write side announce what it did. Here is the question that turns into the pattern. What if the copy were kept up to date by the same events that changed the truth? Not a timer, but the actual facts. An order was placed. A product was renamed. Stock changed. Something listens to those, does the composition once, and keeps the finished rows ready. Commands change things, queries read things, and they stop being the same code path. That is all Command Query Responsibility Segregation means.
The work did not vanish. It moved. Be honest about this, or the pattern is a magic trick. Catalog was still called, once, when the order was placed. The composition still happens; it happens at write time instead of at read time. That is only a good trade because of the ratio: a shop places one order and shows that page a thousand times. Invert the ratio, write far more often than you read, and this pattern is a straightforward loss.
The same rename, and this copy is corrected by the fact. Run the rename again, this time against the read model. The event that makes the copy wrong is the same event that corrects it, and it arrives immediately rather than in five minutes. The cache next to it is still saying the old name. Both copies are fast. Only one of them can ever be told. And there is a second prize that is easy to miss: a page served from the read model calls no other service, so it keeps working when Catalog is down.
And now the bill: a paid order, on an empty page. The events take time to arrive, and for as long as they are in flight the copy is behind. Watch the worst frame of it. An order is placed, paid for and final, and the customer is looking at an order history page with nothing on it. Nothing is broken. The events have not been delivered yet. This window is real, you cannot code it away, and you have to decide page by page whether you can live inside it.
The rule: never decide a sale from a read model. Here is the part that has to survive production. There is one kettle left, or rather there is not. The ledger says zero, and the read model, still inside its window, says one. A second shopper arrives and tries to buy it. Nothing bad happens, and the reason is the only reason: the sale was not decided by the read model. It was decided on the write side, against the ledger that holds the actual number, and the ledger refused. Show a read model's stock number. Never sell against it.
The consolation: a read model is throwaway. And one last thing, which is genuinely liberating. A read model is not data you have to protect. It is derived. Delete it, replay the events, and it comes back exactly as it was, rebuilt here from six events, with two rows returned. That means you can change the shape of a page whenever you like and rebuild the projection from history. The write side holds the truth, it does not care whether anybody is projecting at all, and everything on the read side is a convenience you can throw away and make again.
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

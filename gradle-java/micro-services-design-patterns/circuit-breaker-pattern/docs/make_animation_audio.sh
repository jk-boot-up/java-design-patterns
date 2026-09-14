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
A service that has stopped answering. The product page shows an espresso machine, and underneath it a row of suggestions from a separate Recommendations service. This morning, Recommendations has stopped answering. Not refusing, which would be easy. It accepts the connection, says nothing, and three seconds later the call gives up with a timeout. Every call, for as long as the outage lasts.
So try again? That is the wrong question. The instinct is to reach for the pattern that worked last time. The call failed, so make it again. Three attempts, three timeouts, nine seconds. And the page the shopper finally gets is identical to the page they would have had at zero seconds. Every one of those nine seconds bought nothing, and a service already on its knees has just received three times the traffic.
The third cost is the one that takes the shop down. For those nine seconds, a request thread is sitting idle, waiting for an answer that is not coming. Threads are finite. A thousand shoppers browsing product pages during the outage are a thousand threads held open on a feature nobody needs. And when they run out, checkout stops working too. Say that plainly. The espresso machines stop selling because the suggestions are broken.
A fuse box, and one word that reads backwards. When something is badly wrong with the wiring, the fuse trips, and it stays tripped. It does not flick itself back on hopefully every few seconds. Later, somebody walks over and flips the switch back on, once, to see. That is the whole pattern. One piece of vocabulary first, because it catches everybody. Closed is the healthy state. A closed circuit is one where current flows, so calls go through. An open circuit is a broken one. If that feels the wrong way round, you are thinking of a door. Think of a wire.
Count the failures, and only the consecutive ones. While the breaker is closed, every call goes through and failures in a row are counted. One, two, three. Note the word consecutive. A success does not merely stop the count, it resets it to zero. A service that answers three times and fails once is not down. It is a service having a bad moment, and that is the retry pattern's job, not this one's.
Three in a row, and it trips. The third consecutive failure opens the breaker. It notes the time and it stops calling. From this moment, nothing reaches Recommendations at all, for five seconds. And the point of tripping is not to punish Recommendations. It is to stop one broken feature consuming the threads that the rest of the shop needs.
Now read the clock, and watch it stop. The fourth shopper arrives, the breaker refuses without making a call, and the page goes out without suggestions. Look at what stopped happening. The clock stopped moving. Nine thousand, nine thousand, nine thousand. Once the breaker is open, a page costs nothing at all to serve. Six pages, three calls made, three refused, and every one of those pages is a page somebody can buy from.
It protects everybody except the people who find out. Be honest about the trade, because it is the thing most descriptions skip. The first three shoppers paid three seconds each. A breaker never protects the people who discover an outage. It protects everybody after them. What it prevents is the outage being rediscovered, at full price, by every single shopper for as long as it lasts.
Five seconds later, one call finds out. The wait is over, so the breaker moves to half open and lets exactly one call through. It works, so the breaker closes, and normal service resumes. Nobody was paged, nobody logged in, nobody deployed anything. And notice how cheap the probe is. One call. Had Recommendations still been down, that single shopper would have waited three seconds, the breaker would have reopened for another full five, and everybody else would have carried on being served instantly.
Now the half that gets left out. Here is the sentence the rest depends on. A breaker does not make failures disappear. It makes them fail fast. And what that speed buys you depends entirely on what you were calling. On the product page, speed bought a fallback, because suggestions are optional, and an empty row of them is a true statement. At checkout there is nothing to fall back to. There is no substitute for taking the money.
So is the breaker worth having there at all? Yes, and this is the part worth keeping. What it buys at checkout is a fast, honest no, instead of a spinner. Both messages say exactly the same thing. One arrives after three seconds and the other in a hundredth of a second, and telling somebody their basket is safe straight away is a genuinely better product. It also stops a thousand shoppers each holding a thread open to discover the same outage.
And the fallback that lies. This last class is wired identically to the honest one, and differs in one catch block. When payments cannot be reached, it returns a made up receipt. Nothing throws. No alert fires. Every dashboard is green, the shopper is thanked, and the warehouse ships an espresso machine that nobody paid for. The rule that tells the two fallbacks apart is one word. An empty list of suggestions is true. A receipt for money that never moved is not.
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

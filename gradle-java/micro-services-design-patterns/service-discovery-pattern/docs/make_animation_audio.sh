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
One service, three copies of it. Pricing is busy, so it runs as three copies of the same program. Any of the three can answer any question, and all three give the same answer, because the price of an espresso machine does not depend on which machine you ask. The checkout needs a price, and so it needs an address. Which of the three does it call, and how does it know?
Writing the address down works, at first. Somebody pasted pricing one into the checkout, and it was the right amount of code at the time. It is fast, it has no dependencies, it cannot be misconfigured, and every test written against it passes. The price comes back in ten milliseconds.
Then somebody deploys pricing. A rolling deployment stops pricing one. That is not a fault; that is Tuesday. And the checkout is now down. Not slow. Down. Because the only thing it was ever told was the name of a machine that no longer exists.
And two healthy instances sit idle. Pricing two and pricing three are up, healthy, and doing nothing, three metres away in the same rack. The client cannot use either of them, and no amount of care inside that client would help, because a constant is not a question you can ask again later. The real problem is this: the set of running instances changes several times a day, and the source code of the callers changes once a fortnight.
So the instances keep the list themselves. Each one announces itself to a registry as it starts up, and then says still here every few seconds afterwards. Nobody edits a file. The list is written by the things it is a list of, which is the only way it can ever keep up with them.
The client asks, and then it calls. The discovering client does two things where the old one did one. First it asks the registry who is running, and it is offered three instances. Then it calls the first of them, and gets four hundred and forty nine pounds ninety nine, in the same ten milliseconds as before. One extra question is the whole mechanical cost of the pattern.
Now deploy again, and watch nothing break. Pricing one shuts down politely this time, so on the way out it takes itself off the list. The next lookup is offered two instances instead of three, and pricing two answers. The shopper never finds out that a deployment happened.
And scaling up needs no permission either. A fourth instance starts for a busy Friday, registers itself, and the very next lookup offers three. No code changed, no restart, no configuration edit. That sentence is the entire return on the pattern.
Then one of them crashes. Pricing two does not shut down politely. The process simply dies. And here is the thing that no design can get around: a process that has crashed cannot send a message saying it has crashed. So the registry does not know, and it goes on listing pricing two as though nothing had happened.
The client is handed a dead address, and copes. The lookup offers three instances, and the first one is dead. The client tries it, gets nothing, writes the word stale into the log, and moves down the list. Pricing three answers, five milliseconds later than pricing two would have. A stale entry cost five milliseconds instead of an outage, and the whole of that rescue is a loop and a caught exception.
Three seconds later, the list corrects itself. The living instances keep renewing their leases. The dead one cannot, and after three thousand milliseconds of silence its lease expires and it is dropped. That window is the honest price of this pattern. You can shorten it by sending heartbeats more often, and you cannot make it zero, because the only message that would close it is the one a dead process cannot send.
So: ask every time, and expect to be wrong sometimes. Instances put themselves on a list. The list forgets anyone who goes quiet. Callers ask it before every single call, so their picture of the world is never older than one request. And callers try the next name on the list, because a registry without a client that copes with stale entries fails every time an instance dies, which is exactly the situation it was introduced to fix.
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

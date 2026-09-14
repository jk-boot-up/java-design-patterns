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
One service, three copies of it, and one of them is slower. The Catalog service is busy, so it runs as three copies of the same program. Ask any of the three for a product name and all three give the same answer. They are not equally quick, though. Two answer in ten milliseconds, and the third takes sixty, because it is older hardware that nobody has got round to replacing. That unevenness is what makes the choice worth making.
The answer that costs no thought is to take the first one. The list arrives in some order, so take whatever is at the front of it. Nobody writes that down as a decision. It is what you get by reaching for the list, taking what is nearest, and moving on to the interesting part of the feature. So twelve requests go to catalog one, and catalog one alone.
Now read that total again, because nothing failed. One hundred and twenty milliseconds is the quickest result in this whole walkthrough. Nothing timed out, nothing threw an exception, every request got the right product name promptly, and every test written against this strategy passes. That is exactly why it survives in real systems. If you were waiting for an error, that expectation is the lesson.
What it actually costs is not on the clock. Two machines are billed every month, monitored, patched, and completely idle. The headroom the shop believes it bought does not exist. And when catalog one falls over, it takes every single request with it, while two healthy machines sit three metres away doing nothing. The failure mode is a bill, and a box that dies under a load the other two could easily have absorbed.
So give the choice a name of its own. Pull the decision out of the caller and put it behind an interface with one method that matters: given every instance currently running, return the one to call. Four classes implement it, and each one is under thirty lines. This is the Strategy pattern, and the only thing new about it is that the choice is now about machines rather than business rules.
Take turns, and the split is perfect. Round robin is a counter and a modulus. No measurements, no configuration, and no knowledge of anything at all. It sends four requests to each of the three machines, which is as even as twelve requests can possibly be shared between three boxes.
But fair is not the same as fast. Three hundred and twenty milliseconds, against one hundred and twenty. Round robin cheerfully sent a third of the shop's traffic to the slowest machine the shop owns, because round robin does not know what slow means and nobody told it. It is still the right default: it cannot be misconfigured, and there is nothing in it to get subtly wrong.
Measure before you judge. The least latency balancer keeps a running average of how long each machine has taken, and prefers the lowest. But first it tries every machine exactly once, because a balancer that trusts a measurement it has not taken is round robin with extra confidence. Three requests in, it has one sample each: ten, ten, and sixty.
Then prefer the fast ones, and notice that nobody configured that. The remaining nine requests go to catalog one. The slow machine was asked exactly once: the once it took to find out that it was slow. One hundred and seventy milliseconds, instead of three hundred and twenty. And here is the sentence that justifies doing any of this inside the caller. Nothing configured those latencies. The client measured them, from its own requests, and a client in a different rack would have measured different ones.
Now the catch: a favourite, and then a stampede. Look at catalog two. It is exactly as fast as catalog one, ten milliseconds, and it received one request out of twelve. The tie broke towards whoever was measured first, so the client found a favourite and kept it. That is harmless with one client. Now picture a thousand clients measuring the same cluster. They all reach the same conclusion, they all crowd the same machine, they make it slow, and then they all leave it together. A learning balancer needs a random tie break, or it will herd.
Two well behaved clients, and one idle machine. Run two clients, each with its own round robin balancer, two requests each. Both behaved impeccably. Both took perfect turns. Between them they left catalog three with nothing at all to do. So which client made the mistake? Neither did. The counter lives inside one client, so it counts one client's requests, and two counters that each start at zero are correct twice over and wrong collectively.
Choose every time, and know when to stop choosing. Several identical machines means a choice, and it is remade on every request. Taking the first one is fast, correct, and runs the shop on a third of what it owns. Take turns and you get fair, which is not the same as fast. Prefer the fastest and you get speed, paid for with the risk of a herd. And when no single caller can see enough to choose well, the answer is not a cleverer client. It is one balancer in front of the cluster, seeing every request, which is simpler and the right answer more often than this pattern's fans admit.
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

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
Two jobs, and one pot of threads. A shop runs on one application with one thread pool. Two of the jobs it does matter here. Checkout takes a shopper's money. It is fast, it is correct, and nobody has ever filed a bug against it. The supplier feed imports a catalogue overnight. Nobody is waiting for it, and if it finished an hour late, nothing bad would happen. Both of them ask the same pool for a thread. That is an entirely ordinary way to build a service, and for a long time it is the right one.
The partner API goes slow, and a waiting job holds its thread. One night the partner A P I that the feed calls stops answering promptly. Not failing. Answering, but slowly. And here is the fact that everything else follows from. A job that is waiting still holds its thread. It is using no processor time, it is doing nothing whatsoever, but that thread belongs to it until the call comes back. The first import batch starts, and takes one.
And then there are none. Batch two, batch three, batch four. Each one makes its call, each one waits, and each one holds a thread. Four batches, four threads, and the pool has four threads. Nothing here has failed. Nothing has thrown. Every one of these jobs is behaving exactly as designed, and the pool is behaving exactly as designed, and the shop is about to stop selling.
A shopper tries to pay. Now checkout needs a thread, and there is not one. So look at the program output, and read what is missing rather than what is there. There is no line for checkout. Not a slow line, not an error line. No line at all, because it never started. Absence is the symptom, and that is precisely what makes this so hard to diagnose while it is happening. There is nothing in the log to read.
And checkout was never broken. It would honestly be easier if checkout were faulty. It is not. There is a test in this project that takes exactly the same checkout job, runs it the moment a thread is free, and watches it complete perfectly. It was starved, not broken, and from outside those two look identical. So the sentence that matters is this one. The shop stopped selling because of a background job that nobody was waiting for. And notice how invisible that is. Neither job mentions the other. No import, no call, no shared field. They are coupled only by a resource that neither of them names.
The first tempting fix. Make the pool bigger. Four threads was too few, so use forty. That buys time and nothing else. Whenever the partner is slow enough for long enough, the feed will take forty threads instead of four, and checkout will be starved at forty exactly as it was at four. The number changes. The failure does not. And it is worse than a draw, because the bigger the pool, the longer it takes anyone to notice, and the more memory the eventual pile up consumes.
The second tempting fix. Never refuse anything. Somebody suggests an unbounded queue. Never turn a job away, just let them all wait their turn. That sounds generous, and it is the more dangerous of the two. What it actually does is convert a fast, visible failure into a slow, invisible one. Jobs pile up until the process runs out of memory, and every caller sits waiting for work that will not start for minutes. A queue that never says no is not generous. It is a slow leak with good manners.
The actual fix, and it is a let down. The two jobs are connected only by the pool they share. So stop sharing it. Give the feed two threads of its own, and checkout two threads of its own. That is the entire mechanism. A fixed pool, a bounded queue, and a name for the worker. There is no algorithm here, nothing adaptive, nothing to tune at runtime. Say it out loud, because it is the point. A bulkhead is not a clever piece of machinery. It is a decision to stop sharing, and the pattern lives in having two of them, rather than in anything either one does.
The same outage, and the shop keeps selling. Same slow partner, same four batches, same instant. Two batches run and two wait for a feed thread. And checkout asks for a thread, and gets one immediately, and the shopper pays. Read the thread names, because they are the entire argument. Feed worker, and checkout worker. Those are different threads, and no amount of demand on one side can produce a thread on the other.
Do not celebrate yet. Is the feed still stuck? Here is the question worth asking before believing any of this. How do we know the partition did that, and not the partner API quietly recovering at the convenient moment? A lucky run would look exactly the same. So there is a test whose whole job is to assert that the feed is still jammed, two threads busy and two jobs queued, at the instant the sale goes through. Without it, you have not shown isolation. You have shown a coincidence. Nothing about the partner was fixed. That is the claim.
A fifth batch arrives with nowhere to go. Two threads busy and a queue that holds two, so four batches fit. A fifth is refused, and the refusal comes back in zero milliseconds. That feels hostile, and it is the opposite. The caller finds out instantly and still has time to do something useful. Shed the batch, degrade, write it down for tonight. It is the circuit breaker's fast failure, applied to a queue rather than to a broken service. Refusing is a feature.
And now the bill. One last picture, and it should be uncomfortable. On a quiet afternoon, the feed has two threads busy with two jobs queued behind them, and checkout has two threads sitting completely idle. Two threads doing nothing, beside two jobs waiting for a thread, and they are not allowed to help. One shared pool of four would have run all four batches at once and finished the import sooner. So partitioned pools are idle capacity by design. Not a bug, not a tuning problem. That is what you are buying with. Draw the walls along what must survive, keep it to two or three, and be able to say the price out loud.
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

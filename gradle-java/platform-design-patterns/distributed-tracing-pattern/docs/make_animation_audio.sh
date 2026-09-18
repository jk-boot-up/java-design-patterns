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
# span ids are spaced so the voice does not run them together, and the key
# takeaway is spelled out a little more plainly than the caption does.
#
# One line per step, and the count must match the STEPS array. If you copied
# this file from another pattern, replace every line below before running it.
narrate() {
cat <<'EOF'
A customer opens the page for a product, and it takes nine hundred milliseconds. Four services contributed to it: catalog, pricing, inventory and recommendations. Every one of them is healthy, every one of them is writing logs, and nobody can say which of the four is at fault. There is one measurement in this picture, and it is the complaint.
Here are six lines from the merged log. Two customers are on the site at once, so there are two quote started lines and two quote complete lines. Subtract the first finish from the first start and pricing took a hundred and eighty milliseconds. Subtract the second and it took two hundred and twenty. Both look reasonable, and one of them pairs one customer's start with another customer's finish. Nothing on any line says which is which. The missing thing is not more detail. It is an identifier.
So the first service to see the request makes one up. A trace id, generated at the front door, put on every call the page makes, read and passed on by everything downstream. That alone fixes the pairing, because the merged log can now be filtered down to one customer. It still does not say where the time went, because a filtered log is still just a list of timestamps.
Now each unit of work records a span. Catalog, pricing and inventory each open one as they run. A span is four things: a name, a start, a duration, and the important one, the id of the span that caused it. All three of these name span one, the page itself, as their parent. That parent field is what will turn a flat list into a shape.
And it nests. Recommendations runs for four hundred milliseconds, and inside it a ranking model runs for three hundred and forty. The model's span is opened from recommendations' own context rather than the page's, so it becomes recommendations' child and sits one level deeper. That single argument is the difference between the answer recommendations is slow and the answer the scoring model inside recommendations is slow. Only one of those tells anybody what to fix.
Here is the whole trick. The page span lasted the full nine hundred milliseconds, so on total time it is the biggest thing here, and it always will be. Subtract the time each span spent waiting on its children, and the page's own work is zero. It did nothing. It waited. Recommendations lasted four hundred and is charged only sixty, because three hundred and forty of them belong to the model it called.
So the question from the start has an answer. The ranking model is three hundred and forty milliseconds, thirty-seven per cent of what the customer waited for. Recommendations as a whole, the model plus its own work, is four hundred milliseconds, forty-four per cent of the page. Nobody computed that while the request was running. It was computed afterwards, from seven spans, by subtraction, which is why a trace can answer questions you did not know you were going to ask.
Now the bill, and there are three items on it. The first: recommendations is well behaved in every respect but one. It never opens a span of its own. It still receives the trace context and still forwards it faithfully, so nothing errors and nothing warns. Watch what happens to the picture. The four hundred milliseconds did not disappear. It landed on the parent.
And that is worse than a gap. This trace has one root. It has no orphans. Every millisecond is accounted for. By every check you would think to run, it is healthy, and the service actually responsible is not on the diagram at all. So somebody spends the afternoon reading the page renderer. Partial instrumentation is worse than none, because none tells you nothing, and partial tells you something false, confidently, with a diagram.
The second item. The recommendations call is moved onto a worker thread, so the page can get on with other things meanwhile. The context lives in a thread-local, which belongs to a thread and does not travel, so the worker asks for it and is handed nothing. It opens its span with no parent. Two roots in one trace, four hundred milliseconds belonging to nobody, no exception and no warning.
The fix is one line, moved earlier. Read the context on the thread that has it, and hand it to the task as an ordinary value. A value does not care which thread reads it. Same two spans, same four hundred milliseconds, and now one root, with the recommendations strip hanging off the page where it belongs. The broken version and this one are the same code with one line in a different place, which is exactly why this failure catches everybody.
The third item. A thousand requests a second, at six spans each, is half a billion spans a day, and nobody pays for that. So the front door keeps one trace in a hundred. A million requests today leaves ten thousand traces kept and nine hundred and ninety thousand gone. Then a customer complains about request number eight hundred and sixty-two thousand, one hundred and forty-four. It was discarded, at the front door, before anybody could know it would matter. The way out is tail sampling: hold the spans, let the request finish, and decide to keep the trace once you know it was slow.
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

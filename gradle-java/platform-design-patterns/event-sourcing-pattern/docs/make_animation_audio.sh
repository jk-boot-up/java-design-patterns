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
The same customer, stored two ways. One shopper, one loyalty scheme, one point for every pound. On the left is the design nearly everybody writes: a row with a number in it. On the right, the same shop keeping the list of things that happened instead. Nothing has happened yet, so both are empty.
An order earns sixty points. The row adds sixty and is finished. The log appends a fact: sixty points were awarded on the first of March, for order O-R-D eighty-eight oh one. Now look at what the row did with that order number and that date. It was handed both, it used neither, and they are gone.
Three more things happen in March. Twenty-five points spent on the third. A hundred and twenty earned on the eighth. Fifteen lost to the twelve-month expiry on the fourteenth. The row is now a hundred and forty. The log is four facts, and the balance is nowhere in it.
The customer asks why it is a hundred and forty. This is the whole answer the row can give: the row says a hundred and forty points, and how it got there was never written down. The four things that happened in March were each added to a number and then forgotten. There is nobody left to ask.
The log answers by adding itself up. Start at zero and walk the events in order. Sixty. Then thirty-five. Then a hundred and fifty-five. Then a hundred and forty. Each line says what happened and what the balance became, including the expiry, which is the call support dreads most. That is not a stored explanation. It is the sum, printed as it goes.
And what was it on the third of March? The same walk, stopped earlier: skip anything dated after the day being asked about. Thirty-five points. Nobody planned for that question, nobody built a history table for it, and the answer was already lying in the data.
A release awards points twice. A bug goes out and one order earns its points twice over. Nobody notices for three weeks. On the left the row simply becomes two hundred and thirty, and a doubled forty-five pound order now looks exactly like one honest ninety pound one. On the right there are two events, both of them true, and two events never look like one.
A query written three weeks after the bug. Nobody wrote this before the release. It is written now, against data that was already there: group the awards by order number, and report any order that earned points more than once. Order O-R-D nine thousand and one, awarded twice. The row cannot be asked this, because there is nothing there to ask.
The repair changes the reading, not the log. Count each order's award once and the balance is a hundred and eighty-five again. Now look at the log. Nothing was edited, nothing was deleted, and both events are still drawn there. The shop really did award twice, so the log was never wrong. What was wrong was the interpretation, and that is what got fixed.
The bill, part one. Reading a long log costs. Four events is nothing. Five thousand is not. Folding from the beginning to answer one balance reads all five thousand of them, every single time somebody asks. The fix is a snapshot: save the balance as at event five thousand, and the next read walks one event instead of five thousand.
And a snapshot is a second place a balance lives, which is the thing the pattern set out to avoid. A snapshot written by code that turned out to have a bug stays wrong forever, and nothing throws, because a wrong balance is just a number. That is why it records which code computed it. The cure is to throw every snapshot away and add the log up again, and that cure is cheap only because the log kept everything.
The bill, part two: erasing, and old events. A customer with a legal right to be forgotten meets a log that has no delete. Removing their events destroys the history that explained them, and a snapshot taken earlier still reports their balance, so the data is still in the building. And a field somebody added in twenty twenty-three is missing from every event written before it, permanently, so the duplicate hunt finds nothing in a log that plainly contains two identical awards. Store the facts, derive the total, and know what it costs.
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

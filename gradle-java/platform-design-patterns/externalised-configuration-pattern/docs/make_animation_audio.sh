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
#
# One line per step, and the count must match the STEPS array. If you copied
# this file from another pattern, replace every line below before running it.
narrate() {
cat <<'EOF'
Free delivery when you spend over fifty pounds. The number is a named constant in the checkout class: one place, correctly typed, and a reviewer would approve it without a comment. The sixty-two pound basket ships free. The forty-eight pound one pays four ninety-nine, and so does the thirty-one fifty one. Nothing here is wrong.
Then marketing wants thirty-five pounds, from Saturday morning. They ask on Friday at half past four. Editing the constant takes fifteen minutes, and then a code review, a build, an approval and a deploy: two hours and a quarter of work altogether. But the release window closes at five and does not reopen until Monday, so the change goes live on Monday at a quarter to eleven. The promotion was for the weekend. It is late by two days and nearly two hours.
So the number moves outside the program. Same arithmetic, one line different: instead of reading a constant, the checkout asks a settings reader for the threshold, and it asks inside the quote rather than once when it is built. Nothing is configured yet, so every quote falls back to the default compiled into the code. The shop behaves exactly as before.
Now somebody types thirty-five into a box. Four seconds later the very next basket is quoted against it, and order seven one zero two, forty-eight pounds, ships free. No rebuild. No redeploy. No restart. Against two days and change, that is the whole reason anybody does this.
Then the config server stops answering. The network link to it drops. Every setting falls back to the default compiled into the code, and the shop starts, and keeps selling, which is the point of carrying a default at all. But listen to what it quietly lost. The threshold is back to fifty pounds, the promotion is off, and no exception, no log line and no alert says so anywhere.
Now the bill, and there are two items on it. Saturday morning, nine twelve, and somebody types minus one. The server stores it happily, because storing text is all a config server does. Every basket in the shop is worth more than minus one pound, so every basket ships free, including the thirty-one fifty one. There is no exception. There is no log line. Nothing reports a problem, because as far as the program is concerned there is not one. The first symptom is the margin.
Eight minutes later, somebody types the word fifty. Not a number at all. The read throws, nothing catches it, and the exception travels straight out through checkout. Not one basket can be quoted. The shop is down, and it was taken down by a text box, with nothing deployed. In one sense this is the better of the two failures, because you find out immediately.
The repair is to declare the setting and validate it at the boundary. A key, a default, a lowest value and a highest value. Five pounds to two hundred: below five you are giving delivery away on a packet of crisps, and above two hundred nobody ever qualifies, so the promotion is broken the other way. Both ends are business judgements, which is exactly why a program has to enforce them. This little record is the replacement for the compiler.
The word fifty again, with validation switched on. The same bad value is still configured, and now something reads it properly. It is refused at the edge, the rejection is recorded, and because this reader has never yet seen a good value there is nothing to keep, so the default in the code keeps the shop selling. Nobody sees an error page.
Thirty-five pounds again, and this time it passes. The reader uses it, and it also files it away as the last value known to be good. That filing is about to matter more than it looks.
Eleven forty on Saturday, and somebody in operations types minus one. It is refused, and listen carefully to what the shop falls back to: not fifty pounds from the code, but thirty-five, the last value that passed. Reverting a perfectly good promotion because of an unrelated typo would be its own kind of wrong. And the rejection is recorded, loudly, because a guard that swallows bad input in silence leaves the typo in place and nobody looking for it.
Finally, a rollback as fast as the change. Four seconds after the decision the threshold is back to thirty-five, and nobody had to remember what it used to be, because every entry in the trail records the value it displaced. The same correction through the release pipeline would have been live on Monday at a quarter past eleven. That is the guard with no equivalent in the source-code world: a bad release takes a release to undo, and a bad value takes four seconds. Externalised configuration is not a way to avoid governing a change. It is a way to govern it in seconds instead of days.
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

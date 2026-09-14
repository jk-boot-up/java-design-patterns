#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice used in the
# teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-7.m4a
#
# Requirements: macOS (for `say`) and ffmpeg.
#
set -euo pipefail

cd "$(dirname "$0")"

OUT=audio
VOICE="${VOICE:-Samantha}"     # female US English voice, matches the video
RATE="${RATE:-165}"            # words per minute

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

# Narration for each step. Kept in the same order as STEPS in animation.html.
# These are spoken versions of the on-screen text, with a little more warmth
# and the key takeaway spelled out.
narrate() {
cat <<'EOF'
NotificationDemo constructs an Order Confirmation Notification and hands it an S M S Channel. Neither class was written knowing about the other. They are just two objects, joined by a constructor argument.
send calls subject and body on itself. Those methods build a string. They never mention email, S M S, or push. The abstraction is completely ignorant of delivery.
send hands the composed subject and body to channel dot deliver. This one line is the entire bridge between the two hierarchies. Everything past it is the implementor's problem.
S M S Channel checks the combined length against its one hundred forty character limit and truncates with an ellipsis if needed. This rule lives in exactly one place, regardless of which notification type triggered it.
Construct the same Order Confirmation Notification again, this time with an Email Channel. Nothing about Order Confirmation Notification changes. Only the object passed to its constructor.
Push Channel implements the exact same deliver method, but discards the body and shows only the subject. Three completely different behaviors, zero changes to any Notification subclass.
Password Reset Notification is a brand new class, written without touching Email Channel, S M S Channel, or Push Channel, and it already works with all three. That is the entire payoff of Bridge.
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

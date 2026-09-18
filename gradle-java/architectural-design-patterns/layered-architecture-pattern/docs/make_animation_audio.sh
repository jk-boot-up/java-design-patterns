#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-5.m4a
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

# Narration for each step, in the same order as STEPS in animation.html.
# One line per step, and the count must match the STEPS array.
narrate() {
cat <<'EOF'
Act one. One class does everything: pricing, storage, payment and email, all in one place. There is no layer to light up here, because there is nothing yet to separate.
Act two. A customer checks out, and the call travels straight down through all four layers: presentation to application to infrastructure, building domain objects as it goes. Every box lights up green, in order, because every layer only ever calls the one directly beneath it.
Act three. Somebody needs an order history screen, and it reaches straight past application into storage. Watch the presentation box turn red, and watch application stay dark: it is never called at all. The screen compiles, the tests pass, and nothing in the build objects.
Act four. The rule is written down as a test: presentation may not depend on infrastructure. Widen that same rule to include the shortcut screen, and the build goes red, naming the class by name and the class it reached for.
Act five. The entire storage layer is replaced: a map keyed by order id becomes an append-only log. Watch the infrastructure box change colour while presentation, application and domain stay exactly as they were. Sixteen of seventeen classes across the four layers are never opened.
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

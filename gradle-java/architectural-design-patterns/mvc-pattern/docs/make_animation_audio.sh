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
narrate() {
cat <<'EOF'
Act one. One class checks stock, takes payment and formats the screen text, all in the same method. There is nothing yet for two outputs to disagree about, because there is only one output.
Act two. The controller places the order, builds a model from what was actually saved, and hands it to the screen. The screen has one import: the model. It does not know how the total was worked out.
Act three. A second view is added, and it reaches past the model into the catalogue, rounding each unit price to the nearest pound before multiplying. The burr grinder's eighty-nine pounds fifty becomes ninety. The screen says three hundred and eighty-two pounds fifty. The email says three hundred and eighty-three pounds. Nothing in the build objects.
Act four. The rule is written down as a test: no class in view may depend on infrastructure. Widened to include the naive package, the build goes red, naming the rounded email view and the catalogue class it reached for.
Act five. The real second view is added instead. It reads the same model the screen does, computes nothing, and the two totals agree, every time, because neither view is allowed to add anything up.
EOF
}

i=0
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

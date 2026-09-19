#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-6.m4a
#
# Requirements: macOS (for `say`) and ffmpeg.
#
set -euo pipefail

cd "$(dirname "$0")"

OUT=audio
VOICE="${VOICE:-Samantha}"
RATE="${RATE:-145}"

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

narrate() {
cat <<'EOF'
Act one. To check the total and the checkout rule, a screen was needed. One window was opened. The rules are welded to the widgets.
Act two. After two adds, the view was told: show the total, twenty five pounds fifty; show the count, two; enable checkout. Windows opened: none. The rules were checked with no screen.
Act three. An empty cart: total zero, count zero, checkout off. Add one item and remove it, and the last three calls are the same. The presenter decides that checkout is off again. The view just obeys.
Act four. The screen starts as zero, no items, checkout off. After two adds it shows twenty five pounds fifty, two items, checkout on. Nobody told the screen. It bound once. The view model holds no reference to any view.
Act five. A phone screen and a watch screen bind to the same view model. Both show sixteen pounds, one item, checkout on. A second screen cost no change to the view model.
Act six. In M V V M, a screen that forgot to bind the total draws a question mark. Nothing failed. It is just wrong. In M V P, the view interface has three methods, and each new thing on the screen adds one to the interface, the presenter and every view. M V V M hides the wiring in the binding. M V P spells it out, and gets long.
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

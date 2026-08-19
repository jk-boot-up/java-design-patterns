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
Our client holds an express delivery object, but it only knows it as a delivery service. It calls ship, and that is the last decision it makes. It never names a courier class.
The ship method lives in the abstract parent, and it is final. Its first step guards the order. No weight, no shipment. This check is written once, and it protects every delivery tier that will ever exist.
Line two calls create courier. Now look carefully at the parent class. There is no body for that method. It is abstract. The parent has written a call that it cannot answer itself.
At runtime, the object really is an express delivery, so the call lands there, and it returns a new air courier. The other three tiers each answer differently, and none of them knows the others exist.
The courier travels back up into the ship method, typed as courier, not as air courier. The parent can call name, and dispatch, and nothing else. That is what keeps it free of every carrier.
Dispatch is called on the interface, and polymorphism does the rest. The sky link air code runs, priced and timed its own way. The workflow around it did not choose this behaviour.
The shared workflow logs the tracking number and hands back a shipment. Now imagine swapping express delivery for same day delivery. A different courier arrives, the price and the date change, and not one existing line is edited. That is the whole point of the pattern.
EOF
}

i=0
while IFS= read -r line; do
    i=$((i + 1))
    printf '%s' "$line" > "$OUT/.step-$i.txt"
    say -v "$VOICE" -r "$RATE" -o "$OUT/.step-$i.aiff" -f "$OUT/.step-$i.txt"
    ffmpeg -y -loglevel error -i "$OUT/.step-$i.aiff" \
        -c:a aac -b:a 128k -ar 44100 -ac 1 "$OUT/step-$i.m4a"
    rm -f "$OUT/.step-$i.aiff" "$OUT/.step-$i.txt"
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/step-$i.m4a")
    printf 'step-%d.m4a  %5.1fs\n' "$i" "$dur"
done < <(narrate)

echo
echo "Wrote $i clips to $OUT/"

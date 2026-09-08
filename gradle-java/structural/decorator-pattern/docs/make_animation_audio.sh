#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice used in the
# teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-9.m4a
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
Pricing Demo calls cost on the outermost layer it holds. Right now that happens to be an Express Handling Decorator, but the client's code never names any decorator directly. It only ever calls cost on a Priced Item.
Express Handling Decorator calls wrapped dot cost first, before adding its own nine dollar and ninety nine cent fee. It has no idea whether wrapped is a plain Product or another decorator.
Insurance Decorator also calls wrapped dot cost first. Its two percent premium will be computed on whatever number comes back. It is about to price the gift wrapped total, not the bare product price.
Gift Wrap Decorator calls wrapped dot cost one more time. This time wrapped really is the plain Product, the bottom of the stack.
Product dot cost simply returns seventy nine dollars and ninety nine cents. It was never written with any decorator in mind. It has no idea it's wrapped by anything at all.
Gift Wrap Decorator adds its flat three dollar and fifty cent fee to the seventy nine ninety nine it got back, and returns eighty three dollars and forty nine cents to whoever called it.
Insurance Decorator computes two percent of eighty three forty nine, the gift wrapped total, not the original seventy nine ninety nine, and adds that premium. This is why stacking order matters. Insurance prices whatever it wraps.
Express Handling Decorator adds its flat nine dollar and ninety nine cent fee on top of eighty five dollars and sixteen cents, and returns the final total to Pricing Demo.
Four independent classes, Product plus three decorators, combined into one total, with zero combination specific classes. Reorder or drop any layer and every other layer's code stays exactly the same.
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

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
Product Image Demo calls render on a Restricted Product Image set to the admin role. The client's code never touches Lazy Product Image or High Resolution Product Image directly. It only ever calls render on a ProductImage.
Restricted Product Image checks whether the role is admin before doing anything else. This request passes. Notice that the check happens before the call is allowed anywhere near the real image.
With the role check passed, Restricted Product Image calls render on the Lazy Product Image it wraps. It has no idea whether that ProductImage is lazy, cached, or something else entirely.
Lazy Product Image checks whether real ProductImage is null. This is the first render call for this image, so the answer is yes. The expensive real subject has not been built.
Lazy Product Image constructs a new High Resolution Product Image. This is the expensive step. The load count increments by one, and the instance is cached in the real ProductImage field for next time.
High Resolution Product Image's display method returns its string. It was never written with any proxy in mind. It has no idea anything is standing in front of it.
Lazy Product Image returns exactly what the real image returned, and Restricted Product Image does too. Neither proxy added anything. That is the tell that this is Proxy, not Decorator.
The client calls display again. The protection proxy checks the role again and delegates again, but this time real ProductImage is not null, so Lazy Product Image reuses the cached instance. The load count stays exactly where it was.
A second Restricted Product Image, set to the shopper role, calls render on its own fresh Lazy Product Image. The role check fails immediately. Lazy Product Image is never even asked, so the real image is never built and the load count never moves.
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

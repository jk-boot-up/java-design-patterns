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
Order sequence generator is an enum with a single constant, instance. The J V M creates it exactly once, during class loading, before any caller's code can even reference it. There is no constructor to call, because enum constants are not built by ordinary code.
Instance dot next order number increments an atomic long and formats the result. Because there truly is only one instance, it's reachable from every thread in the program at once, and atomic long is what keeps concurrent callers from ever landing on the same number.
Reflection can call a private constructor directly, unless the class is an enum. Constructor dot new instance on an enum's constructor is specifically rejected by the reflection A P I itself. No defensive code was needed in this project.
Serializing instance and reading it back does not rebuild a new object from its fields. The language defines an enum's serialized form as its name, and deserialization resolves that name against the existing constant. The same instance comes back.
Legacy order sequence generator uses the shape most singleton tutorials teach first. A private constructor, a static field, a public get instance. Under ordinary use it behaves identically to the enum, every caller gets the same shared instance back.
Get declared constructor, then set accessible true, bypasses the private access check that was the only thing standing between a caller and a second instance. Legacy order sequence generator has no special protection against this. Nothing about being a singleton is enforced by the J V M here.
Default Java serialization never calls a constructor at all, it rebuilds an object's fields straight from bytes. Implementing serializable without a read resolve method means a round trip mints a brand new instance, counter reset and all.
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

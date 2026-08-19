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
The client, our checkout service, already has a payment type. That is just data, from a dropdown or a JSON field. It hands that to the factory and asks for something it can use. It does not know the name of a single payment class.
The factory switches on the type. This one switch is the only place in the whole codebase that maps a type to a class. And because payment type is an enum and payment method is sealed, the compiler checks that every case is covered.
The U P I case wins, so the factory calls new upi payment. The other three are never touched. But notice, the factory is the only thing that knows they exist at all.
The new object travels back to the client, typed as payment method, not as upi payment. That single fact is what keeps the client decoupled from every concrete class.
Now the client uses it, knowing nothing. It asks for a display name, and because it is talking to an interface, this line reads exactly the same no matter which implementation arrived.
Pay is called on the interface, and polymorphism does the rest. The U P I code runs. The client never chose this behaviour. It only chose a type name.
A receipt comes back, and checkout is done. Now imagine changing U P I to pay pal. A different object arrives, the payment lines are different, and not one line of client code changes. That is the whole point of the pattern.
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

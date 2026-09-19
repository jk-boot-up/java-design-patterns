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
Act one. The payment service refuses its first two calls. Checkout retries three times, and succeeds. Refunds never retries, and fails. Reports retries once, and fails. Three services, three copies of the retry code, three different behaviours.
Act two. The same bad day, and the same policy for everyone. The call worked. The proxy made three attempts, and the checkout service has no retry code at all.
Act three. With three retries, the call works. One setting changed to zero, and it fails. Every service's calls changed. Services redeployed: none.
Act four. Checkout calls payments, and it works. An unknown service calls payments, and is refused. The payment service received one call. The proxy turned the other away before it got there. Denied: one.
Act five. Checkout to payments: two calls, none failed, four attempts. Refunds to payments: one call, none failed, one attempt. No service counted anything. The proxies did.
Act six. One call, with two refusals: the payment service received three calls. Retrying multiplies the load on a service that is already struggling. One attempt takes three ticks through the proxies, and one directly. This call took nine ticks. And three services means three more processes to run, upgrade and understand.
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

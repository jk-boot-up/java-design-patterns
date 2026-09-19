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
Act one. The payment service refuses its first two calls, for each caller in turn. With retry code of three, none, and one tries: checkout worked, refunds failed, reports failed. Three services, three copies of the retry code, three different behaviours.
Act two. Envoy is told to retry server errors up to three times. The checkout has no retry code, and the call worked. The payment service received three calls, and Envoy counts two retries.
Act three. One setting in Envoy's configuration is changed, from three retries to none. The same call fails. Services changed or redeployed: none.
Act four. Only checkout and refunds are allowed. Checkout gets a 200. Gift cards gets a 403. The payment service received one call: the proxy turned the other away before it got there. Here the caller's name is a header. A real mesh checks a certificate instead, which a service cannot forge.
Act five. Read from Envoy, and not from any service: requests to payments, three; retries, two; retries that ended in success, one. No service counted anything. The proxy did.
Act six. One call, with two refusals: the payment service received three calls. Retrying multiplies the load on a service that is already struggling. Every call now crosses a proxy, which is a second process and a second network hop. And the policy is in a configuration file of about forty five lines, that someone must read, and keep right.
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

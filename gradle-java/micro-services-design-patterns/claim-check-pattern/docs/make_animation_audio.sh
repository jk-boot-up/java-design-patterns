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
Act one. The invoice is five thousand bytes, and the broker refuses it: it is over its limit of a thousand.
Act two. The invoice goes to storage. The message carries a claim with a thirty seven character id, the size and a checksum. The receiver redeems it and gets the same five thousand bytes.
Act three. A hundred invoices carry five hundred thousand bytes through a broker with no limit, and five thousand nine hundred by claim.
Act four. Ten are sent and six collected and deleted, so four blobs are left. After the time limit a sweep removes them. A slow receiver who arrives later finds its blob gone.
Act five. One byte is changed in storage. The receiver checks the checksum in the claim, and refuses the payload.
Act six. One invoice now takes three storage operations and two broker steps, where it took one. Claims that count up let anyone read the next invoice, and random ones do not. And storing then sending can stop between the two.
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

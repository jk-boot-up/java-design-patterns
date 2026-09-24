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
Act one. The email service's queue is on Amazon SQS, played by LocalStack, and it takes messages of at most 1048576 bytes. A business customer's monthly invoice is a PDF of 1500000 bytes. A message has to be text, so the PDF is written out as base64, which is 2000000 characters. SQS refuses it. Even a PDF of 786433 bytes, under the limit, grows to 1048580 characters and is refused. 786432 bytes is the largest that fits.
Act two. Checkout stores the PDF in an S3 bucket under a random key of 36 characters, and sends only a ticket through the queue: 113 bytes of text naming the bucket, the key, the size and a checksum. The email service takes the ticket, fetches 1500000 bytes, identical to what was sent, then deletes the object and the message. Nothing is left in either.
Act three. Checkout sends 10 invoices by ticket. The email service collects 6, then stops. S3 still holds 4 invoices and SQS still holds 4 tickets. Then an 11th invoice is stored, and its send fails because the queue does not exist. Now S3 holds 5 invoices and SQS holds 4 tickets: 1 invoice has no ticket, and nobody will ever ask for it.
Act four. A bucket keyed by order number. Order 1042's invoice is stored and its ticket sent, then a corrected invoice is stored under the same key. S3 keeps 1 object, the new one. The first ticket's checksum does not match, and the email service refuses it. With versioning on, each store keeps its own version and the ticket names one: the first ticket gets the first invoice. But deleting the key leaves 0 keys listed, 2 versions still stored and 1 delete marker. Only deleting each version by its id brings it to 0.
Act five. The bucket gets a rule: remove every invoice 1 day after it was stored. A day is the smallest unit S3 takes, and it stamps the invoice to expire at a midnight UTC between 24 and 48 hours away. The queue keeps a ticket nobody has taken for 345600 seconds, which is 4 days. The demo removes the invoice as the rule would; 1 ticket is still waiting, and a slow email service that redeems it is told the key does not exist.
Act six. A 600000-byte invoice sent whole takes 3 requests, and the queue carries 800000 bytes. The same invoice by ticket takes 6 requests: store, send, receive, fetch, delete the object, delete the message. The queue carries 117 bytes. Twice the requests, two services to run and pay for, and a gap between storing and sending. The demo needed 1 container for 1 queue service and 1 storage service.
EOF
}

i=0
while IFS= read -r line <&3; do
    i=$((i + 1))
    printf '%s' "$line" > "$OUT/.step-$i.txt"
    say -v "$VOICE" -r "$RATE" -o "$OUT/.step-$i.aiff" -f "$OUT/.step-$i.txt"
    ffmpeg -y -loglevel error -i "$OUT/.step-$i.aiff" \
        -af "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11" \
        -c:a aac -b:a 128k -ar 44100 -ac 1 "$OUT/step-$i.m4a"
    rm -f "$OUT/.step-$i.aiff" "$OUT/.step-$i.txt"
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/step-$i.m4a")
    printf 'step-%d.m4a  %5.1fs\n' "$i" "$dur"
done 3< <(narrate)

echo
echo "Wrote $i clips to $OUT/"

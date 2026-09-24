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
Act one. There is no outbox yet. The checkout saves the order in Postgres, and then sends the event to Kafka itself. The process dies between the two. Order one is in Postgres, and Kafka has no event. The customer is charged, and nobody is told. Now swap the two lines. Send first, then save, and die in between. Kafka has one event, and order two is not in Postgres. The shop has announced an order that does not exist. Two systems, two steps, and no transaction that covers both.
Act two, the pattern. Postgres is started so that its log, the journal it writes every change into before touching a table, can be read from outside. Debezium holds a bookmark in that log, called a replication slot. The checkout writes each order and a row in the outbox table, in one transaction, and has no Kafka code at all. Debezium reads the three commits from the log and sends three events. Then order four writes both rows, the card is declined, and the transaction rolls back. Order five commits after it. Kafka now holds four events, and none for order four. The log only hands over committed work.
Act three, the headline. This time each transaction writes the outbox row and deletes it again, before committing. Three orders. The outbox table ends with no rows at all. Kafka still receives three events. Debezium never looked at the table. It read the inserts from the log. A relay that polls the table would have found nothing to send.
Act four. Debezium is stopped, and its slot has no reader. The checkout still takes three orders, and Kafka receives nothing. Meanwhile Postgres keeps every part of its log that Debezium has not confirmed, and the log it keeps for the slot grows. The limit on that is minus one, which means no limit at all. Debezium starts again, carries on from its slot, and sends all three. Nothing was lost, and nobody wrote a retry.
Act five. Debezium sends orders one and two to Kafka, and then dies before writing down how far it has read. Kafka holds two events. Debezium starts again from the last place it wrote down, and the slot hands it the same two changes. It sends both again. Four events for two orders, and each pair carries the same event id. Delivery is at least once, and the id is what lets a reader throw the second copy away.
Act six. Three orders are placed, paid and shipped, each step its own transaction, the orders taking turns. The topic is split into three partitions, and the order id picks the partition. Each order's three events land on one partition, in the order they were committed. Order one is alone on partition one. Orders two and three share partition two, taking turns. Across orders, nothing is promised. The bill: two containers, Postgres started with logical decoding, and one replication slot, which keeps the log for ever if its reader is gone. Retiring Debezium means dropping the slot. And every reader has to recognise an event id it has already seen.
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

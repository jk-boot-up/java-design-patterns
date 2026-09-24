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
Act one. Checkout places three orders. Kafka keeps them in a topic, at places zero, one and two. Copy A of the notifications service is handed all three, and queues three confirmation emails. Then it crashes, before asking Kafka to write down the place it reached. Kafka calls that writing-down committing the offset. So no place is written down, and copy B is handed the same three orders again, at the same places. Nothing on them says they are repeats. Six deliveries for three orders, and six emails.
Act two. Copy A keeps a list of the ids it has handled, in its own memory. It handles three orders, remembers three ids, and crashes before writing down its place. Copy B is handed the same three. Its list starts with no ids at all. Six emails again. A repeat only happens because a copy stopped, so it always lands on a list that is new.
Act three. The pattern. Copy A writes each order's id into a table in Postgres, and the email beside it, in one database transaction. Then it crashes before writing down its place in Kafka. Copy B is handed the same three. The table already holds their ids, so copy B skips all three and queues none. Six deliveries, three emails, three ids. The table outlived the copy that wrote it.
Act four. First the id is written after the email, as a second step. Copy A queues the email for order one and dies before writing the id. Copy B finds no id and queues the email again. Two emails. Then the id and the email go in one transaction, and copy A dies before the commit. Postgres throws both away: no email, no id. Copy B handles the order properly. One email, one id. Exactly once, from a broker that only promises at least once.
Act five. Kafka gives each copy a patience limit: how long it may go without asking for more, before Kafka decides it is stuck. Here the limit is three seconds. Copy A is handed order one, writes the id and the email, and is slow to commit. After three seconds Kafka hands the same order to copy B. Copy B tries to write the same id, and Postgres makes it wait, because copy A holds a lock on it. Copy A commits. Postgres tells copy B the id is taken, and copy B skips it. One email. Then copy A asks Kafka to write down its place, and Kafka refuses. Copy A no longer owns those orders.
Act six, the bill. Three orders placed two days ago are handled, and their three ids stored. A cleanup job keeps ids for twenty four hours, and deletes all three. But this topic keeps orders for one hundred and sixty eight hours, which is seven days. An operator replays the group from the start. Three orders are handed out again, and with their ids gone, three more emails are queued. Six in all. Keep the ids at least as long as Kafka keeps the orders. And there are two more systems to run: two containers, a broker and a database, for one email per order.
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

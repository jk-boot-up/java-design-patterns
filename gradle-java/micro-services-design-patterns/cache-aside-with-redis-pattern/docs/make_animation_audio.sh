#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# Output: docs/audio/step-1.m4a ... step-7.m4a
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
Act one. Every product page reads the database. A thousand page views over ten popular products cost a thousand database reads, though only ten different rows were ever read.
Act two. A Redis server is now running in a container. The shop asks Redis for the price first. On a miss it reads the database and writes the price into Redis, with a sixty-second expiry. The same thousand views now cost ten database reads: ten misses, then nine hundred and ninety hits.
Act three. A second shop starts as a separate Java program. With a cache in its own memory, its first ten views cost ten database reads. With the same Redis, they cost none: ten hits. Redis's own command-line program reads the price for SKU-0 and is told one thousand. Then the first shop changes the price and deletes the key once, and no copy is left for any process.
Act four. The price of SKU-0 is cached for two seconds. Another system changes it to two thousand, so a customer still sees one thousand. Nobody deletes the key. The demo only asks Redis whether the key is still there, until Redis removes it on its own clock. The next customer sees two thousand.
Act four, continued. The time a key has left is its time to live, and Redis calls it the T T L. A price-sync job writes the price back with a plain SET, carrying no expiry. Redis now reports the time to live as minus one, which means never. The price changes to twenty-one hundred. Two seconds later a customer still sees two thousand, and the entry will never expire.
Act five. Fifty requests arrive together, across two shop instances, for SKU-0 just after it expired. A database read takes five hundred milliseconds. Every request misses: more than forty database reads, for one price. Sharing a read inside each instance gives two reads, one per instance. A lock kept in Redis, set only if nobody holds it, gives one database read. The lock expires by itself after five seconds if its holder dies.
Act six. Redis is emptied, as a restart with nothing saved would leave it, and the first ten views cost ten database reads again. Out of the box Redis has no size limit and never throws anything away. The price crosses the network as text. And Redis is one more system to run: one container, for two shop processes.
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

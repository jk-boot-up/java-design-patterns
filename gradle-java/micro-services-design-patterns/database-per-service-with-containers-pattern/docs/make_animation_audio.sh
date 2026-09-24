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
Act one. Both teams keep their tables in one Postgres database called shop. The order history page for customer cust-7 is one SQL join, and it takes one round trip to the database. Then the Catalog team tries to delete the kettle, which order ord-101 still names. Postgres refuses, with error code two three five zero three: a foreign key would be broken.
Act two. The Catalog team renames its column from product name to title. The change is correct and its tests pass. But the order history page belongs to the Orders team, and its query still names the old column. Postgres answers with error four two seven zero three: the column does not exist. Nobody did anything wrong.
Act three. Now the split. Orders keeps Postgres, in a database of its own with one table. Catalog moves to MongoDB, a document database, where the kettle's record has a wattage and the mug's has a capacity. The page asks Orders, then asks Catalog for both names at once: two round trips. The Catalog renames its name field in two documents, and the page is unchanged.
Act four. The old join is tried from both sides. From Orders, Postgres says there is no table called products, and refuses even a reach into another database on the same server. From Catalog, MongoDB's own join is pointed at a collection called orders, which it does not have. It raises no error. It hands back both products, each with zero orders.
Act five. The Catalog team deletes the kettle. MongoDB deleted one document, and nothing refused. Postgres still holds one order naming the kettle, and cannot know it has gone. The page shows no longer in the catalogue. In act one Postgres refused this delete. Across two engines, nothing can.
Act six. Customer cust-7 checks out two more mugs. Orders writes the order inside a Postgres transaction, and Catalog takes two mugs from stock in MongoDB. The payment is declined, and Orders rolls back. Postgres forgets the order. MongoDB keeps its change: thirty eight mugs, where there were forty. Then MongoDB is stopped, and the page shows the orders with no names. Two containers, two drivers, two query languages.
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

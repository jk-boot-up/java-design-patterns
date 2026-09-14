#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-12.m4a
#
# Requirements: macOS (for `say`) and ffmpeg.
#
set -euo pipefail

cd "$(dirname "$0")"

OUT=audio
VOICE="${VOICE:-Samantha}"     # female US English voice, matches the video
RATE="${RATE:-145}"            # words per minute, the series standard

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$OUT"

# Narration for each step. Kept in the same order as STEPS in animation.html.
# These are spoken versions of the on-screen text: column names are read out in
# words, class names are spaced so the voice does not run them together, and
# the key takeaway is spelled out a little more plainly than the caption does.
narrate() {
cat <<'EOF'
One database, and two teams. The shop has two teams. The catalog team looks after products: names, prices, photographs. The orders team looks after what people have bought. They share one database, so the products table and the orders table sit in it side by side. The order history page is one query that joins them, and it is a good page. Two rows come back, each with an order id, a sku, a product name, and a quantity.
Be fair to this, because it is very good. Before anything else, notice what the shared database is giving you, because the rest of this is the story of handing it back. One round trip. A join done by an engine that is extremely good at joins. A join cannot forget a name, so there is no such thing as a half built page. And a foreign key guarantees the product row is there to be joined to, which means an order physically cannot refer to a product that does not exist. If a shop can live like this, it should.
Tuesday afternoon. The catalog team renames a column. They decide that product name should be called title. They have good reasons of their own: consistency with the rest of their schema, or the word the business actually uses. It is their column, in their table. They write a migration, they run it, their tests pass, their service works, and they go home. Nothing here is careless.
Somebody else's page is broken. The order history query names product name in its own source, and that column no longer exists, so the page dies. Now look at who saw what. The catalog team saw a green build. The orders team saw an incident. Both of those are true at the same time, and neither team can see the other one.
Nobody did anything wrong. This is the uncomfortable part. The migration was correct: every product name is still there, readable under its new name. The catalog team could not have known, because the query that broke is not in their code, not in their tests, and not in their build. And here is the sharpest way to say it. This project has a test called a rename breaks the order history page, and that test passes. Your test suite is not going to warn you. A test suite tests a codebase, and this problem lives between two codebases.
And the expensive part is what happens next. The broken page gets fixed in an hour. What does not get fixed is the conversation afterwards, in which both teams agree that from now on, schema changes need a meeting. That agreement is what actually costs money. Not today, but for years. Writing a test does not help, because whose repository would it live in? Saying, do not rename columns, does not help either, and it is the one that usually gets adopted, because nobody has to write it down.
So: give each service its own database. If the catalog team's data were somewhere the orders team physically could not read, the Tuesday rename would be nobody else's business. So that is what the shop does. Orders gets a database. Catalog gets a database. And every method on each of them takes the name of whoever is asking, and refuses anybody else. That is the whole mechanism. There is no algorithm in it.
In a real shop, nothing throws that exception. This is the most important sentence here, so it is worth being slow about. The rule is not enforced in Java, and it is not a note in a wiki. The orders service connects with database credentials that simply cannot see the catalog tables, so a cross service read fails as a permissions error long before it reaches any application code. The exception in this project exists only so that the rule is visible in something small enough to read. If the rule in your system is a comment asking people not to, you do not have this pattern. You have a wish.
The same page, for more money. Now rebuild that page. Ask orders what the customer bought. That comes back as skus and quantities, with no names on it. Collect the skus. Ask catalog what those skus are called. Then stitch the two answers together in Java. Same page, byte for byte. A test asserts that the assembled page says exactly what the joined page said. But it cost two service calls and twenty milliseconds, instead of one query. The cost changed. The answer did not.
Ask once for many, or this gets much worse. One detail in there is doing more work than it looks. The call to catalog takes a list of skus and returns all of the names in one answer. It is not a convenience method. Asking once per row would turn this two row page into two network calls, a fifty row page into fifty, and a report into an outage. There is a test that asserts catalog is called exactly once, no matter how many rows there are. And a customer with no orders never troubles catalog at all. The batch call is the difference between an assembly step and a disaster.
The same rename, and nothing happens. Now run Tuesday again. The catalog team renames product name to title, this time in a database only they can read. The rows change, and the queries that read them change in the same class, in the same commit, tested together. The order history page is unchanged. And be precise about what has just been bought, because it is easy to oversell. It bought no speed: the split page is slower. It bought no correctness: the page was already right. It bought the catalog team the right to change their mind without asking permission.
And now the bill. Two things were given up, and the second is the one people forget. The join is gone, so every question that spans both services is now two calls and some code, and the report that somebody runs on a Monday has nowhere to live. And the foreign key is gone. Watch: catalog deletes a product that an order refers to, and nothing stops it, because the two rows are in different databases and no constraint can span them. The order survives, naming a product nobody has heard of, and the page has to decide what to render. A rule that used to be impossible to break is now merely impolite to break. It lives in code, in tests, and in agreements between teams.
EOF
}

i=0
# The narration is read on file descriptor 3, not stdin. `say`, `ffmpeg` and
# `ffprobe` all read stdin when it is available, and one of them will happily
# swallow the first character of the next line if the loop feeds them from it.
while IFS= read -r line <&3; do
  [ -z "$line" ] && continue
  i=$((i + 1))
  # The text goes via a file rather than an argument: `say` otherwise reads
  # from the loop's stdin and swallows the first character of the next line.
  printf '%s' "$line" > "$OUT/.step-$i.txt"
  say -v "$VOICE" -r "$RATE" -o "$OUT/step-$i.aiff" -f "$OUT/.step-$i.txt"
  ffmpeg -loglevel error -y -i "$OUT/step-$i.aiff" \
      -af "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11" \
      -c:a aac -b:a 128k "$OUT/step-$i.m4a"
  rm -f "$OUT/step-$i.aiff" "$OUT/.step-$i.txt"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/step-$i.m4a")
  printf 'step-%-2d %6.1fs\n' "$i" "$dur"
done 3< <(narrate)

echo
echo "$i clips in $OUT/"

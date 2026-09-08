#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-13.m4a
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
# These are spoken versions of the on-screen text: numbers are written out,
# method names are spoken rather than punctuated, and the key takeaway is
# spelled out a little more plainly than the caption does.
narrate() {
cat <<'EOF'
One tree, and a business that keeps asking new questions. The catalog is a tree. Categories hold products, bundles and other categories, and it has looked like that since the composite project built it. What changes is not the tree. It is what the business wants to know about it. What the stock is worth. How many lines sit in each category. A spreadsheet export. And which items cannot simply be put in a box.
The first two reports are methods, and they are correct. Written the obvious way, a report is a method on the node. Inventory value asks each node what it is worth and adds them up. The counts do the same. Both are the shortest correct way to answer their question, both agree with the visitor version to the penny, and nobody minded writing them.
The third report teaches a product about spreadsheets. The C S V export is not about a product. It is about the rule that a field containing a comma is wrapped in quotes, and a quote inside it is doubled. That rule now lives on a class whose job is to describe a thing on a shelf. And it lives there twice, because the bundle needed one too.
Knowing it twice is how it comes to be known differently. The bundle class was written eighteen months after the product class, by copying it. The copy dropped the quoting. Nothing failed, because no kit had a comma in its name that year. Then marketing renamed the kit, and one row of the finance spreadsheet quietly gained a column.
And the fourth copy is the one that matters. The compliance audit on the product reads the product's restriction field. The bundle version was copied from it, so it reads its own restriction field. A field that came across with the copy and is never set. A bundle has no restriction of its own. It is restricted by what is in the box.
What that costs, outside the codebase. The shipment is filed as clear for air freight, with an undeclared lithium cell in it. Nobody wrote that bug. It is what four near identical implementations of the same idea do over eighteen months. And the interface could not have caught it. It says the method exists, and both classes have one.
Turn it around. One method on the node, forever. The visitor version takes every report method off the model, and puts one method back. Accept, which hands the node to a visitor. Every implementation is one line, and it is the same line in all three classes. From here on, a new report is a new file, and the model is never opened again.
Why accept has to exist. Call visit on a node held as a catalog component, and it does not compile. Java picks between overloads using the static type, which is what the compiler can see, and there is no visit that takes a component. Move the same call inside the product class and it compiles, because there, this is a product. Two calls to reach one method. That is double dispatch, and nobody finds it obvious the first time.
The walk is written once, in the structure. Category accept visits itself, then hands the visitor to each child in turn, then says it is leaving. Depth first, parents before children, siblings in the order they were added. And the same order on every run, because a report that reorders itself cannot be compared with yesterday's. No visitor contains a loop.
The same four reports, as four visitors. Each report is now a class implementing three visit methods, and not one of them required a line of change to the product, the bundle or the category. The inventory value is the same to the penny. The export has one quoting rule, in the class that is about spreadsheets, applied to every node. So every row has the same number of columns.
Visit of bundle is where the missing rule lives. A product is restricted or it is not. One field, one line. A bundle is restricted by what is inside it, and that is a genuinely different rule. Because visit of bundle is a different method from visit of product, the loop over the contents has somewhere to be written. And the kit is on the list.
A fifth report, asked for this morning. Low stock. Everything with fewer than a hundred units, and what it would cost to buy the cover back. It is a private class inside the demo file, written below main, and adding it changed no interface, no node type, and no other report. In the naive design it is a fifth method on the interface, and three more implementations of it.
The bill, and when not to do this. Add one node type, a gift card say, and the visitor interface gains a method, and all six reports stop compiling until it is written. The naive design takes a new node type in its stride. A visitor also cannot prune. The walk belongs to the structure, so a report wanting only accessories still sees the whole tree. Use this when the node types are settled and the reports are not. In a catalog that is true. In a hierarchy that is still growing types, write the methods on the nodes.
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

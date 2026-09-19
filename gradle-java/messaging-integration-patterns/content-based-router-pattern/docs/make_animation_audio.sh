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
Act one. All six orders arrive on the warehouse's channel. Two are gift cards and one is neither, so the warehouse needs an if for each kind, and every new kind means changing it.
Act two. Each order goes where its content says. The physical orders go to the warehouse, the gift cards to digital delivery, the very high value one to fraud review, and the subscription, which no rule covers, to manual review.
Act three. A gift card for fifteen hundred pounds goes to fraud review if the high value rule is first, and to digital delivery if it is last. The order of the rules is part of the design.
Act four. A subscription order no rule covers goes to manual review when there is a fallback channel, and goes nowhere when there is not. A router with no fallback loses what it does not recognise.
Act five. One rule is added, from three to four. An EU subscription now goes to a VAT check. Senders and receivers were not touched. A physical EU order still goes to the warehouse, because an earlier rule matched first.
Act six. The sender starts calling physical orders goods, and the router's rule for physical misses them and sends them to manual review. The router is coupled to the format of the content, and every route is a rule to test.
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

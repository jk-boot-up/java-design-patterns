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
Act one. With nothing coordinating the copies, all three send the report, and the manager receives it three times.
Act two. All three ask for the lease. A gets it, and is the leader. The report is sent by A alone.
Act three. A dies holding the lease. After ten seconds B asks and is refused, because A still holds it. After thirty seconds the lease has expired, and B takes it. For those thirty seconds nobody was actually leading.
Act four. A pauses for thirty five seconds, perhaps in a long garbage collection. Its lease expires and B takes it. A wakes, still believing it leads, and sends, and so does B. The report goes twice.
Act five. Each lease carries a token that only goes up. B's is two, A's was one. When A wakes and tries to send, the report sink refuses the older token. Only B's report is sent.
Act six. A healthy leader that renews every seven seconds against a lease of five loses leadership at second five. Against a lease of thirty it never does. Too short loses a healthy leader, too long misses a dead one, and everything depends on one shared record.
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

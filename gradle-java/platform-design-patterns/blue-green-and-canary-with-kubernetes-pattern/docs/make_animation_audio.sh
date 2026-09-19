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
Act one. The first release is stopped to make room for the second. Twenty requests arrive while nothing is running, and all twenty fail.
Act two. Version two runs beside version one, and only a test port reaches it. The test request is answered by version two. Twenty requests before the switch are all answered by version one. The switch is one patch to the service. Twenty after are all answered by version two, and none failed.
Act three. Version two has a bug with big orders. Twenty big orders on version two: all twenty fail. One patch sends the service back to version one, whose pods never stopped. Twenty big orders: none fail.
Act four. Nine pods of version one and one of version two, behind one service. Three hundred big orders: a few dozen failed, a small share, as a canary should be. The spread is chosen by the cluster's own rules, so the exact count changes from run to run. Had all three hundred gone to version two, all would have failed.
Act five. Steps of one, five and ten pods of version two, with a gate at five failures in a hundred. The buggy release is halted, and every pod is version one again. A first step with few requests can miss a bug, and the next step, with more traffic, catches it.
Act six. During a blue-green switch both releases are fully running: four pods, where one release needs two. Both share one database, so a release that changes the data cannot be switched back safely. And a cluster is a lot to run for a checkout.
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

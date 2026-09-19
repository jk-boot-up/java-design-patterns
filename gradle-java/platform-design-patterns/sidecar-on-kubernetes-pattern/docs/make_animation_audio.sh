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
Act one. In Compose the shared network is a line in a file, and it can be forgotten. In a Pod there is no line. Both containers are on one address because that is what a Pod is.
Act two. In Compose, stopping checkout leaves the proxy running. Delete a Pod and both containers go together. The replacement is a new Pod on a new address.
Act three. The proxy dies, and the Pod reads one of two. A payment is refused. The kubelet restarts the proxy alone. Checkout is never touched.
Act four. The refunds team wrote one container. The Pod that was created has two. The sidecar arrived from outside. That is what a service mesh is built on.
Act five. One logical service, two containers. With the proxy down it reads one of two, and traffic stops. Containers started together race. A native sidecar starts first.
Act six. A scheduler, a control plane, a YAML dialect and a networking model. For four services, probably not yet. For a fleet, the bargain.
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

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
Act one. The threshold lives in a git repository: fifty pounds, committed by Priya in engineering. A config server, running as a separate Java program, reads the repository and hands the value out over the network. The shop fetches its settings as it starts, and quotes a forty-eight pound basket with four ninety-nine for delivery. The banner says free delivery over fifty pounds.
Act two. Maya in marketing commits thirty-five pounds for the weekend. The config server reads the repository on every request, so it answers thirty-five at once. But the running shop has not asked again. It fetched its settings once, when it started, and still quotes against fifty pounds.
Act three. The demo sends the running shop a refresh request. The shop fetches its settings again and reports what changed: the commit its settings came from, and the threshold. The next quote ships the forty-eight pound basket free. It is the same running copy of the shop. No restart.
Act four, and the surprise. The refresh rebuilt the checkout's settings, because they are marked to be refreshed. The banner copied fifty pounds into a field when the shop started, and nothing rebuilds it. One running shop now quotes against thirty-five pounds and advertises fifty. No error anywhere.
Act four, continued. Only a restart of the shop reaches the banner. The new copy fetches thirty-five pounds as it starts, and the banner now says free delivery over thirty-five pounds.
Act five. On Saturday morning somebody commits minus one. The config server serves it, because it does not check values. The refresh answers two hundred, which means OK. The shop declares a range, five pounds to two hundred, and checks it when it rebuilds the settings, on the next quote. The check fails, and there is nothing to fall back to. Five quotes, five failures, each with status five hundred. Sam on call commits thirty-five again, refreshes, and the shop quotes normally. Git's own log holds the history.
Act six. The config server stops. A refresh of the running shop now answers five hundred, and the shop keeps what it already fetched: still free delivery against thirty-five pounds. A new copy of the shop told to fail fast refuses to start. A new copy told the server is optional starts on the default packed inside it, fifty pounds, and charges four ninety-nine. The promotion is gone, with no error.
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

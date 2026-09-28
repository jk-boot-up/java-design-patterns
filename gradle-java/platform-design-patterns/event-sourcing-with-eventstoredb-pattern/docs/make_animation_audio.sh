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
Act one. The demo appends the four things that happened to customer C 4 4 1 7 in March, and KurrentDB numbers them revision zero to three. A second connection reads the stream from the start and adds it up to a hundred and forty points. Nothing stores a hundred and forty; it was added up just now.
Act two. Customer C 5 1 2 0 pays with points on the website and in the phone app at the same moment. Both look, and both see a hundred and forty points at revision three. Both decide a hundred is affordable, and both append a spend with no check. Both are accepted, at revisions four and five, and the balance is minus sixty.
Act three. The same race for C 5 1 2 1, but each append now says: only if the stream is still at revision three. One is written at revision four. The other is refused with Wrong Expected Version: expected revision three, but the stream is at revision four. The refused checkout looks again, sees forty points, and says no. The balance is forty.
Act four. The shop awards C 5 1 2 2 forty-five points, loses the reply, and sends the award again with a new event id. Two awards, a balance of ninety. For C 5 1 2 3 the retry reuses the same event id and the same expectation. The server answers revision zero again and writes nothing. One award, a balance of forty-five.
Act five. The support dashboard starts last and asks for every loyalty stream from the start. It receives eighteen stored events, and is told it has caught up. Then a new order awards C 4 4 1 7 twenty points, and with nobody telling it, the dashboard shows a hundred and sixty.
Act six. C 5 1 2 2 asks to be forgotten, and the shop deletes the stream. Reading it now gives stream not found. But the store's whole log still holds its two events until a clean-up called a scavenge runs, and the dashboard still shows ninety.
Act six, continued. A later order writes to the same stream name, and it is accepted at revision two, not zero. And the server ran with its security switched off: no encryption, no passwords, one container. Production must never run like that.
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

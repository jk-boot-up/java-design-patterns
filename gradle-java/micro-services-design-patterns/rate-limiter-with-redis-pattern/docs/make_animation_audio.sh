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
Act one. The rule is ten searches per client, filled back up once an hour. Three copies of the search service each keep their own bucket in their own memory. client-42 sends ninety searches, dealt to the servers in turn, and each server lets ten through: thirty in all, not ten. Scaled out to six servers, the same ninety get sixty through. Every server added loosens the limit by another ten.
Act two. Now no server keeps a bucket. Each has its own connection to one Redis, a separate program that keeps small values under names, and every server asks it on every search. client-42 sends ninety through three servers: ten allowed, eighty refused. Scaled out to six servers, a second client, client-77, sends ninety: still ten. Redis holds two keys, one per client, however many servers there are.
Act two, continued. Server one is restarted, and comes back with empty memory. client-42's next search is refused, and the refusal says to come back in sixty minutes. The bucket was never in the server, so restarting the server does not refill it.
Act three. Ninety searches, thirty on each of three servers, each on its own thread, held at a gate and released at the same instant. Exactly ten are allowed. No server holds a lock. Each writes its answer back only if the bucket has not changed since it read it, and reads again if it has.
Act four. The count is now a plain number, read and written in two steps. One token is left. Server one reads one. Server two reads one. Both write back zero and both serve: two searches from one token, and Redis afterwards says zero, so nothing looks wrong. Again, but each write lands only if the number is still what was read: server two's write is turned down, it reads again, finds zero, and refuses. One search from one token. Bucket4j does the second, on every search.
Act five. Two servers with correct clocks spend client-42's ten searches, and the next is refused. A third server's clock runs one hour fast. client-42 sends twenty searches through it, and ten are allowed. The fast server decided the hour was up, refilled the bucket, and Redis stored its answer. Redis keeps the bucket; the sums are done on each server, with that server's clock. The clocks must agree.
Act six. One thousand different clients search once each, and Redis holds one thousand keys. Each is set to delete itself in sixty minutes, when its bucket would be full again. Then Redis is stopped. Five searches get five errors from the limiter, and no answer. Let them through, and there is no limit. Refuse them, and five real customers see an error. The shop must choose. And every search now waits for a trip to Redis: one container, for six servers.
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

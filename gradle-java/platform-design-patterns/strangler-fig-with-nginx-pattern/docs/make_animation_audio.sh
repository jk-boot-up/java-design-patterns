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
Act one. NGINX starts in front of the old shop, with one rule: everything to the old shop. The shop's four pages all work. Then a big-bang Monday: one line sends every route to the new service, which has built only prices and checkout. The price page works. The other three answer four oh four. One page in four works.
Act two. A customer's price request has reached the old shop, and the old shop is slow. While it is open, one rule is added, prices to the new service, and NGINX reloads. Its main process is number one before and after, so nothing restarted. One worker is still finishing the open request, and one new worker takes new requests. A new price request goes to the new service. Then the open request finishes, from the old shop.
Act three. The shop's real configuration has an old rule, a regular expression, which is a pattern written with symbols, sending prices and stock to the old shop. The same move goes in. The check passes and the reload succeeds. Ten price requests: ten from the old shop, none from the new service. NGINX tried the regular expression after the prefix, and it won. The move did nothing, and nothing said so.
Act three, continued. The same rule, written with a caret and a tilde in front of the prefix. That tells NGINX to stop looking once the prefix matches. Ten price requests: all ten from the new service.
Act four. The new service's address is written two ways, one character apart. With nothing after the name, the new service is asked for slash api slash prices slash S K U one, and answers two hundred. With one slash after the name, NGINX cuts the matched prefix off, and the new service is asked for slash S K U one, and answers four oh four.
Act five. The new service stops. Ten price requests: ten answers of five oh two, Bad Gateway, written by NGINX itself. Ten stock requests, still on the old shop: ten answers of two hundred. Rolling back is one rule removed and one reload, and prices come from the old shop again.
Act six. A customer puts three items in the basket. The old shop keeps it, and sets a cookie called legacy session. Checkout moves to the new service. NGINX passes the cookie along, and the new service cannot use it: your basket is empty. Moved back, the old shop places the order: three items, four thousand two hundred and forty-nine pence. The old shop still serves four of five routes, and there are three things to run.
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

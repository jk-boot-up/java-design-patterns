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
Act one. Three copies of the reporting service run as three separate processes. None of them asks who is in charge. Each is told to send the nightly sales report, and each does. The manager receives it three times.
Act two. Copy A asks the API server first, and is written into the lease: holder A, five seconds, holder changes zero. B and C read it and are told the leader is A. Only A sends the report. Then two writes are made from the same version of the lease. The server accepts the first, and refuses the second with 409 Conflict. That is the only rule it enforces.
Act three. A is shut down cleanly, and hands the lease back on its way out. One of B and C takes over within a couple of seconds. Then the new leader is killed outright. The lease goes on naming the dead copy, and the last copy waits about one whole five-second lease before it takes over. For that time, nobody leads.
Act four. A checks that it leads, and starts the report. Then its whole process freezes, as in a long garbage-collection pause, and it stops renewing. The lease runs out, and B takes it: holder B, holder changes one. B sends the report. A wakes, still believing it leads, and sends too. The lease, read at that moment, names B.
Act five. The same again, but each report carries a token: the lease's count of holder changes when that copy took it. A's token is zero, B's is one. B sends first. When A wakes and sends with zero, the inbox refuses it. Only B's report arrives.
Act six. B is killed. A is still running, but its elector gave up for good when it lost the lease. Two whole leases later the lease still names B, and nobody leads. Only when A starts a brand-new elector does it lead again, with token two.
Act six, continued. A five-second lease means a dead leader goes unnoticed for up to five seconds, and a shorter one lets a slow moment cost a healthy leader its lease. Each copy judges the lease by its own clock. And all of it needs a Kubernetes API server: one cluster, with one node, for one nightly report.
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

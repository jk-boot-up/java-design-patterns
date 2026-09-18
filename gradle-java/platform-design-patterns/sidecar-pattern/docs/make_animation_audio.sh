#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-12.m4a
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
# field names are spoken as English rather than as identifiers, and the key
# takeaway is spelled out a little more plainly than the caption does.
#
# One line per step, and the count must match the STEPS array. If you copied
# this file from another pattern, replace every line below before running it.
narrate() {
cat <<'EOF'
The online store takes money in four places. Checkout charges a card while a customer sits watching a spinner. Refunds gives money back when the coffee maker comes back in the post. Subscription billing runs at two in the morning against thousands of saved cards. And marketplace payouts pays the independent sellers every Friday. Four teams, four repositories, four release days, and one payment provider at the other end of all four.
None of those four teams wanted to become an expert on a payment provider's network behaviour, but every one of them had to answer the same four questions before going live. How many times to retry a failed attempt. When to give up altogether. Which transport security profile to present. And what to count, and what to call the counters. Four questions, four services, sixteen answers. And not one of those sixteen is about checkout, or refunds, or subscriptions, or payouts. They are all facts about a network and a supplier's contract. They would be identical if the shop sold bicycles.
In March the provider writes to every merchant. Retrying ten milliseconds after a failure does not help anybody, the letter says. The failure has not had time to clear, and all you have done is spend capacity that the provider then has to ration. From now on: at most three attempts per payment, and wait properly between them. The shop's platform engineer agrees, and does the obvious thing.
Checkout: two lines, a pull request, a review, shipped. Then refunds. Then marketplace payouts. Three pull requests, three reviews, three releases, all in one afternoon, and everybody goes home. Now look at the fourth row. Subscription billing was not updated. Not through carelessness, and not through anybody being wrong. It runs overnight, so nobody was watching it that week. It is owned by a team who were not in the meeting with the provider. It lives in its own repository with its own build, and it had no open work that sprint. There was no fourth place to look unless you already knew there was a fourth place to look. Nothing throws. Nothing is logged. Every test in all four services still passes, because each one tests its own copy, and its own copy is internally consistent.
Three weeks later, at two in the morning, the provider has one of its wobbles. Three hundred milliseconds of declining everything, and then it is fine again. The contract allows the shop twelve attempts across the whole merchant account during an event like this: three per payment, four services that take payments. Subscription billing is already running, because it is always running at two in the morning, so it reaches the wobble first. On the old policy it makes six attempts. It succeeds. It gets its money, and its dashboards are green.
Marketplace payouts arrives fourth. It makes one attempt, and the answer is not a decline. It is a refusal, because the account's twelve attempts are already gone. The sellers do not get paid. And there is nothing wrong with the marketplace payouts service. It was updated in March. It did exactly what the provider asked. It happened to arrive fourth. The code that misbehaved and the code that suffered are in different repositories, owned by different people, in different rooms. On Monday morning somebody opens an incident about the service whose every line is correct.
So here is the pattern. Those four decisions are not decisions about the shop's business. They are decisions about how anything on this network talks to that supplier, and they ended up inside four services only because that is where the code that makes the call happens to live. So move them out. Not into a library compiled into the service, but into a separate process running beside it on the same machine. The service sends its payment to localhost and knows nothing else. The proxy is the only thing that leaves the machine.
All four proxies read the same configuration. Not four equal copies of it: the same one. The test in this project says so with assert same, rather than assert equals, because four equal copies would be March all over again with better manners. Now run the same night. The gateway still wobbles for three hundred milliseconds. Nothing about the network improved. But every service makes three attempts, twelve of twelve are spent, and nobody is refused. The policy was not applied four times and missed once. It was stated once.
Now the bill, and there are three items on it. Read all three rows of this table or none of them. The copies fall from sixteen to four, and the places to edit a policy fall from four to one. Those two rows are why you would do this. The third row is why it is not free: four proxies is four more processes wanting memory, a version number, a restart when they are patched, and a line in somebody's runbook. But notice which row scales. Add a fifth service that takes payments and the copies go from sixteen to twenty the old way. Beside the services, it is still four. The method that calculates that takes no argument at all, and the missing argument is the whole answer.
The second item on the bill. A healthy gateway, a healthy service, a healthy network, and the proxy beside checkout fails to start after a patch. Connection refused to localhost. Now look at the next number: attempts that reached the gateway, zero. The request never left the machine, and the service has no retry code left to fall back on, because we deleted it, on purpose. You added a dependency to every single call in order to make those calls more reliable. That trade is usually worth it, because a proxy on the same machine with no business logic in it fails far less often than the internet does. But it is a trade, and on the night it goes wrong it goes wrong for every call the service makes, rather than for one of them.
The third item. The same payment, the same policy, the same wobble, measured both ways. With the retry code inside the service: three attempts, six hundred milliseconds. With the retry code in a proxy next door: three attempts, six hundred and three. Three milliseconds, which is one millisecond per attempt for crossing to a neighbouring process and back. On a payment that already takes six hundred, that is nothing. On an internal call that takes two milliseconds it is a fifty per cent increase. And in a system where every service talks through a proxy, every hop between two services is paid twice: once leaving one, and once entering the next. That is the arithmetic that decides whether a service mesh belongs in your system, and it is arithmetic, not taste.
And now the admission this project owes you. Everything you have just watched happened inside one Java program. In one program, a proxy that a service talks through is an object wrapping another object, and an object wrapping another object is the Decorator pattern, from earlier in this course. The code is not new. What makes this a different pattern is not the code. It is where the code runs. A decorator is compiled into your jar, is written in your language, and changes when your service is rebuilt. A sidecar is its own process, may be written in a language nobody on your team knows, and changes when somebody restarts it. So the question is never wrapper or no wrapper. It is this: does this concern need to change without rebuilding the service, or apply to a service written in a language your library does not support? Yes to either, and it goes next door. No to both, and a shared library in your own process is cheaper, faster, and has one fewer thing that can fail.
EOF
}

i=0
# The narration is read on file descriptor 3, not stdin. `say`, `ffmpeg` and
# `ffprobe` all read stdin when it is available, and one of them will happily
# swallow the first character of the next line if the loop feeds them from it.
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

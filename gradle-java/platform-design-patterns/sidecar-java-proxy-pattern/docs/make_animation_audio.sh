#!/usr/bin/env bash
#
# Generates the optional narration clips for docs/animation.html.
#
# One .m4a per animation step, spoken by the same female voice and at the
# same rate as the teaching video, so the two sound consistent.
#
# Output: docs/audio/step-1.m4a ... step-10.m4a
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
Checkout takes payments, and the code that knows how to talk to the payment provider is not in it any more. It moved next door into a proxy. That is the Sidecar pattern, and that project is the one to read first. What matters here is the one line of configuration the service has left: an address on its own machine. Not a provider hostname, not a certificate, not a retry count. Whatever is listening there answers, and checkout has no way to find out what it is. Today it is nginx. About twenty-two lines of configuration, in a container somebody else wrote, tested, hardened, and has been patching for twenty years. That was a good decision, and this project does not undo it.
In March the payment provider wrote to every merchant asking for two things. At most three attempts per payment, and wait properly between them. The shop agreed to both. The configuration says three attempts, and everybody went home. Now read the second half of that sentence again, because it is the whole problem. nginx can say the first of those things. It cannot say the second.
The provider has a bad three hundred milliseconds. Nothing is broken and nobody needs paging. It declines everything, and then it is fine again. A customer buys a coffee maker for forty-seven pounds ninety-nine. The proxy makes its three allowed attempts, and here is what the provider itself recorded, with the times taken at its end rather than the shop's. One millisecond. Two milliseconds. Three milliseconds. Three attempts spanning two milliseconds, against a provider that did not recover until three hundred. Every one of them landed inside the bad window, because they were all made inside the bad window. The shop spent its entire allowance for that payment before the provider had time to get better, and the customer got nothing. The half of the agreement that limits the shop was kept. The half that would have helped was not.
This is the part that makes it a design problem rather than a defect. nginx does not have a retry counter. What it has is an upstream group, which is a list of servers, and a rule that says if this one fails, try the next one in the list. The shop's configuration lists the provider's address three times, because three entries is how you spell up to three attempts when the upstream is a single address. Moving to the next entry happens immediately. That was a good decision for the case nginx was built for. In a pool of machines, the next machine is a different machine and is probably fine, so waiting first would only make every request slower for nothing. It stops being a good decision the moment every entry in the pool is the one address that is currently unwell. So there is nothing to fix. There is no directive anywhere in nginx's http proxy module that says wait two hundred milliseconds before the next attempt. The sentence does not exist in the language.
There are three ways out, and two of them are bad. You could put the waiting back in the service, which undoes the entire previous project: four services means four copies of the waiting, and the next policy change lands in three of them. You could script the proxy. nginx will run Lua, and njs will run JavaScript, and either one can express a delay. But then you are writing code inside a proxy you chose because it was configured rather than programmed, in a language most of your team does not use, with worse tooling and nowhere obvious to put a test. Or you could put a different proxy on the port. That third option only exists because of a decision made in the last project. The contract between the service and its proxy is an address, not a library. Nothing about it is Java, and nothing about it is nginx.
So somebody writes a proxy. It is about forty lines of Java, and the whole of it is one shape: read the policy, try, catch, wait, double the wait, try again. Compare it with the nginx proxy's loop and they are the same loop with one statement missing. And the statement is not missing because whoever wrote the nginx version forgot it. It is missing because there was nothing to write it with. Now put the new one on the port. That is one line, and look at what that line does not take. No reference to the service. Nothing it could use to notify one. Nothing it could use to restart one. The start number did not move, and that is not the demo being careful. There is exactly one place in the whole program where a payments service is constructed, and it runs before the first act. A test reads the source with the comments stripped and counts, so it stays that way.
Identical provider. Identical bad three hundred milliseconds. Identical payment, and an identical allowance of three attempts. One millisecond. Two hundred and two. Six hundred and three, and that one is charged. Read this against the earlier block and notice what is not different. Three attempts in both. The provider's allowance is untouched, the shop is not being greedier, and the change costs the provider nothing at all. The only thing that changed is when the third attempt arrives, and by six hundred milliseconds the provider is well again. The spacing was the difference between a customer walking away and a coffee maker being sold. The doubling matters too. If every retry in the shop waited a fixed two hundred milliseconds, every service that failed at the same moment would come back at the same moment, and the provider's first breath after a bad second would be the whole shop arriving at once.
The last two steps skipped something, and it is the thing that will actually page somebody. A swap is not instant. The old proxy stops and the new one starts, and in between there is a moment when nothing is listening on the port at all. A payment that arrives then does not fail slowly. It fails immediately, and the service has nothing to fall back on, because its retry code was deleted in the last project on purpose. A healthy provider, a healthy network, a healthy service, and zero attempts reached anybody. The request never left the machine, which also means nothing in the provider's dashboards will ever show that it happened. So a real swap is not one line, it is a rollout. Start the new proxy before stopping the old one. Move one service at a time. And keep the old proxy installable, because the honest reason to be able to swap forwards is to be able to swap back.
Now, what you just bought. Two proxies. One is configured in nginx's configuration language, and the other is written in Java. They go on the same port, beside the same service, and they are handed the same policy object. The service's source file is byte for byte identical in both runs. The previous project claimed that a sidecar is language independent: that the proxy may be written in a language nobody on your team knows, and the service will not care. That claim was true, and it was unsupported, because every line of evidence in that project was Java talking to Java. This is not a claim about language independence. It is language independence, happening.
And now what you paid for it, because a pattern taught without its costs is an advertisement, and the honest accounting here mostly argues against doing it. Twenty-two lines of somebody else's configuration became forty lines of your own code. That code is yours to test, to review, to keep working on the next JDK, and to fix at three in the morning. Everything nginx brought for free is gone until you write it. Transport security termination. A structured access log with a format every service shares. Connection pooling. And twenty years of somebody answering security advisories before you have heard of them. A virtual machine now sits beside every service where a few megabytes of nginx used to sit, so multiply that by the number of services you run. And nothing stops the next person putting the shop's refund rules in the proxy, because a general purpose language will happily let them. A configuration language was a fence, and you took the fence down at the same moment you took the limitation away. So the rule is narrow. Swap the proxy when the thing you need cannot be said in the configuration language at all. Not when it is awkward. Not when you would rather write Java. Here the missing sentence was the difference between a payment going through and a payment failing, and that clears the bar. Very little else does. What is worth keeping either way is that the choice was available. Because the service talks to an address rather than to a library, swapping the proxy was a decision somebody could make on a Tuesday afternoon, and swapping it back is the same decision in the other order.
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

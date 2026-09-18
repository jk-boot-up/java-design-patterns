"""Scene definitions for the Sidecar-with-a-Java-proxy teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and every number is said out loud rather than left on a slide.

Every figure spoken aloud comes from the captured output of `./gradlew run`,
which is deterministic by construction: the provider recovers at a fixed
millisecond, the clock is a counter rather than a timer, and nothing is random.
DemoRunsTest pins the exact strings, so a change to the program that moved a
number would fail the build rather than quietly make this video wrong.

This is the second of three Sidecar videos and it does not re-teach the first.
Scene 2 is the only scene that recaps §41, and it recaps it in about a minute
because the rest of this video is worthless without it. From scene 3 onwards the
subject is one gap: nginx has no directive for waiting between retries, because
it retries by moving to the next server in an upstream group and that move is
immediate. Scenes 3 to 6 are that gap. Scenes 7 to 10 are the swap and what it
proves. Scenes 11 to 13 are the bill, which is longer than the benefit and is
the reason this video ends by advising most viewers not to do any of it.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Sidecar with a Java Proxy",
        body=None,
        narration=(
            "Hello, and welcome. This video explains how to swap out a sidecar "
            "proxy in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 165]] Here is the simple definition. When a "
            "service talks to a helper program running beside it, the only "
            "thing connecting the two is an address. Not a library, not a "
            "shared language, not a shared build. Just an address. And that "
            "means whatever is listening at that address can be replaced with "
            "something completely different, written in a completely different "
            "language, while the service keeps running and is never told. "
            "[[slnc 193]] Think about the plug on a kettle. The kettle knows "
            "nothing about the electricity. Not the voltage, not which wire is "
            "live, not what the fuse in the plug is rated at. So when somebody "
            "discovers the fuse is the wrong rating, they change the fuse. They "
            "do not open the kettle, and they do not send it back to the "
            "factory. That works because the contract between the kettle and "
            "the electricity is the shape of a socket, rather than a wiring "
            "diagram. [[slnc 165]] One thing before we start. This video is a "
            "follow-on. It assumes you have already watched the Sidecar video, "
            "which explains what a sidecar is and why the retry code left the "
            "service in the first place. If you have not seen that one, watch "
            "it first, because this video spends about one minute recapping it "
            "and then never mentions it again. [[slnc 193]] The rest of this "
            "video does one job properly, by building a working Java project. "
            "An online shop. A payment provider that has a bad three hundred "
            "milliseconds. A sentence the shop's proxy has no words for. And a "
            "forty-line replacement that goes on the same port beside a service "
            "that is never rebuilt, never restarted, and never told anything at "
            "all. [[slnc 150]] By the end you will know why a proxy retrying "
            "immediately is correct almost everywhere and wrong here, what it "
            "costs to write your own proxy instead, and the narrow rule that "
            "says when you should."
        ),
    ),
    dict(
        key="02-recap",
        kind="bullets",
        title="One Minute On Where We Are",
        body=[
            "From the previous project:",
            "",
            "    the retry policy left the service",
            "    it lives in a proxy next door, its own process",
            "    the service's whole configuration is one line",
            "",
            "    http://localhost:8081/pay",
            "",
            "Not a hostname. Not a certificate. Not a retry count.",
            "",
            "Today, the thing listening there is nginx.",
        ],
        narration=(
            "So, one minute on where we are, and then we move on. [[slnc 165]] "
            "The online shop takes payments at checkout. The code that knows "
            "how to talk to the payment provider used to live inside that "
            "service, and in the previous project we moved it out. It now runs "
            "in a small separate program on the same machine, right beside the "
            "service. Everything the shop had decided about that provider — how "
            "many times to try, when to give up, what certificate to present — "
            "is written down once, in one file, which that proxy reads. [[slnc "
            "193]] Which means the checkout service's entire configuration for "
            "reaching a payment provider is now one line, and that line is an "
            "address on its own machine. Not a provider hostname. Not a "
            "certificate. Not a retry count. Whatever is listening at that "
            "address answers, and checkout has no way at all to find out what "
            "it is. [[slnc 165]] Today, the thing listening there is nginx. "
            "About twenty-two lines of configuration, running in a container "
            "that somebody else wrote, somebody else tested, somebody else "
            "hardened, and somebody else has been patching for twenty years. "
            "That was a good decision, and nothing in this video undoes it. "
            "[[slnc 150]] Hold on to one thing from all of that: the contract "
            "between the service and the thing next door is an address."
        ),
    ),
    dict(
        key="03-letter",
        kind="bullets",
        title="The Letter From The Provider",
        body=[
            "In March the payment provider wrote to every merchant:",
            "",
            "    at most three attempts per payment",
            "    and wait properly between them",
            "",
            "The shop agreed to both.",
            "The configuration says three attempts.",
            "Everybody went home.",
            "",
            "Read the second half of that sentence again.",
        ],
        narration=(
            "In March, the payment provider writes to every merchant, and it "
            "asks for two things. At most three attempts per payment. And wait "
            "properly between them. [[slnc 165]] Both of those are reasonable, "
            "and the reason for the second one is worth a moment. If you retry "
            "ten milliseconds after a failure, the failure has not had time to "
            "clear. All you have done is spend capacity that the provider then "
            "has to ration. So: try again, but leave a real gap. [[slnc 150]] "
            "The shop agreed to both. The configuration says three attempts. "
            "Everybody went home. [[slnc 193]] Now read the second half of that "
            "sentence again, because it is the whole problem in this video. "
            "Wait properly between them. The shop's proxy can say the first "
            "half of what the provider asked for. It cannot say the second."
        ),
    ),
    dict(
        key="04-wobble",
        kind="console",
        title="Three Attempts That Bought Nothing",
        body="""Act 2 - the provider has a bad 300 milliseconds.
  A customer buys a coffee maker for £47.99.

  What the provider itself recorded, at its own end:

    attempt at    1ms   declined
    attempt at    2ms   declined
    attempt at    3ms   declined
    3 attempts, first to last: 2ms

    ORD-4418     £47.99    NOT PAID

  The provider recovered at 300ms.
  There was nobody left to ask.""",
        narration=(
            "Three weeks later, the provider has a bad three hundred "
            "milliseconds. Nothing is broken and nobody needs paging. It "
            "declines everything for a fraction of a second, and then it is "
            "fine again. [[slnc 165]] A customer buys a coffee maker for "
            "forty-seven pounds ninety-nine. The proxy makes its three allowed "
            "attempts. And here is what the provider itself recorded, with the "
            "times measured at the provider's end rather than the shop's, which "
            "matters, because a proxy reporting on its own behaviour is a claim "
            "and a supplier's log is evidence. [[slnc 193]] The first attempt "
            "arrived after one millisecond, and was declined. The second "
            "arrived after two milliseconds, and was declined. The third "
            "arrived after three milliseconds, and was declined. Three "
            "attempts, and from the first to the last, two milliseconds. "
            "[[slnc 165]] The provider did not recover until three hundred. "
            "Every one of those attempts landed inside the bad window, because "
            "every one of them was made inside the bad window. The shop spent "
            "its entire allowance for that payment before the provider had time "
            "to get better, and the customer got nothing. [[slnc 150]] So the "
            "half of the agreement that limits the shop was kept. The half that "
            "would have helped was not."
        ),
    ),
    dict(
        key="05-no-bug",
        kind="bullets",
        title="Nobody Wrote A Bug",
        body=[
            "nginx has no retry counter. It has an upstream group:",
            "",
            "    a list of servers, and a rule —",
            "    if this one fails, try the next one",
            "",
            "The config lists the provider's address three times.",
            "Three entries is how you spell 'three attempts'.",
            "",
            "Moving to the next entry happens immediately.",
            "",
            "There is no backoff directive. The sentence does",
            "not exist in the language.",
        ],
        narration=(
            "Now, the obvious response is to go and fix the proxy's "
            "configuration. And this is the part that makes this a design "
            "problem rather than a defect: there is nothing to fix it with. "
            "[[slnc 193]] nginx does not have a retry feature in the sense you "
            "are probably imagining. What it has is something called an "
            "upstream group, which is a list of servers, and a rule that says: "
            "if this one fails, try the next one in the list. The shop's "
            "configuration lists the payment provider's address three times, "
            "because three entries in the list is how you spell up to three "
            "attempts when there is only one address to talk to. [[slnc 165]] "
            "And moving on to the next entry in that list happens immediately. "
            "[[slnc 150]] That was a good decision for the case it was designed "
            "for. Picture a pool of ten web servers. If the ninth one fails, "
            "the tenth one is a different computer, and it is probably "
            "perfectly healthy. Waiting before you try it would make every "
            "single request slower, for no reason at all. [[slnc 193]] It stops "
            "being a good decision the moment every entry in that list is the "
            "same address, and that address is the one having a bad minute. "
            "Three attempts at the same unwell thing, made inside the same "
            "three milliseconds, are three attempts that are all going to get "
            "the same answer. [[slnc 165]] So nobody wrote a bug here. There is "
            "no directive anywhere in nginx's proxy module that says wait two "
            "hundred milliseconds before the next attempt. The sentence the "
            "provider asked for does not exist in the language the shop's "
            "policy is written in. And that is a very different situation from "
            "a mistake, because there is nothing to correct."
        ),
    ),
    dict(
        key="06-ways-out",
        kind="bullets",
        title="Three Ways Out, Two Of Them Bad",
        body=[
            "✗  put the waiting back in the service",
            "       four services, four copies, and the next",
            "       policy change lands in three of them",
            "",
            "✗  script the proxy in Lua or JavaScript",
            "       code inside a proxy you chose because it",
            "       was configured rather than programmed",
            "",
            "✓  put a different proxy on the port",
            "       the service already talks to an address",
        ],
        narration=(
            "There are three ways out of this, and two of them are bad. [[slnc "
            "165]] The first is to put the waiting back inside the service. "
            "That undoes the entire previous project. Four services that take "
            "money means four copies of the waiting, and the next time the "
            "policy changes it will land in three of them and be missed in the "
            "fourth. That was the exact problem the sidecar existed to solve. "
            "[[slnc 193]] The second is to script the proxy. nginx will run a "
            "language called Lua, and there is a JavaScript module for it too, "
            "and either one can express a delay. But think about what you have "
            "just done. You are now writing code inside a proxy that you chose "
            "precisely because it was configured rather than programmed, in a "
            "language most of your team does not use, with worse tooling, and "
            "nowhere obvious to put a test. [[slnc 193]] And the third is to "
            "put a different proxy on the port. [[slnc 165]] That third option "
            "only exists because of a decision made in the previous project, "
            "and it is easy to walk straight past it. The contract between the "
            "service and its proxy is an address. Not a library. Not a "
            "language. Not a shared build, or a shared version of anything. The "
            "service sends a request to a local address, and something answers. "
            "Nothing about that is Java, and nothing about it is nginx. [[slnc "
            "150]] That is a far weaker promise than a library dependency, and "
            "it turns out to be exactly as sufficient."
        ),
    ),
    dict(
        key="07-the-gap",
        kind="code",
        title="The Loop, With The Sentence Missing",
        body="""// NginxProxy.forward — the retry loop, as the config expresses it
for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
    clock.waitFor(HOP_MILLIS);
    try {
        return receiptFrom(
                provider.charge(besideService, payment, clock.now()));
    } catch (PaymentFailed failure) {
        if (failure.reason() == PaymentFailed.Reason.RATE_LIMITED) {
            break;
        }
        // And here is where the waiting would go,
        // if it could be said at all.
    }
}""",
        narration=(
            "Here is the nginx proxy's retry loop, written out in Java so we "
            "can look at it. Try the provider. If it fails, go round again. If "
            "the provider says the allowance is spent, stop immediately, "
            "because retrying that would just be making a busy supplier busier. "
            "[[slnc 165]] And then, at the bottom of the loop, there is a "
            "comment, and the comment says: and here is where the waiting would "
            "go, if it could be said at all. [[slnc 193]] That empty space is "
            "the entire subject of this video. It is not empty because somebody "
            "forgot. It is empty because there was nothing to write in it."
        ),
    ),
    dict(
        key="08-forty-lines",
        kind="code",
        title="Forty Lines Of Java",
        body="""// JavaProxy.forward — the same loop, plus four lines
long backoff = policy.firstBackoffMillis();
for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
    clock.waitFor(HOP_MILLIS);
    try {
        return receiptFrom(
                provider.charge(besideService, payment, clock.now()));
    } catch (PaymentFailed failure) {
        if (failure.reason() == PaymentFailed.Reason.RATE_LIMITED) {
            break;
        }
        if (attempt < policy.maxAttempts()) {
            clock.waitFor(backoff);
            backoff *= 2;          // 200ms, then 400ms
        }
    }
}""",
        narration=(
            "So somebody writes a proxy. It is about forty lines of Java, and "
            "the whole of it is one shape: read the policy, try, catch, wait, "
            "double the wait, try again. [[slnc 165]] Put it next to the other "
            "one and they are the same loop with four lines added. Wait. Then "
            "double how long you will wait next time. [[slnc 193]] The doubling "
            "is not decoration, and it is worth understanding why. If every "
            "retry in the whole shop waited a fixed two hundred milliseconds, "
            "then every service that failed at the same moment would come back "
            "at the same moment — and the provider's first breath after a bad "
            "second would be the entire shop arriving at once. Doubling spreads "
            "them out. [[slnc 165]] One honest note. A real production proxy "
            "would also add a small random amount to each wait, for exactly the "
            "same reason. This one does not, and that is deliberate: a random "
            "number would make the program print something different on every "
            "run, and every figure in this video is asserted by a test."
        ),
    ),
    dict(
        key="09-swap",
        kind="console",
        title="The Swap",
        body="""Act 4 - one line, and it is not in the service:

    port.install(java);

  before the swap, listening on localhost:8081: nginx
  checkout is on start number:       1
  checkout's configured endpoint:    http://localhost:8081/pay

  after the swap, listening:         java-proxy
  checkout is on start number:       1
  checkout's configured endpoint:    http://localhost:8081/pay
  payments services ever started:    1

  Checkout was not told.
  There is no method on it to tell.""",
        narration=(
            "Now put the new proxy on the port. That is one line, and the line "
            "is not in the service. [[slnc 165]] Look at what that line does "
            "not take. It takes a proxy. It does not take the service. It has "
            "nothing it could use to notify a service, and nothing it could use "
            "to restart one. There is no such thing to pass in, because there "
            "is no such step. [[slnc 193]] Before the swap, the thing listening "
            "on the local port is nginx, checkout is on start number one, and "
            "its configured endpoint is that same local address. After the "
            "swap, the thing listening is the Java proxy, checkout is still on "
            "start number one, and its configured endpoint is character for "
            "character the same. Payments services ever started, across the "
            "whole program: one. [[slnc 165]] And that start number staying "
            "still is not the demonstration being careful with itself. There is "
            "exactly one place in the entire program where a payments service "
            "is constructed, and it runs before the first act. A test reads the "
            "program's own source code, strips the comments out, and counts the "
            "constructions, so it stays that way. [[slnc 150]] Checkout was not "
            "told about any of this. There is no method on it to tell."
        ),
    ),
    dict(
        key="10-spacing",
        kind="console",
        title="The Same Wobble, The Same Three Attempts",
        body="""Act 5 - identical provider, identical bad 300ms,
  identical payment, identical allowance of three attempts:

    attempt at    1ms   declined
    attempt at  202ms   declined
    attempt at  603ms   charged
    3 attempts, first to last: 602ms

    ORD-4418     £47.99    pay_ORD-4418 (3 attempts)

  Still three attempts.
  The provider's allowance is untouched.
  Only the spacing changed.""",
        narration=(
            "Same provider. Same bad three hundred milliseconds. Same payment, "
            "and the same allowance of three attempts. [[slnc 165]] The first "
            "attempt arrived after one millisecond, and was declined. The "
            "second arrived after two hundred and two milliseconds, and was "
            "declined. The third arrived after six hundred and three "
            "milliseconds — and that one was charged. Three attempts, and from "
            "the first to the last, six hundred and two milliseconds. [[slnc "
            "193]] Now hold that against the earlier run and notice what is not "
            "different. Three attempts in both. The shop is not being greedier. "
            "The provider's allowance is completely untouched, and the provider "
            "did not get one extra request out of this change. It cost them "
            "nothing at all. [[slnc 165]] The only thing that changed is when "
            "the third attempt arrives. And by six hundred milliseconds, the "
            "provider is well again. [[slnc 150]] The spacing was the "
            "difference between a customer walking away and a coffee maker "
            "being sold."
        ),
    ),
    dict(
        key="11-roles",
        kind="diagram",
        title="What Is Actually In This Program",
        body=None,
        narration=(
            "Let me name the pieces, because there are not many of them. "
            "[[slnc 165]] There is a payments service, and it has two things "
            "in it: a name, and a local port to send payments to. That is all "
            "it has. A test reads its source code and fails if the words retry, "
            "backoff, timeout, keystore or certificate ever appear in it. "
            "[[slnc 165]] There is the local port itself, which is the hinge of "
            "the whole project. It holds one thing: whatever proxy is currently "
            "bound to it. You can install something, you can empty it, and you "
            "can send a payment to it — and if nothing is bound, sending gets "
            "you a connection refused. [[slnc 165]] There is an interface "
            "called Proxy, which is just a shape: a name, a language, a line "
            "count, and a method that forwards a payment. Two classes implement "
            "it. One is the nginx proxy, one is the Java proxy, and they hold "
            "exactly the same three things — the name of the service they stand "
            "beside, the provider, and the policy. [[slnc 193]] And that policy "
            "is the piece worth pausing on. It is one object, and both proxies "
            "read that same one object. Not a copy each. Because four equal "
            "copies of a policy would be the old problem back again with better "
            "manners. [[slnc 165]] Look at what neither proxy holds: nothing "
            "about the shop. No basket. No order. No refund window. No "
            "customer. That is the test for whether something belongs in a "
            "proxy at all — and remember it, because it is about to get much "
            "harder to enforce."
        ),
    ),
    dict(
        key="12-the-gap-window",
        kind="console",
        title="The Gap In The Middle Of A Swap",
        body="""Act 6 - a swap is not instant. The old proxy stops,
  and for a moment there is nothing on the port at all.

  The provider is healthy. The network is healthy.
  Checkout is healthy. A customer pays for a £31.50 kettle:

    ORD-4419     £31.50    NOT PAID
      connection refused to localhost:8081 — nothing is listening

  attempts that reached the provider: 0

  Nothing in the provider's dashboards
  will ever show that this happened.""",
        narration=(
            "There is a cost here, and it is the one that will actually page "
            "somebody, so we are going to look at it rather than skip past it. "
            "[[slnc 165]] A swap is not instant. The old proxy stops, and the "
            "new one starts, and in between there is a moment when nothing at "
            "all is listening on that port. [[slnc 193]] So: the payment "
            "provider is healthy. The network is healthy. The checkout service "
            "is healthy. A customer pays thirty-one pounds fifty for a kettle, "
            "and the payment fails instantly, with a connection refused, "
            "because nothing is listening. [[slnc 165]] And the number to "
            "listen for is the next one. Attempts that reached the provider: "
            "zero. The request never left the machine. Which also means nothing "
            "in the provider's dashboards will ever show that it happened. "
            "[[slnc 165]] And there is nothing to fall back on, because the "
            "retry code that would have covered this was deleted in the "
            "previous project — and deleting it was the right call. But it does "
            "mean the swap window is a window of hard, immediate failures "
            "rather than slow ones. [[slnc 193]] So a real swap is not one line "
            "in a demonstration. It is a rollout. Start the new proxy before "
            "you stop the old one. Move one service at a time. And keep the old "
            "proxy installable — because the honest reason to be able to swap "
            "forwards is to be able to swap back."
        ),
    ),
    dict(
        key="13-demonstration",
        kind="console",
        title="A Claim Is Not A Demonstration",
        body="""Act 7 - the table this project exists for:

    proxy        language              lines
    nginx        nginx configuration      22
    java-proxy   Java                     40

  what nginx has no words for:
    wait 200ms between attempts, doubling
  what java-proxy has no words for:
    nothing

  Two proxies. Two languages. One port.
  One service whose source file did not change.""",
        narration=(
            "So here is what all of that actually bought. [[slnc 165]] The "
            "previous project made a claim: that a sidecar is language "
            "independent, that the proxy may be written in a language nobody on "
            "your team knows, and that the service will not care. [[slnc 150]] "
            "That claim was true, and it was completely unsupported. Every "
            "single line of evidence in that project was Java talking to Java. "
            "[[slnc 193]] Here there are two proxies. One is configured in "
            "nginx's configuration language, in twenty-two lines. The other is "
            "written in Java, in forty. They go on the same port, beside the "
            "same service, and they are handed the same policy object. And the "
            "service's source file is byte for byte identical in both runs. "
            "[[slnc 165]] That is not a claim about language independence. That "
            "is language independence, happening."
        ),
    ),
    dict(
        key="14-bill",
        kind="bullets",
        title="The Bill, Which Is Longer",
        body=[
            "✗  22 lines of somebody else's configuration",
            "       became 40 lines of your own code",
            "",
            "✗  gone until you write them: TLS termination,",
            "       a structured access log, connection pooling,",
            "       twenty years of security advisories answered",
            "",
            "✗  a JVM beside every service, where a few",
            "       megabytes of nginx used to sit",
            "",
            "✗  and nothing now stops the next person putting",
            "       the shop's refund rules in the proxy",
        ],
        narration=(
            "And now the bill, because a pattern taught without its costs is an "
            "advertisement. This bill is longer than the benefit, and most of it "
            "argues against doing any of this. [[slnc 193]] Twenty-two lines of "
            "somebody else's configuration became forty lines of your own code. "
            "That code is now yours. Yours to test, yours to review, yours to "
            "keep working on the next version of Java, and yours to fix at "
            "three in the morning. Nobody is patching it for you while you "
            "sleep. [[slnc 165]] Everything nginx brought for free is gone "
            "until you write it. Transport security termination. A structured "
            "access log, in a format every service in the shop already shares. "
            "Connection pooling. Header handling that nobody has to think "
            "about. And twenty years of somebody answering security advisories "
            "before you had even heard of them. A forty-line proxy that grows "
            "all of that back is not a forty-line proxy any more. [[slnc 165]] "
            "A whole Java virtual machine now sits beside every service, where "
            "a few megabytes of nginx used to sit. Multiply that by the number "
            "of services you run, and then go and look at what that costs on "
            "the machines you actually rent. [[slnc 193]] And here is the one "
            "that is not on any invoice. Nothing now stops the next person "
            "putting the shop's refund rules into the proxy. A configuration "
            "language is a fence: there is simply no way to express refunds are "
            "not allowed after ninety days in an nginx config block, so nobody "
            "ever tries. Java will happily let them. And a business rule hidden "
            "in a proxy is a business rule that no developer will ever think to "
            "go looking for. [[slnc 165]] The limitation and the fence were the "
            "same thing. You took the fence down at the exact moment you took "
            "the limitation away."
        ),
    ),
    dict(
        key="15-rule",
        kind="quote",
        title="The Rule To Take Away",
        body=[
            "Swap the proxy when the thing you need",
            "cannot be said in the configuration",
            "language at all.",
            "",
            "Not when it is awkward.",
            "Not when the config file has grown ugly.",
            "Not when you would rather write Java.",
            "",
            "— here, the missing sentence was the difference between",
            "— a payment going through and a payment failing.",
            "— Very little else clears that bar.",
        ],
        narration=(
            "So the rule is narrow, and it is the thing to remember when the "
            "demonstration has faded. [[slnc 165]] Swap the proxy when the "
            "thing you need cannot be said in the configuration language at "
            "all. [[slnc 193]] Not when it is awkward. Not when the "
            "configuration file has grown ugly. And not when you would rather "
            "write Java — which you would, because everybody would. [[slnc "
            "165]] Here, the missing sentence was the difference between a "
            "payment going through and a payment failing. That clears the bar. "
            "Very little else does. Most of the time the right answer is to "
            "keep nginx, accept the gap, and spend the afternoon on something "
            "that matters more. [[slnc 193]] But here is what is worth keeping "
            "either way, and it is the real prize. The choice was available. "
            "Because the service talks to an address rather than to a library, "
            "swapping the proxy was a decision somebody could make on a Tuesday "
            "afternoon — and swapping it back is the same decision in the other "
            "order. [[slnc 150]] That option is what the previous project "
            "actually bought you, and this is what it looks like when somebody "
            "finally spends it."
        ),
    ),
    dict(
        key="16-takeaway",
        kind="bullets",
        title="What To Remember",
        body=[
            "✓  the contract is an address — so the thing at",
            "       the other end of it is replaceable",
            "",
            "✓  same three attempts, spaced: 1ms, 202ms, 603ms",
            "       instead of 1ms, 2ms, 3ms — and the provider",
            "       gets no extra traffic at all",
            "",
            "✓  proved by identity, not by behaviour",
            "",
            "✗  a swap is a rollout: start the new one first,",
            "       and keep the old one installable",
        ],
        narration=(
            "Four things to take away. [[slnc 165]] First: the contract between "
            "a service and the helper beside it is an address, and that is why "
            "the thing on the other end of it is replaceable. Weak contracts "
            "buy you options. [[slnc 165]] Second: the fix was the same three "
            "attempts, spaced out. One millisecond, two hundred and two, six "
            "hundred and three — instead of one, two and three. The provider "
            "got no extra traffic out of it at all. When something is failing, "
            "asking better is usually available before asking more. [[slnc "
            "165]] Third: the swap was proved by identity rather than by "
            "behaviour. The test asserts that the service object afterwards is "
            "the same object, not that it behaves the same — because a service "
            "that merely behaves the same afterwards is a service somebody may "
            "have carefully rebuilt. [[slnc 165]] And fourth: a swap is a "
            "rollout, not an assignment. Start the new proxy before you stop the "
            "old one, move one service at a time, and keep the old one "
            "installable."
        ),
    ),
    dict(
        key="17-outro",
        kind="outro",
        title="Thanks for watching",
        body=[
            "Code, documents and the animated walkthrough:",
            "gradle-java/platform-design-patterns/sidecar-java-proxy-pattern",
            "",
            "Written and presented by Jayasekhar Konduru",
        ],
        narration=(
            "Thanks for watching. [[slnc 165]] The full project is in the "
            "repository, including the two proxies side by side, the tests that "
            "hold every number in this video in place, and an animated "
            "walkthrough you can step through in a browser. [[slnc 165]] If "
            "this was useful, please like the video and subscribe — it genuinely "
            "helps. And if you disagree with the rule at the end, I would like "
            "to hear why in the comments. [[slnc 150]] This was written and "
            "presented by Jayasekhar Konduru. See you in the next one."
        ),
    ),
]

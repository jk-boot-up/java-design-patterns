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
            'Hello, and welcome. [[slnc 400]] This video explains how to '
            'swap out a sidecar proxy, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] When a service talks to a '
            'helper program beside it, the only thing connecting them is '
            'an address. [[slnc 300]] Not a library, and not a shared '
            'language. [[slnc 300]] So whatever listens at that address '
            'can be replaced, even with something in a different '
            'language. [[slnc 300]] And the service is never told. [[slnc '
            '600]] Think of the plug on a kettle. [[slnc 300]] The kettle '
            'knows nothing about the electricity. [[slnc 300]] If the '
            'fuse in the plug is wrong, you change the fuse. [[slnc 300]] '
            'You do not open the kettle. [[slnc 600]] This video follows '
            'on from the Sidecar video. [[slnc 300]] If you have not seen '
            'that one, watch it first. [[slnc 700]] In our online store, '
            'a payment provider has a bad three hundred milliseconds. '
            "[[slnc 300]] The shop's proxy cannot express what the "
            'provider asked for. [[slnc 300]] And a forty-line '
            'replacement goes on the same port, beside a service that is '
            'never rebuilt or restarted. [[slnc 500]] By the end, you '
            'will know why retrying immediately is wrong here. [[slnc '
            '300]] What writing your own proxy costs. [[slnc 300]] And '
            'the narrow rule for when you should.'
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
            'First, one minute on where we are. [[slnc 400]] The shop '
            'takes payments at checkout. [[slnc 300]] The code that talks '
            'to the payment provider used to live inside that service. '
            '[[slnc 300]] In the Sidecar video, it moved into a small '
            'separate program beside the service. [[slnc 300]] Everything '
            'about talking to the provider, how often to retry and when '
            'to give up, is written once, in one file that the proxy '
            "reads. [[slnc 600]] So checkout's whole configuration for "
            'payments is now one line. [[slnc 300]] An address on its own '
            'machine. [[slnc 300]] Whatever listens there answers, and '
            'checkout cannot tell what it is. [[slnc 600]] Today, the '
            'thing listening there is nginx, a well-known web server. '
            '[[slnc 300]] About twenty-two lines of settings. [[slnc '
            '300]] Written, tested, and patched by other people, for '
            'twenty years. [[slnc 300]] That was a good decision. [[slnc '
            '500]] Remember one thing: the contract between the service '
            'and its neighbour is just an address.'
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
            'In March, the payment provider writes to every shop. [[slnc '
            '300]] It asks for two things. [[slnc 500]] At most three '
            'attempts per payment. [[slnc 300]] And wait properly between '
            'them. [[slnc 600]] The second part matters. [[slnc 300]] '
            'Retrying ten milliseconds after a failure does not help. '
            '[[slnc 300]] The problem has not had time to clear. [[slnc '
            '300]] So try again, but leave a real gap. [[slnc 600]] The '
            'shop agrees to both. [[slnc 300]] The settings say three '
            'attempts. [[slnc 300]] Everyone goes home. [[slnc 600]] But '
            'listen again to the second part: wait properly between them. '
            "[[slnc 300]] The shop's proxy can express the first half. "
            '[[slnc 300]] It cannot express the second.'
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
            'First demo: three attempts that bought nothing. [[slnc 400]] '
            'The provider has a bad three hundred milliseconds. [[slnc '
            '300]] It declines everything for a moment, and then it is '
            'fine. [[slnc 600]] A customer buys a coffee maker for '
            'forty-seven pounds ninety-nine. [[slnc 300]] The proxy makes '
            'its three allowed attempts. [[slnc 300]] The times are '
            'recorded by the provider itself, which is real evidence. '
            '[[slnc 600]] The first attempt arrives after one '
            'millisecond, and is declined. [[slnc 300]] The second, after '
            'two milliseconds, declined. [[slnc 300]] The third, after '
            'three milliseconds, declined. [[slnc 300]] All three '
            'attempts, within two milliseconds. [[slnc 600]] The provider '
            'did not recover until three hundred milliseconds. [[slnc '
            '300]] So every attempt landed inside the bad moment. [[slnc '
            '300]] And the customer got nothing. [[slnc 500]] The half of '
            'the agreement that limits the shop was kept. [[slnc 300]] '
            'The half that would have helped was not.'
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
            "The obvious response is to fix the proxy's settings. [[slnc "
            '300]] But there is nothing to fix them with. [[slnc 600]] '
            'nginx does not have a retry setting as you might imagine. '
            '[[slnc 300]] It has a list of servers, and a rule. [[slnc '
            '300]] If this one fails, try the next one on the list. '
            "[[slnc 300]] The shop's settings list the provider's address "
            'three times. [[slnc 300]] Because that is how you say three '
            'attempts, when there is only one address. [[slnc 500]] And '
            'moving to the next entry happens immediately. [[slnc 600]] '
            'That makes sense for what it was designed for. [[slnc 300]] '
            'Picture ten web servers. [[slnc 300]] If the ninth fails, '
            'the tenth is a different computer, and probably healthy. '
            '[[slnc 300]] Waiting would just slow every request down. '
            '[[slnc 600]] But here, every entry is the same address. '
            '[[slnc 300]] And that address is the one having a bad '
            'moment. [[slnc 300]] Three instant attempts at the same '
            'unwell thing all get the same answer. [[slnc 600]] So nobody '
            'wrote a bug. [[slnc 300]] nginx simply has no way to say: '
            'wait two hundred milliseconds before the next attempt. '
            '[[slnc 300]] The sentence does not exist in its language.'
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
            'There are three ways out of this. [[slnc 300]] Two of them '
            'are bad. [[slnc 600]] The first: put the waiting back inside '
            'the service. [[slnc 300]] That undoes the Sidecar video. '
            '[[slnc 300]] Four services would need four copies of the '
            'waiting. [[slnc 300]] And the next rule change would be '
            'missed in one of them. [[slnc 600]] The second: add a script '
            'inside nginx, in a language called Lua. [[slnc 300]] That '
            'can express a delay. [[slnc 300]] But now you are writing '
            'code inside a proxy you chose because it needed no code. '
            '[[slnc 300]] In a language your team rarely uses, and hard '
            'to test. [[slnc 600]] The third: put a different proxy on '
            'the port. [[slnc 500]] That option only exists because of a '
            'decision in the Sidecar video. [[slnc 300]] The contract '
            'between the service and its proxy is an address. [[slnc '
            '300]] The service sends a request to a local address, and '
            'something answers. [[slnc 300]] Nothing about that is Java, '
            'and nothing about it is nginx.'
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
            "Here is the nginx proxy's retry loop, written out in Java, "
            'so we can see it. [[slnc 500]] Try the provider. [[slnc '
            '300]] If it fails, go round again. [[slnc 300]] If the '
            'provider says the allowance is used up, stop at once. [[slnc '
            '600]] And at the bottom of the loop, there is just a '
            'comment. [[slnc 300]] It says: this is where the waiting '
            'would go, if it could be expressed at all. [[slnc 600]] That '
            'empty space is the whole subject of this video. [[slnc 300]] '
            'It is not empty because someone forgot. [[slnc 300]] It is '
            'empty because there was nothing to write.'
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
            'So someone writes their own proxy. [[slnc 300]] About forty '
            'lines of Java. [[slnc 500]] Read the rules. [[slnc 200]] '
            'Try. [[slnc 200]] If it fails, wait. [[slnc 200]] Double the '
            'wait. [[slnc 200]] Try again. [[slnc 600]] Compared with the '
            'nginx version, it is the same loop, with four lines added. '
            '[[slnc 300]] Wait. [[slnc 300]] Then double how long to wait '
            'next time. [[slnc 600]] Why double? [[slnc 300]] If every '
            'retry in the shop waited exactly two hundred milliseconds, '
            'every service that failed together would come back together. '
            "[[slnc 300]] And the provider's first moment of recovery "
            'would be the whole shop arriving at once. [[slnc 300]] '
            'Doubling spreads them out. [[slnc 600]] A real proxy would '
            'also add a small random amount to each wait. [[slnc 300]] '
            'This one does not, on purpose. [[slnc 300]] So every number '
            'in this video stays the same, and can be checked by a test.'
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
            'Second demo: the swap. [[slnc 400]] Put the new proxy on the '
            'port. [[slnc 300]] That is one line, and it is not in the '
            'service. [[slnc 600]] That line takes a proxy. [[slnc 300]] '
            'It does not take the service. [[slnc 300]] It has no way to '
            'notify or restart a service. [[slnc 600]] Before the swap, '
            'nginx is listening on the local port. [[slnc 300]] Checkout '
            'is on its first start. [[slnc 300]] And its configured '
            'address is that local port. [[slnc 500]] After the swap, the '
            'Java proxy is listening. [[slnc 300]] Checkout is still on '
            'its first start. [[slnc 300]] And its configured address is '
            'exactly the same. [[slnc 600]] There is only one place in '
            'the whole program where a payment service is created. [[slnc '
            "300]] And a test checks the program's own code to keep it "
            'that way. [[slnc 500]] Checkout was never told about any of '
            'this. [[slnc 300]] There is no way to tell it.'
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
            'Third demo: the same wobble, and the same three attempts. '
            '[[slnc 400]] Same provider, same bad three hundred '
            'milliseconds, same payment, same allowance. [[slnc 600]] The '
            'first attempt arrives after one millisecond, and is '
            'declined. [[slnc 300]] The second, after two hundred and two '
            'milliseconds, declined. [[slnc 300]] The third, after six '
            'hundred and three milliseconds. [[slnc 300]] And that one is '
            'charged. [[slnc 600]] Notice what did not change. [[slnc '
            '300]] Three attempts in both runs. [[slnc 300]] The shop is '
            'not being greedier. [[slnc 300]] The provider got no extra '
            'requests at all. [[slnc 500]] The only change is when the '
            'attempts arrive. [[slnc 300]] And by six hundred '
            'milliseconds, the provider is well again. [[slnc 500]] The '
            'spacing was the difference between a lost customer, and a '
            'coffee maker sold.'
        ),
    ),
    dict(
        key="11-roles",
        kind="diagram",
        title="What Is Actually In This Program",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are only a few. "
            '[[slnc 600]] First, a payment service. [[slnc 300]] It holds '
            'just two things: a name, and a local port to send payments '
            'to. [[slnc 300]] A test fails if words like retry, backoff, '
            'or timeout ever appear in its code. [[slnc 500]] Second, the '
            'local port, which is the hinge of the project. [[slnc 300]] '
            'It holds whichever proxy is currently plugged into it. '
            '[[slnc 300]] If nothing is plugged in, sending a payment '
            'gets connection refused. [[slnc 500]] Third, a proxy '
            'interface, with two versions: the nginx proxy, and the Java '
            'proxy. [[slnc 300]] Both hold the same three things: which '
            'service they sit beside, the provider, and the rules. [[slnc '
            '500]] Both read the very same rules object. [[slnc 300]] Not '
            'a copy each. [[slnc 600]] And notice what neither proxy '
            'holds. [[slnc 300]] Nothing about the shop. [[slnc 300]] No '
            'basket, no order, no refund rules, no customer. [[slnc 300]] '
            'That is the test for what belongs in a proxy. [[slnc 300]] '
            'Remember it, because it is about to get harder to enforce.'
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
            'Fourth demo: the gap in the middle of a swap. [[slnc 400]] A '
            'swap is not instant. [[slnc 300]] The old proxy stops, and '
            'the new one starts. [[slnc 300]] In between, nothing is '
            'listening on the port. [[slnc 600]] The provider is healthy. '
            '[[slnc 300]] The network is healthy. [[slnc 300]] Checkout '
            'is healthy. [[slnc 300]] A customer pays thirty-one pounds '
            'fifty for a kettle. [[slnc 300]] And the payment fails '
            'instantly: connection refused. [[slnc 600]] Attempts that '
            'reached the provider: zero. [[slnc 300]] The request never '
            "left the machine. [[slnc 300]] So the provider's dashboards "
            'will never show it happened. [[slnc 600]] And there is '
            "nothing to fall back on, because the service's retry code "
            'was removed on purpose. [[slnc 600]] So a real swap is not '
            'one line. [[slnc 300]] It is a careful rollout. [[slnc 300]] '
            'Start the new proxy before stopping the old one. [[slnc '
            '300]] Move one service at a time. [[slnc 300]] And keep the '
            'old proxy ready, so you can swap back.'
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
            'So here is what all of that really bought. [[slnc 500]] The '
            'Sidecar video claimed that a sidecar is language '
            'independent. [[slnc 300]] That the proxy could be written in '
            'any language, and the service would not care. [[slnc 300]] '
            'That was true, but unproven. [[slnc 300]] Every piece of '
            'evidence there was Java talking to Java. [[slnc 600]] Here, '
            'there are two proxies. [[slnc 300]] One is nginx settings, '
            'twenty-two lines. [[slnc 300]] The other is Java, forty '
            'lines. [[slnc 300]] They sit on the same port, beside the '
            'same service, reading the same rules. [[slnc 300]] And the '
            "service's code is exactly the same in both runs. [[slnc "
            '500]] That is not a claim about language independence. '
            '[[slnc 300]] That is language independence, happening.'
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
            'Now the bill. [[slnc 300]] It is longer than the benefit, '
            'and most of it argues against doing this. [[slnc 600]] '
            "Twenty-two lines of someone else's settings became forty "
            'lines of your own code. [[slnc 300]] Now you must test it, '
            'review it, keep it working, and fix it at three in the '
            'morning. [[slnc 300]] Nobody is patching it for you. [[slnc '
            '600]] Everything nginx gave for free is gone until you write '
            'it. [[slnc 300]] Network encryption, a standard access log, '
            'connection reuse, and twenty years of security fixes. [[slnc '
            '300]] A forty-line proxy that grows all that back is no '
            'longer forty lines. [[slnc 600]] A whole Java runtime now '
            'sits beside every service, where a few megabytes of nginx '
            'used to be. [[slnc 300]] Multiply that by the number of '
            'services you run. [[slnc 600]] And one cost that appears on '
            'no invoice. [[slnc 300]] Nothing now stops someone putting '
            "the shop's refund rules into the proxy. [[slnc 300]] nginx "
            'settings simply cannot express a refund rule, so nobody '
            'tries. [[slnc 300]] Java can express anything. [[slnc 300]] '
            'And a business rule hidden in a proxy is one nobody will '
            'think to look for. [[slnc 500]] The limitation and the fence '
            'were the same thing. [[slnc 300]] Removing one removed the '
            'other.'
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
            'So the rule is narrow. [[slnc 400]] Swap the proxy when what '
            'you need cannot be expressed in its settings at all. [[slnc '
            '600]] Not when it is awkward. [[slnc 300]] Not when the '
            'settings file has grown ugly. [[slnc 300]] And not just '
            'because you would rather write Java. [[slnc 600]] Here, the '
            'missing sentence was the difference between a payment '
            'succeeding, and failing. [[slnc 300]] That clears the bar. '
            '[[slnc 300]] Very little else does. [[slnc 300]] Most of the '
            'time, keep nginx, and accept the gap. [[slnc 600]] But here '
            'is the real prize, either way. [[slnc 300]] Because the '
            'service talks to an address, not a library, swapping the '
            'proxy is a choice anyone can make on a Tuesday afternoon. '
            '[[slnc 300]] And swapping back is the same choice, in '
            'reverse.'
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
            'Here are four things to remember. [[slnc 500]] One. [[slnc '
            '200]] The contract between a service and its helper is an '
            'address. [[slnc 300]] That is why the helper can be '
            'replaced. [[slnc 300]] Weak contracts buy you options. '
            '[[slnc 400]] Two. [[slnc 200]] The fix was the same three '
            'attempts, spaced out. [[slnc 300]] One, two hundred and two, '
            'and six hundred and three milliseconds, instead of one, two, '
            'and three. [[slnc 300]] The provider got no extra traffic. '
            '[[slnc 300]] Asking better often works before asking more. '
            '[[slnc 400]] Three. [[slnc 200]] The swap was proved by '
            'checking that the service afterwards is the very same '
            'object. [[slnc 300]] Not just that it behaves the same. '
            '[[slnc 400]] Four. [[slnc 200]] A swap is a rollout, not a '
            'single step. [[slnc 300]] Start the new proxy first, move '
            'one service at a time, and keep the old one ready.'
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
            "That's swapping a Sidecar, with a Java proxy. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'Because a service talks to its sidecar through an address, '
            'the sidecar can be replaced, but only replace it when what '
            'you need truly cannot be said any other way. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'Including both proxies, side by side, and the tests that '
            'hold every number in place. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]

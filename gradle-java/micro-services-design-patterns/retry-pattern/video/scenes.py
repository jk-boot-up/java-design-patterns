"""Scene definitions for the Retry with Backoff teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the code slides are described in words rather than read out as
syntax. The slides illustrate the narration; they never carry it.

Every number quoted in these scenes comes from the real output of
`./gradlew run`: one attempt costs 50ms, the backoff wait is 103ms rather than
100 because of jitter, a recovered checkout lands at 203ms, and the two totals
that the whole video turns on are £449.99 for one charge and £899.98 for two.

Scene order is the argument. The pattern is shown *working* in scenes four to
seven before the lost reply is mentioned at all, because the room has to
believe in retrying before it is shown the trap inside it. Do not move the
lost-reply scenes earlier.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines
is the maximum.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Retry with Backoff",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Retry with Backoff pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] When a call to another '
            'service fails for a reason that might not happen again, you '
            'try once or twice more. [[slnc 300]] Each time, you wait a '
            'little longer first. [[slnc 300]] And you only do this if '
            'doing the job twice cannot actually do it twice. [[slnc '
            '500]] That last part is the half everybody skips. [[slnc '
            '300]] And it is the half that costs money. [[slnc 600]] '
            'Think of calling a friend whose line is busy. [[slnc 300]] '
            'You wait a minute and try again. [[slnc 300]] But if they '
            'say no, calling back will not turn it into a yes. [[slnc '
            '700]] In our online store, the shop takes card payments '
            'through a payment gateway, on the other side of the '
            'internet. [[slnc 300]] About one call in five fails, for '
            'reasons that have nothing to do with the payment. [[slnc '
            '500]] By the end, you will know which failures are worth '
            'retrying. [[slnc 300]] Why the waits get longer, and are '
            'deliberately not all the same. [[slnc 300]] And the failure '
            'that charges a shopper twice, while every test still passes.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shop takes card payments through somebody",
            "else's gateway, across the internet.",
            "",
            "About one call in five fails for a reason that has",
            "nothing to do with the payment:",
            "",
            "    a dropped connection  ·  a router that reset",
            "",
            "The bank is fine. The money is there. The request",
            "simply did not make the round trip.",
            "",
            "One espresso machine. £449.99. One error page.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop sells an '
            'espresso machine for four hundred and forty-nine pounds '
            'ninety-nine. [[slnc 300]] To take the money, it calls a '
            'payment gateway owned by someone else, across the internet. '
            '[[slnc 600]] About one call in five fails. [[slnc 300]] And '
            'those failures have nothing to do with the payment. [[slnc '
            '300]] A connection drops. [[slnc 300]] A router somewhere '
            'resets. [[slnc 300]] The bank is fine, and the money is '
            'there. [[slnc 300]] The request simply did not make the '
            'round trip. [[slnc 600]] Think about what that means for the '
            'shop. [[slnc 300]] Each one is a shopper who chose a '
            'product, typed in a card number, pressed pay, and got an '
            'error page. [[slnc 300]] They did nothing wrong. [[slnc '
            '300]] And most of them do not come back.'
        ),
    ),
    dict(
        key="03-just-try-again",
        kind="code",
        title="The Obvious Answer — Just Try Again",
        body="""for (int attempt = 1; attempt <= 3; attempt++) {
    try {
        return payments.charge(request);
    } catch (RuntimeException failure) {
        // try again
    }
}

// no bug, no slowness, no failing test, nothing to notice""",
        narration=(
            'Ask any room of developers what to do, and someone will say: '
            'just try again. [[slnc 400]] And they are right. [[slnc '
            '300]] That really is the idea. [[slnc 500]] Loop up to three '
            'times. [[slnc 300]] Call the gateway. [[slnc 300]] If it '
            'fails, go round again. [[slnc 600]] To be fair, almost '
            'everybody writes this first, and it is not stupid. [[slnc '
            '300]] It rescues checkouts. [[slnc 300]] It has nothing to '
            'configure wrongly. [[slnc 300]] And every test written '
            'against it passes. [[slnc 600]] So remember that. [[slnc '
            '300]] The rest of this video is about what the word just is '
            'hiding. [[slnc 300]] And the answer is not a bug. [[slnc '
            '300]] It is one line of code in the wrong place.'
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act One — A Timeout That Recovers",
        body="""$ ./gradlew run

1. The gateway timed out once, then worked
      0ms ->    50ms  Payments    TIMEOUT   request never arrived
     50ms ->    50ms  Retrier     RETRYABLE attempt 1 failed
    153ms ->   153ms  Retrier     WAITED    103ms before attempt 2
    153ms ->   203ms  Payments    CHARGED   chg-1 £449.99
    203ms ->   203ms  Retrier     RECOVERED succeeded on attempt 2

  checkout succeeded: chg-1 £449.99
  card charged 1 time, £449.99 in total""",
        narration=(
            'First demo: a timeout that recovers. [[slnc 300]] The good '
            "case is real, so let's hear it. [[slnc 600]] The first "
            'attempt goes out, and the gateway times out. [[slnc 300]] '
            'Nothing was charged, because the request never arrived. '
            '[[slnc 500]] The retrier looks at that failure, and decides '
            'it is worth another try. [[slnc 300]] It waits a moment, and '
            'calls again. [[slnc 300]] The second attempt goes through. '
            '[[slnc 300]] The card is charged, and the checkout succeeds. '
            '[[slnc 600]] Here is the only number that matters in this '
            'video. [[slnc 300]] The card was charged one time. [[slnc '
            '500]] The shopper waited about two hundred milliseconds, '
            'instead of fifty. [[slnc 300]] And in return, they got a '
            'finished order instead of an error page. [[slnc 300]] That '
            'is a good trade. [[slnc 600]] But notice one small thing. '
            '[[slnc 300]] The retrier waited one hundred and three '
            'milliseconds, not one hundred. [[slnc 300]] Hold that '
            'thought.'
        ),
    ),
    dict(
        key="05-backoff-jitter",
        kind="bullets",
        title="Wait Longer Each Time — And Not All The Same",
        body=[
            "Backoff:  100ms, then 200ms, then 400ms.",
            "",
            "Not politeness. If the gateway is failing because",
            "it is overloaded, the thing that makes the next",
            "attempt work is the gateway getting some room.",
            "",
            "Jitter:  every caller waits a slightly different",
            "amount — 103ms here, 117ms for somebody else.",
            "",
            "A thousand callers all waiting exactly 100ms",
            "come back as one wave, at the same instant.",
            "The stampede just repeats itself, on a timer.",
        ],
        narration=(
            'Those three extra milliseconds have a name. [[slnc 300]] But '
            'first, the wait itself. [[slnc 600]] The retrier does not go '
            'straight back. [[slnc 300]] It waits a hundred milliseconds '
            'before the second attempt. [[slnc 300]] It would wait two '
            'hundred before a third, and four hundred before a fourth. '
            '[[slnc 300]] Each wait is longer than the last. [[slnc 300]] '
            'That is called backoff. [[slnc 600]] The reason is not '
            'politeness. [[slnc 300]] If the gateway is failing because '
            'it is overloaded, it needs room to recover. [[slnc 300]] A '
            'caller that retries instantly takes that room away. [[slnc '
            '600]] Now, the extra three milliseconds. [[slnc 300]] Each '
            'caller waits a slightly different, random amount. [[slnc '
            '300]] That is called jitter. [[slnc 500]] With one caller, '
            'it seems pointless. [[slnc 300]] So picture a thousand '
            'callers instead. [[slnc 300]] They all failed at the same '
            'moment, because the same thing went wrong for all of them. '
            '[[slnc 300]] If they all wait exactly a hundred '
            'milliseconds, they all come back at exactly the same moment. '
            '[[slnc 300]] One big wave, and the crush that knocked the '
            'gateway over simply happens again. [[slnc 500]] Jitter '
            'spreads them out, and turns the wave into a trickle.'
        ),
    ),
    dict(
        key="06-classify",
        kind="code",
        title="Not Every Failure Is Worth Another Go",
        body="""private boolean worthRetrying(RuntimeException failure) {
    return failure instanceof GatewayTimeoutException;
}

// retry what you RECOGNISE.
// the opposite rule -- "retry unless I recognise it" --
// eventually retries a NullPointerException four hundred
// times, to get four hundred identical crashes.""",
        narration=(
            "That was the retrier's first decision: how long to wait. "
            '[[slnc 300]] Here is its second decision. [[slnc 300]] Is '
            'this failure worth trying again at all? [[slnc 600]] A '
            'timeout might not happen a second time. [[slnc 300]] So, '
            'yes. [[slnc 500]] But suppose the bank declines the card. '
            '[[slnc 300]] That is not a network hiccup. [[slnc 300]] That '
            'is an answer. [[slnc 300]] No funds, a wrong expiry date, or '
            'a block on the account. [[slnc 300]] All still true a '
            'hundred milliseconds later. [[slnc 600]] So the rule is '
            'deliberate. [[slnc 300]] Retry only the failures you '
            'recognise as temporary. [[slnc 300]] Treat everything else '
            'as permanent. [[slnc 500]] The tempting rule is the other '
            'way round: retry everything, unless you know it is hopeless. '
            '[[slnc 300]] Write it that way, and one day a bug in your '
            'own code is retried four hundred times, to produce four '
            'hundred identical crashes.'
        ),
    ),
    dict(
        key="07-act-two",
        kind="console",
        title="Act Two — A Declined Card",
        body="""2. The bank declined the card
      0ms ->    50ms  Payments    DECLINED  the bank said no
     50ms ->    50ms  Retrier     PERMANENT not retrying

  checkout declined, and the shopper was told at once
  the gateway was asked 1 time

  a 'no' does not become a 'yes' on the third attempt""",
        narration=(
            'Second demo: a declined card. [[slnc 400]] The result is '
            'short, and that is the point. [[slnc 500]] One attempt. '
            '[[slnc 300]] Fifty milliseconds. [[slnc 300]] The bank said '
            'no. [[slnc 300]] The retrier recognised that as a permanent '
            'answer. [[slnc 300]] So the shopper was told at once. [[slnc '
            '600]] Compare that with the plain three-times loop. [[slnc '
            '300]] It asks the gateway three times, and waits twice, to '
            'get exactly the same no. [[slnc 500]] The shopper waits '
            'longer to hear the same thing. [[slnc 300]] The gateway does '
            'three times the work, for nothing. [[slnc 300]] And on a bad '
            "day, you triple your traffic against someone else's service."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Pieces, And What Each One Decides",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are only four. "
            '[[slnc 600]] First, the checkout service, which is the '
            'caller. [[slnc 300]] It builds the payment request. [[slnc '
            '300]] Then it asks a retrier to make the call. [[slnc 300]] '
            'The order of those two steps turns out to be the whole '
            'safety of this project. [[slnc 500]] Second, the retrier. '
            '[[slnc 300]] It is the loop, and it makes the two decisions '
            'we have heard. [[slnc 300]] Is this failure worth another '
            'try? [[slnc 300]] And how long should I wait? [[slnc 500]] '
            'Third, the retry policy. [[slnc 300]] It answers only the '
            'second question: how long. [[slnc 300]] A hundred '
            'milliseconds, doubling each time, plus a little jitter. '
            '[[slnc 500]] Fourth, the payment gateway, which is the thing '
            'that fails. [[slnc 300]] It can fail in three ways. [[slnc '
            '300]] It can time out before the request arrives. [[slnc '
            '300]] It can decline the card. [[slnc 300]] Or, and we have '
            'not met this one yet, it can take the money, and then lose '
            'the reply on the way back. [[slnc 600]] One more thing about '
            'the retrier. [[slnc 300]] It knows nothing about payments or '
            'money. [[slnc 300]] That makes it reusable. [[slnc 300]] And '
            'it is exactly why it cannot warn you when something is '
            'unsafe to repeat.'
        ),
    ),
    dict(
        key="09-lost-reply",
        kind="quote",
        title="The Failure You Cannot See",
        body=[
            "The request arrives.",
            "The card IS charged.",
            "The reply is lost on the way home.",
            "",
            "So what does the caller see?",
            "",
            "A timeout. The same timeout as act one,",
            "byte for byte.",
            "",
            "No flag. No header. No clever code.",
            "That is not a gap in this project —",
            "it is a property of networks.",
        ],
        narration=(
            'Now the third kind of failure. [[slnc 300]] This is the one '
            'the video is really about. [[slnc 600]] The request leaves '
            'the shop. [[slnc 300]] It reaches the gateway. [[slnc 300]] '
            'The card is charged, and the money really moves. [[slnc '
            '300]] And then the reply is lost on the way back. [[slnc '
            '700]] So here is the question the whole pattern turns on. '
            '[[slnc 300]] What does the caller see? [[slnc 600]] It sees '
            'a timeout. [[slnc 300]] Exactly the same timeout as in the '
            'first demo, when nothing had been charged at all. [[slnc '
            '600]] There is no flag to check, and nothing to read. [[slnc '
            '300]] No code can tell apart a request lost on the way out, '
            'from a reply lost on the way back. [[slnc 500]] And this is '
            'not a weakness of a teaching project. [[slnc 300]] The '
            'caller simply does not have that information. [[slnc 300]] '
            'It is how networks work.'
        ),
    ),
    dict(
        key="10-act-four",
        kind="console",
        title="Act Four — And The Plain Loop Charges Twice",
        body="""4. The same failure, with a plain three-times loop
      0ms ->    50ms  Payments        CHARGED-THEN-LOST chg-1
     50ms ->    50ms  NaiveCheckout   RETRYING immediately
     50ms ->   100ms  Payments        CHARGED   chg-2 £449.99

  checkout succeeded: chg-2 £449.99
  card charged 2 times, £899.98 in total

  the shopper paid twice for one espresso machine.""",
        narration=(
            'Fourth demo: give that failure to the plain three-times '
            'loop. [[slnc 500]] First attempt. [[slnc 300]] The card is '
            'charged, and the reply is lost. [[slnc 300]] The loop sees a '
            'failure, and goes round again, immediately. [[slnc 500]] '
            'Second attempt. [[slnc 300]] The gateway charges the card '
            'again. [[slnc 600]] Eight hundred and ninety-nine pounds '
            'ninety-eight. [[slnc 300]] For one espresso machine. [[slnc '
            '600]] And the gateway did nothing wrong. [[slnc 300]] The '
            'second attempt was a request it had never seen before. '
            '[[slnc 300]] And a new request means a new job. [[slnc 300]] '
            'So it did the job. [[slnc 500]] Every double charge in this '
            "project is the caller's doing."
        ),
    ),
    dict(
        key="11-nothing-went-wrong",
        kind="bullets",
        title="And Nothing Went Wrong. That Is The Problem.",
        body=[
            "Read what is missing from that output:",
            "",
            "    no exception escaped",
            "    nothing was logged as an error",
            "    the checkout returned a valid receipt",
            "    the order looks perfect",
            "",
            "NaiveCheckoutServiceTest:  5 tests, 5 passing.",
            "One of them asserts £899.98.",
            "",
            "A double charge does not arrive as a red test.",
            "It arrives as a phone call, two days later.",
        ],
        narration=(
            'Now think about what did not happen. [[slnc 600]] No error '
            'was raised. [[slnc 300]] Nothing was logged as a problem. '
            '[[slnc 300]] The checkout returned a perfectly valid '
            "receipt. [[slnc 300]] In the shop's own admin screens, the "
            'order would look completely fine. [[slnc 600]] This project '
            'has a test file for that naive checkout. [[slnc 300]] It has '
            'five tests. [[slnc 300]] All five pass. [[slnc 300]] And one '
            'of them deliberately checks that eight hundred and '
            "ninety-nine pounds ninety-eight left a customer's account. "
            '[[slnc 700]] So here is the sentence to take away. [[slnc '
            '300]] A double charge does not show up as a failing test, or '
            'an alert. [[slnc 300]] It shows up as a phone call from a '
            'customer, two days later. [[slnc 300]] And by then, it has '
            'happened to everybody else too.'
        ),
    ),
    dict(
        key="12-the-key",
        kind="code",
        title="So Stop Trying To Tell Them Apart",
        body="""public static PaymentRequest forOrder(String orderId, Money amount) {
    return new PaymentRequest(orderId, amount, "key-" + orderId);
}

// CheckoutService.pay -- the line that decides everything:
PaymentRequest request = PaymentRequest.forOrder(orderId, amount);
return retrier.call("payment for " + orderId,
                    () -> payments.charge(request));""",
        narration=(
            'So what does a careful caller do, when it cannot tell the '
            'two failures apart? [[slnc 400]] It stops trying to. [[slnc '
            '300]] Instead, it makes the difference not matter. [[slnc '
            '600]] It attaches a value to the request, called an '
            'idempotency key. [[slnc 300]] Idempotent means doing it '
            'twice has the same effect as doing it once. [[slnc 300]] The '
            'key is a promise to the other end. [[slnc 300]] If you have '
            'already seen this key, you have already done this job. '
            '[[slnc 300]] So do not do it again. [[slnc 300]] Just tell '
            'me what happened last time. [[slnc 600]] Now listen to what '
            'the key is made from, because this is where it goes wrong. '
            '[[slnc 300]] It is made from the order number, and nothing '
            'else. [[slnc 300]] Not the attempt number, not the time, and '
            'nothing random. [[slnc 300]] Otherwise the two attempts '
            'would not look like the same job, and the promise is '
            'worthless. [[slnc 600]] And here is the line that decides '
            'where the money goes. [[slnc 300]] The careful checkout '
            'builds the request once, before the first attempt, outside '
            'the retry. [[slnc 300]] The naive loop builds its request '
            'inside the loop. [[slnc 300]] So every attempt gets a fresh '
            'key. [[slnc 500]] That one line, and where it sits, is the '
            'difference between charging a shopper once, and charging '
            'them twice.'
        ),
    ),
    dict(
        key="13-act-three",
        kind="console",
        title="Act Three — The Same Failure, The Same Key",
        body="""3. The card was charged and the reply was lost
      0ms ->    50ms  Payments    CHARGED-THEN-LOST chg-1 taken
     50ms ->    50ms  Retrier     RETRYABLE attempt 1 failed
    153ms ->   153ms  Retrier     WAITED    103ms before attempt 2
    153ms ->   203ms  Payments    REPLAYED  key already charged

  checkout succeeded: chg-1 £449.99
  card charged 1 time, £449.99 in total""",
        narration=(
            'Third demo: the same failure, with the same key. [[slnc '
            '400]] The money is charged, and the reply is lost, just as '
            'before. [[slnc 300]] But this time, the caller is the '
            'careful one. [[slnc 600]] The first attempt charges the '
            'card, and the reply vanishes. [[slnc 300]] The retrier waits '
            'its hundred and three milliseconds, and tries again. [[slnc '
            '300]] Carrying the same key, because the request was built '
            'before any of this started. [[slnc 600]] The gateway looks '
            'up the key. [[slnc 300]] It finds it has already charged it. '
            '[[slnc 300]] So it returns the first charge, instead of '
            'making a second one. [[slnc 500]] The card was charged once. '
            '[[slnc 300]] And the checkout still succeeded. [[slnc 600]] '
            'Notice what the caller never had to do. [[slnc 300]] It '
            'never found out which kind of failure it had. [[slnc 300]] '
            'It could not have found out. [[slnc 300]] And it did not '
            'need to.'
        ),
    ),
    dict(
        key="14-who-keeps-the-record",
        kind="code",
        title="Somebody Has To Keep The Record",
        body="""// inside PaymentGateway.charge -- BEFORE any money moves
Receipt existing = chargesByKey.get(request.idempotencyKey());
if (existing != null) {
    log.note("REPLAYED", "key already charged");
    return existing;
}

// one map. that is the entire idempotency mechanism.""",
        narration=(
            'One more thing about the key. [[slnc 300]] People often miss '
            'this when they take the pattern back to work. [[slnc 600]] A '
            'key is only a promise. [[slnc 300]] And a promise is worth '
            'nothing, unless the other end remembers it. [[slnc 600]] '
            'Inside the gateway, there is one record: each key, and its '
            'receipt. [[slnc 300]] It is checked before any money moves. '
            '[[slnc 300]] That record is the whole mechanism. [[slnc '
            '300]] Everything the caller does with keys only works '
            'because the far end keeps that record. [[slnc 600]] So '
            'making an operation safe to repeat takes work at both ends. '
            '[[slnc 300]] Your retry loop cannot decide it for you. '
            '[[slnc 300]] And no library can hand it to you. [[slnc 500]] '
            'Remember, the retrier just runs a piece of work. [[slnc '
            '300]] It cannot tell a harmless database read from a '
            'payment.'
        ),
    ),
    dict(
        key="15-costs",
        kind="bullets",
        title="What It Costs, And When Not To",
        body=[
            "Time, and the shopper pays it: 203ms, not 50ms.",
            "Load, exactly when you can least afford it —",
            "three attempts each against a struggling service.",
            "",
            "A hard requirement on the thing you are calling:",
            "no key, no retry. A rule, not a preference.",
            "",
            "Don't retry a definite answer: a declined card,",
            "a validation error, a 404, a 401.",
            "",
            "And retrying a service that is properly down",
            "turns a slow system into a dead one.",
        ],
        narration=(
            'So what does retrying cost? [[slnc 300]] Because it is not '
            'free. [[slnc 600]] First, time, and the shopper pays it. '
            '[[slnc 300]] That recovered checkout took two hundred '
            'milliseconds, instead of fifty. [[slnc 300]] Sometimes a '
            'person would rather have the error quickly. [[slnc 500]] '
            'Second, load, exactly when you can least afford it. [[slnc '
            '300]] Three attempts per caller against a struggling service '
            'triples the traffic. [[slnc 300]] Backoff and jitter reduce '
            'that. [[slnc 300]] They do not remove it. [[slnc 500]] '
            'Third, and this is a rule, not a preference. [[slnc 300]] '
            'Only retry an operation that is safe to repeat. [[slnc 300]] '
            'No key, no retry. [[slnc 500]] And do not retry a definite '
            'answer. [[slnc 300]] A declined card, a validation error, or '
            'a page that does not exist. [[slnc 300]] Retrying those just '
            'asks the same question louder. [[slnc 600]] One more '
            'warning. [[slnc 300]] If the service is not just flaky, but '
            'completely down, retrying makes things worse. [[slnc 300]] '
            'Every caller waits three times as long, for something that '
            'will never answer. [[slnc 300]] That is not an argument '
            'against retrying. [[slnc 300]] It is an argument for knowing '
            'when to stop.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that moves",
            "one line into the lambda and turns the careful checkout",
            "into the one that charges a shopper twice.",
        ],
        narration=(
            "That's the Retry with Backoff pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A safe '
            'retry needs two things: the failure must be temporary, and '
            'doing the job twice must not do it twice. [[slnc 300]] '
            'Everybody thinks about the first one. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'In the careful checkout, move the line that builds the '
            'payment request inside the retry. [[slnc 300]] So it is '
            'built on every attempt, instead of once. [[slnc 300]] Then '
            'run the tests. [[slnc 300]] One test fails, and its name '
            'tells you what you broke. [[slnc 500]] Then ask yourself: in '
            'a code review on a Friday afternoon, would anyone have '
            'caught it? [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]

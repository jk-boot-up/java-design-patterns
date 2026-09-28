"""Scene definitions for the Circuit Breaker teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the fuse-box analogy is spoken in full before
any class name, and the code slides are described in words rather than read out
as syntax. The slides illustrate the narration; they never carry it.

Every number quoted in these scenes comes from the real output of
`./gradlew run`: one call to a dead service costs 3000ms, the threshold is
three consecutive failures, the reset wait is 5000ms, retry costs 9000ms for a
page identical to the one you would have had immediately, and act two serves
six pages by making three calls and refusing three.

Scene order is the argument, and it has two halves. The mechanism is shown
working -- scenes six to eleven -- before the word *fallback* is used for
anything harder than an empty list of suggestions. Only then do scenes twelve
to fourteen ask what the speed is actually for, and end on a fallback that
lies. Moving the checkout scenes earlier turns the video into a warning rather
than an explanation; do not do it.

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
        title="Circuit Breaker",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Circuit Breaker pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] When a service you depend on '
            'has clearly stopped working, you stop calling it for a '
            'while. [[slnc 300]] Then, after that while, you let exactly '
            'one call through, to find out whether it has come back. '
            '[[slnc 600]] Think of the fuse box in a house. [[slnc 300]] '
            'When the wiring has a fault, the fuse trips, and stays off. '
            '[[slnc 300]] Later, someone flips it back on, once, to see. '
            '[[slnc 600]] There is a second half that most explanations '
            'leave out. [[slnc 300]] A breaker does not make failures '
            'disappear. [[slnc 300]] It makes them fail fast. [[slnc '
            '300]] And you still have to decide what to tell the person '
            'waiting. [[slnc 700]] In our online store, one service has '
            'stopped answering this morning. [[slnc 500]] By the end, you '
            'will know why trying again is the wrong tool for an outage. '
            '[[slnc 300]] How a broken feature that nobody would miss can '
            'stop the shop selling anything. [[slnc 300]] And why one of '
            'the four callers in this project thanks a shopper for money '
            'that never moved.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A product page shows one espresso machine,",
            "and under it a row of suggestions from a",
            "separate Recommendations service.",
            "",
            "This morning, Recommendations has stopped",
            "answering. Not refusing — that would be easy.",
            "",
            "It accepts the connection, says nothing, and",
            "3000ms later the call gives up with a timeout.",
            "",
            "Every call. For as long as the outage lasts.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A shopper is looking at a '
            'product page for an espresso machine. [[slnc 300]] The page '
            'shows the machine, the price, and the description. [[slnc '
            '300]] And underneath, a row of suggestions: people who '
            'bought this also bought. [[slnc 500]] Those suggestions come '
            'from a separate service, called Recommendations. [[slnc '
            '600]] This morning, Recommendations has stopped answering. '
            '[[slnc 500]] It is not refusing connections. [[slnc 300]] '
            'That would be easy, because you would get an error straight '
            'away. [[slnc 300]] Instead, it accepts the connection, and '
            'says nothing. [[slnc 300]] Three seconds later, the call '
            'gives up with a timeout. [[slnc 500]] Every call does that, '
            'for as long as the outage lasts. [[slnc 500]] And remember '
            'one detail, because the whole video turns on it. [[slnc '
            '300]] Nobody would miss these suggestions. [[slnc 300]] They '
            'are the least important thing on the page.'
        ),
    ),
    dict(
        key="03-just-retry",
        kind="code",
        title="The Obvious Answer — Just Try Again",
        body="""for (int attempt = 1; attempt <= 3; attempt++) {
    try {
        return recommendations.suggestionsFor(sku);
    } catch (ServiceUnavailableException timeout) {
        // try again
    }
}
return List.of();   // gave up, serve the page anyway

// compiles, works, correct page, every test passes""",
        narration=(
            'Ask a room of developers what to do about a failed call, and '
            'someone will say: try it again. [[slnc 400]] That is '
            'reasonable. [[slnc 300]] For a dropped connection, trying '
            'again is exactly right. [[slnc 300]] That is the retry '
            'pattern. [[slnc 500]] So here it is, applied here. [[slnc '
            '300]] A loop makes up to three attempts. [[slnc 300]] If an '
            'attempt times out, it tries again. [[slnc 300]] If all three '
            'fail, it gives up, and serves the page with no suggestions. '
            '[[slnc 500]] To be fair to this code, there is no bug in it. '
            '[[slnc 300]] It always returns a correct page, and every '
            "test passes. [[slnc 500]] Let's run it against a service "
            'that has stopped answering, and watch the clock.'
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act One — Retry, Applied To An Outage",
        body="""$ ./gradlew run

1. Retry, applied to an outage
      0ms ->  3000ms  Recommendations  TIMEOUT   no answer in 3000ms
   3000ms ->  3000ms  ProductPage      RETRYING  attempt 1 timed out
   3000ms ->  6000ms  Recommendations  TIMEOUT   no answer in 3000ms
   6000ms ->  6000ms  ProductPage      RETRYING  attempt 2 timed out
   6000ms ->  9000ms  Recommendations  TIMEOUT   no answer in 3000ms
   9000ms ->  9000ms  ProductPage      RETRYING  attempt 3 timed out

  page: Barista Pro Espresso Machine, 0 suggestion(s)
  the shopper waited 9000ms for a page with nothing extra on it,
  and a service that is already down received 3 more calls.""",
        narration=(
            'Here is the timeline. [[slnc 400]] Zero to three seconds: '
            'timeout. [[slnc 300]] Three to six seconds: timeout. [[slnc '
            '300]] Six to nine seconds: timeout. [[slnc 500]] The shopper '
            'waited nine seconds. [[slnc 300]] And then got a page with '
            'no suggestions. [[slnc 300]] Exactly the page they could '
            'have had at zero seconds, if we had never called at all. '
            '[[slnc 500]] So those nine seconds bought nothing. [[slnc '
            '600]] There is a second cost, too. [[slnc 300]] A service '
            'that is already struggling just got three times as much '
            'traffic from us. [[slnc 300]] We are not helping it recover. '
            '[[slnc 300]] We are standing on it. [[slnc 500]] Retry is '
            'not a bad pattern. [[slnc 300]] It is the wrong pattern for '
            'an outage.'
        ),
    ),
    dict(
        key="05-three-costs",
        kind="bullets",
        title="Three Costs — And The Third Closes The Shop",
        body=[
            "1.  Nine seconds, for a page identical to the",
            "     one you'd have had at zero seconds.",
            "",
            "2.  Three times the traffic, aimed at a service",
            "     that is already struggling.",
            "",
            "3.  For all nine seconds, a request thread sits",
            "     idle. Threads are finite.",
            "",
            "A thousand shoppers browsing during the outage",
            "is a thousand threads held open — and when they",
            "run out, checkout stops working too.",
        ],
        narration=(
            'There are three costs here. [[slnc 300]] Most people find '
            'the first two, and stop. [[slnc 500]] One. [[slnc 200]] Nine '
            "seconds of a shopper's time, to reach the same page they "
            'could have had at once. [[slnc 400]] Two. [[slnc 200]] Three '
            'times the traffic, aimed at a service that is already '
            'struggling. [[slnc 500]] Three is the one that takes the '
            'shop down. [[slnc 300]] While the code waits for an answer '
            'that never comes, it holds a thread. [[slnc 300]] A thread '
            'is a worker that can serve one request at a time. [[slnc '
            '300]] That thread does nothing, and cannot serve anyone '
            'else. [[slnc 300]] And a web server only has a limited '
            'number of them, perhaps a couple of hundred. [[slnc 500]] '
            'Now imagine a thousand shoppers browsing during the outage. '
            '[[slnc 300]] That is a thousand threads, each held for nine '
            'seconds, waiting on a feature nobody would miss. [[slnc '
            '300]] When the threads run out, there are none left for '
            'anything. [[slnc 300]] Including checkout. [[slnc 500]] So '
            'the espresso machines stop selling, because the suggestions '
            'are broken.'
        ),
    ),
    dict(
        key="06-fuse-box",
        kind="quote",
        title="The Fuse Box",
        body=[
            "When something is badly wrong with the wiring,",
            "the fuse trips.",
            "",
            "And it STAYS tripped.",
            "",
            "It does not flick itself back on hopefully,",
            "every few seconds, to see how things are going.",
            "",
            "Later, somebody walks over and flips the",
            "switch back on — once — to see.",
            "",
            "That is the entire pattern.",
        ],
        narration=(
            'Forget software for a moment, and think about the fuse box '
            'in a house. [[slnc 400]] When something goes badly wrong '
            'with the wiring, the fuse trips. [[slnc 300]] The power to '
            'that circuit is cut. [[slnc 300]] And it stays off. [[slnc '
            '500]] A fuse does not keep switching itself back on every '
            'few seconds, hoping. [[slnc 300]] The fault is still there, '
            'and that is exactly what the fuse exists to prevent. [[slnc '
            '500]] Instead, later on, someone walks over and flips the '
            'switch back on. [[slnc 300]] Once. [[slnc 300]] To see. '
            '[[slnc 500]] If the lights come on, good. [[slnc 300]] If it '
            'trips again, it stays off, and they go and find the real '
            'problem. [[slnc 600]] That is the entire pattern. [[slnc '
            '300]] Stop calling. [[slnc 300]] Wait. [[slnc 300]] Then let '
            'one call through, to find out.'
        ),
    ),
    dict(
        key="07-vocabulary",
        kind="bullets",
        title="One Word That Reads Backwards",
        body=[
            "CLOSED     healthy. Current flows, so calls go",
            "                through. Failures in a row are counted.",
            "",
            "OPEN        tripped. Calls are refused without",
            "                being made at all. Costs nothing.",
            "",
            "HALF-OPEN   exactly one call is let through,",
            "                to see what happens.",
            "",
            "If CLOSED sounds wrong for the healthy state,",
            "you are thinking of a door.",
            "Think of a wire.",
        ],
        narration=(
            'A breaker has three states. [[slnc 300]] And one of the '
            "names sounds backwards, so let's deal with it now. [[slnc "
            '500]] The healthy state, where calls go through normally, is '
            'called closed. [[slnc 500]] That sounds wrong if you think '
            'of a door, because a closed door stops you. [[slnc 300]] But '
            'the name comes from electrical circuits. [[slnc 300]] A '
            'closed circuit is complete, and the current flows. [[slnc '
            '600]] So, closed means healthy. [[slnc 300]] Calls go '
            'through, and failures in a row are counted. [[slnc 500]] '
            'Open means tripped. [[slnc 300]] Calls are refused, without '
            'being made at all. [[slnc 500]] And half-open is the moment '
            'with a finger on the fuse switch. [[slnc 300]] Exactly one '
            'call is let through, to see what happens. [[slnc 500]] Think '
            'of a wire, not a door.'
        ),
    ),
    dict(
        key="08-the-breaker",
        kind="code",
        title="The Whole Decision, In One Method",
        body="""public <T> T call(Supplier<T> action) {
    if (state == BreakerState.OPEN) {
        if (clock.millis() - openedAt < resetAfterMillis) {
            throw new CircuitOpenException(serviceName);   // no call made
        }
        state = BreakerState.HALF_OPEN;   // let exactly one through
    }
    try {
        T answer = action.get();
        onSuccess();          // consecutiveFailures = 0
        return answer;
    } catch (RuntimeException failure) {
        onFailure(failure);   // 3 in a row -> trip
        throw failure;
    }
}""",
        narration=(
            'In code, the whole decision fits in one method, with three '
            'questions. [[slnc 500]] First question. [[slnc 300]] Is the '
            'breaker open, and is the waiting time over? [[slnc 300]] If '
            'it is open, and the wait is not over, it refuses at once, '
            'and makes no call. [[slnc 300]] If the wait is over, it '
            'moves to half-open, and lets this one call through. [[slnc '
            '500]] Second question. [[slnc 300]] Did the call work? '
            '[[slnc 300]] If so, the failure count goes back to zero, and '
            'the answer is returned. [[slnc 500]] Back to zero, not down '
            'by one. [[slnc 300]] Because it counts failures in a row. '
            '[[slnc 300]] A service that answers three times and fails '
            'once is not down. [[slnc 300]] It is having a bad moment, '
            "and that is retry's job. [[slnc 500]] Third question. [[slnc "
            '300]] If the call failed, has it now failed enough times in '
            'a row? [[slnc 300]] In this project, the limit is three. '
            '[[slnc 300]] At three, the breaker trips, notes the time, '
            'and stops calling. [[slnc 500]] That is the whole mechanism.'
        ),
    ),
    dict(
        key="09-act-two",
        kind="console",
        title="Act Two — Six Pages, With A Breaker",
        body="""2. Six product pages, with a breaker
      0ms ->  3000ms  Recommendations  TIMEOUT   no answer in 3000ms
   3000ms ->  3000ms  Recommendations  FAILED    failure 1 of 3
   3000ms ->  6000ms  Recommendations  TIMEOUT   no answer in 3000ms
   6000ms ->  6000ms  Recommendations  FAILED    failure 2 of 3
   6000ms ->  9000ms  Recommendations  TIMEOUT   no answer in 3000ms
   9000ms ->  9000ms  Recommendations  OPENED    not calling for 5000ms
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made

  6 pages served, every one of them buyable, none with suggestions
  3 calls reached Recommendations, 3 were refused without a call
  total time 9000ms""",
        narration=(
            'Now the same outage, with six shoppers, and a breaker. '
            '[[slnc 500]] The first page: zero to three seconds, timeout. '
            '[[slnc 300]] Failure one of three. [[slnc 300]] The second '
            'page: three to six seconds, timeout. [[slnc 300]] Failure '
            'two. [[slnc 300]] The third page: six to nine seconds, '
            'timeout. [[slnc 300]] That is three in a row, so the breaker '
            'trips. [[slnc 600]] The fourth shopper arrives at nine '
            'seconds, and is refused instantly. [[slnc 300]] No call is '
            'made. [[slnc 300]] The fifth, also instantly. [[slnc 300]] '
            'The sixth, also instantly. [[slnc 500]] The clock has '
            'stopped moving. [[slnc 300]] Once the breaker is open, '
            'serving a page costs nothing, because nothing leaves the '
            'building. [[slnc 500]] Six pages, three real calls, and nine '
            'seconds in total. [[slnc 300]] The same nine seconds retry '
            'spent on a single shopper. [[slnc 300]] And every one of '
            'those six pages can still sell an espresso machine. [[slnc '
            '600]] To be honest about the trade: the first three shoppers '
            'still waited three seconds each. [[slnc 300]] A breaker '
            'never protects the people who discover an outage. [[slnc '
            '300]] It protects everybody after them.'
        ),
    ),
    dict(
        key="10-roles",
        kind="diagram",
        title="The Pieces, And What Each One Decides",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are only a few. "
            '[[slnc 500]] At the centre is one class: the circuit '
            'breaker. [[slnc 300]] It remembers three things. [[slnc '
            '300]] Its state, how many failures in a row it has seen, and '
            'the moment it tripped. [[slnc 500]] It is given a piece of '
            'work, and runs it. [[slnc 300]] It knows nothing about '
            'product pages, money, or shoppers. [[slnc 300]] That is why '
            'one breaker class can serve every caller. [[slnc 600]] It '
            'also has a clock, and that clock is the whole half-open '
            'mechanism. [[slnc 300]] There is no background timer. [[slnc '
            '300]] The breaker simply compares the time now with the time '
            'it tripped, whenever the next call arrives. [[slnc 300]] So '
            'recovery is found by ordinary traffic. [[slnc 600]] Then '
            'there are four callers, and they are the interesting part. '
            '[[slnc 300]] The product page, which treats suggestions as '
            'optional. [[slnc 300]] Checkout, which treats payment as '
            'essential. [[slnc 300]] A third caller that invents a '
            'receipt. [[slnc 300]] And a fourth with no breaker at all, '
            'which only retries. [[slnc 500]] All four use the same '
            'breaker class. [[slnc 300]] What changes between them is '
            'what they do when the call fails. [[slnc 300]] That is the '
            'only decision the pattern leaves to you.'
        ),
    ),
    dict(
        key="11-act-three",
        kind="console",
        title="Act Three — It Lets Itself Back In",
        body="""3. Recommendations comes back, and one probe finds out
   9000ms ->  9000ms  Recommendations  OPENED    not calling for 5000ms
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made

  14000ms -> 14000ms  Recommendations  HALF-OPEN letting one call through
  14000ms -> 14020ms  Recommendations  OK        [SKU-2001, SKU-2002]
  14020ms -> 14020ms  Recommendations  CLOSED    the probe worked, calls resume

  page: Barista Pro Espresso Machine, 2 suggestion(s)
  state: CLOSED -- nobody deployed anything to make that happen.""",
        narration=(
            'Meanwhile, somebody has fixed Recommendations. [[slnc 500]] '
            'At nine seconds, the breaker is open, and a call is refused '
            'instantly. [[slnc 300]] At fourteen seconds, five seconds '
            'after it tripped, the next shopper gets a different answer. '
            '[[slnc 300]] Half-open: one call is let through. [[slnc '
            '500]] That call takes twenty milliseconds, and returns two '
            'suggestions. [[slnc 300]] So the breaker closes, and normal '
            'service resumes. [[slnc 600]] Nobody was called out. [[slnc '
            '300]] Nobody logged in, and nobody deployed anything. [[slnc '
            '300]] The shop noticed by itself that the outage was over. '
            '[[slnc 500]] And finding out was cheap: one call. [[slnc '
            '300]] If the service had still been down, one shopper would '
            'have waited three seconds. [[slnc 300]] The breaker would '
            'have opened again for another five. [[slnc 300]] And '
            'everyone else would still be served instantly. [[slnc 500]] '
            'That single call is the whole point of half-open. [[slnc '
            '300]] Let every waiting call through instead, and you just '
            'rush the broken service all over again.'
        ),
    ),
    dict(
        key="12-fail-fast",
        kind="quote",
        title="Now The Half That Gets Left Out",
        body=[
            "A breaker does not make failures disappear.",
            "",
            "It makes them fail FAST.",
            "",
            "And what that speed buys you depends entirely",
            "on what you were calling.",
            "",
            "Suggestions are optional, so there is something",
            "true to say instead: we have none to show.",
            "",
            "Payment is essential. There is no substitute",
            "for taking the money.",
        ],
        narration=(
            'Everything so far is the mechanism, and that is the easy '
            'half. [[slnc 500]] Here is the key sentence. [[slnc 300]] A '
            'breaker does not make failures disappear. [[slnc 300]] It '
            'makes them fail fast. [[slnc 500]] The call still failed. '
            '[[slnc 300]] The shopper still does not get what they asked '
            'for. [[slnc 300]] They just find out at once, instead of '
            'after three seconds. [[slnc 500]] So what is that speed '
            'worth? [[slnc 300]] It depends entirely on what you were '
            'calling. [[slnc 600]] On the product page, it is worth a '
            'lot. [[slnc 300]] Suggestions are optional, so there is '
            'something true to say instead. [[slnc 300]] We have no '
            'suggestions to show right now. [[slnc 300]] The page goes '
            'out without them, and the shopper buys the machine anyway. '
            '[[slnc 600]] Now ask the same question about checkout, where '
            'the failing service takes the money. [[slnc 300]] There is '
            'no substitute for taking the money.'
        ),
    ),
    dict(
        key="13-act-four",
        kind="console",
        title="Act Four — Checkout, Where There Is No Fallback",
        body="""4. Checkout: the same breaker, no fallback
      0ms ->  3000ms  Payments   TIMEOUT   no answer in 3000ms
   3000ms ->  3000ms  Checkout   HONEST-NO told the shopper after a timeout
   ...
   9000ms ->  9000ms  Payments   OPENED    not calling for 5000ms
   9000ms ->  9000ms  Payments   REFUSED   circuit open, no call made
   9000ms ->  9000ms  Checkout   HONEST-NO told at once, card untouched

  5 shoppers were told honestly that we cannot take payment
  0 cards were charged

// "We cannot take payment at the moment. Your basket is saved.\"""",
        narration=(
            'Here is checkout, using the same breaker class, with the '
            'same limit and the same wait. [[slnc 500]] When the breaker '
            'refuses, checkout does not invent anything. [[slnc 300]] It '
            'tells the shopper the truth. [[slnc 300]] We cannot take '
            'payment at the moment, and your basket is saved. [[slnc '
            '500]] Five shoppers were told that. [[slnc 300]] No cards '
            'were charged. [[slnc 600]] So, with no fallback, is the '
            'breaker still worth having? [[slnc 300]] Yes, for two '
            'reasons. [[slnc 500]] First, speed. [[slnc 300]] The first '
            'shopper got that message after three seconds of waiting. '
            '[[slnc 300]] The fourth and fifth got the same message '
            'instantly. [[slnc 300]] Being told straight away that your '
            'basket is safe is a better experience. [[slnc 500]] Second, '
            'threads. [[slnc 300]] Without the breaker, every shopper '
            'holds a thread for three seconds. [[slnc 300]] With a '
            'thousand shoppers, you lose the whole shop, not just '
            'checkout. [[slnc 500]] A fast, honest no is a real feature.'
        ),
    ),
    dict(
        key="14-act-five",
        kind="console",
        title="Act Five — The Fallback That Lies",
        body="""5. The same outage, with a fallback that lies
      0ms ->  3000ms  Payments   TIMEOUT   no answer in 3000ms
   3000ms ->  3000ms  Checkout   PRETENDED a receipt for money that never moved

  the shopper was shown receipt chg-assumed-ok and thanked
  cards actually charged: 0

  nothing threw, no alert fired, and the warehouse will ship an
  espresso machine nobody paid for.

// catch (RuntimeException anything) { return "chg-assumed-ok"; }""",
        narration=(
            'And now the last caller. [[slnc 300]] Think about this one '
            'carefully. [[slnc 500]] It is set up exactly like the honest '
            'checkout. [[slnc 300]] Same service, same breaker, same '
            'limit. [[slnc 300]] The only difference is what it does on '
            'failure. [[slnc 300]] When payments cannot be reached, it '
            'returns a made-up receipt. [[slnc 600]] So the shopper is '
            'thanked, and shown a receipt. [[slnc 300]] No error is '
            'raised. [[slnc 300]] No alert fires. [[slnc 300]] Every '
            'dashboard stays green. [[slnc 300]] And the warehouse will '
            'ship an espresso machine that nobody paid for. [[slnc 300]] '
            'Cards actually charged: zero. [[slnc 600]] The lesson is not '
            "that fallbacks are bad. [[slnc 300]] The product page's "
            'fallback is excellent. [[slnc 300]] It is why the shop kept '
            'selling this morning. [[slnc 500]] The difference is one '
            'word: true. [[slnc 300]] An empty list of suggestions is '
            'true. [[slnc 300]] The shop really has none to show. [[slnc '
            '300]] A receipt for money that never moved is not true. '
            '[[slnc 500]] And a fallback that hides a real failure is '
            'worse than the error it replaced. [[slnc 300]] The error '
            'would be noticed in seconds. [[slnc 300]] This will be '
            'noticed at the end of the month.'
        ),
    ),
    dict(
        key="15-costs",
        kind="bullets",
        title="What It Costs, And When Not To",
        body=[
            "It does not protect the people who discover the",
            "outage — only everybody after them.",
            "",
            "Tuned badly it hurts: threshold 1 trips a healthy",
            "service; a 60s wait keeps you degraded after",
            "the dependency has already recovered.",
            "",
            "Don't bother for a call that is already fast and",
            "local, or one that runs once at startup.",
            "",
            "And a library can give you the state machine.",
            "It cannot tell you whether your fallback is true.",
        ],
        narration=(
            'Now the costs, because every pattern has them. [[slnc 500]] '
            'First, a breaker does not protect the people who discover '
            'the outage. [[slnc 300]] Somebody always pays full price. '
            '[[slnc 500]] Second, it can be tuned badly, in both '
            'directions. [[slnc 300]] With a limit of one, a single '
            'hiccup cuts off a perfectly healthy service. [[slnc 300]] '
            'With a one-minute wait, the shop stays degraded for a whole '
            'minute after the service has recovered. [[slnc 500]] Third, '
            'it is harder to reason about. [[slnc 300]] The same call now '
            'behaves differently, depending on what happened five seconds '
            'ago. [[slnc 300]] For a call that is fast and local, or runs '
            'once at startup, that is not worth it. [[slnc 600]] Finally, '
            'in real systems, you would probably use a library rather '
            'than write this yourself. [[slnc 300]] That is fine. [[slnc '
            '300]] A library gives you the states, the limit, and the '
            'timer. [[slnc 300]] But it cannot tell you whether what you '
            'say instead is true. [[slnc 300]] That part is yours.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that lets",
            "every waiting call through instead of one, and shows you",
            "why half-open lets exactly one.",
        ],
        narration=(
            "That's the Circuit Breaker pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'breaker makes failures fast, not invisible, and a fallback '
            'is only acceptable if what it tells the person waiting is '
            'true. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 300]] There '
            'is no network, and no resilience library. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Remove the half-open '
            'step, so every waiting call is let through once the wait is '
            'over. [[slnc 300]] Then run the demo with the service still '
            'down. [[slnc 300]] Every caller waits three seconds at the '
            'same time, against a service that is already struggling. '
            '[[slnc 300]] That is the rush the pattern exists to prevent. '
            '[[slnc 500]] And one question to think about. [[slnc 300]] '
            'Somewhere in your own system, a catch block returns '
            'something reassuring when a service fails. [[slnc 300]] Is '
            'what it says true? [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]

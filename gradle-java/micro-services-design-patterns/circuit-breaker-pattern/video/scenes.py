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
            "Hello, and welcome. This video explains the Circuit Breaker "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the simple definition. When "
            "a service you depend on has clearly stopped working, you stop "
            "calling it for a while — and then, after that while, you let "
            "exactly one call through to find out whether it has come back. "
            "[[slnc 350]] That is the whole mechanism, and it takes about a "
            "hundred lines of plain Java. [[slnc 250]] But there is a second "
            "half that most explanations leave out, and it is the harder half: "
            "a breaker does not make failures disappear, it makes them fail "
            "fast, and you still have to decide what to say to the person "
            "waiting. [[slnc 300]] The rest of the video does both, by building "
            "a real working Java project: an online shop where one service has "
            "stopped answering this morning. [[slnc 300]] By the end you'll know "
            "why trying again is the wrong tool for an outage; why an outage in "
            "a feature nobody would miss can stop the shop selling anything at "
            "all; and why one of the four callers in this project thanks a "
            "shopper for money that never moved, while nothing throws, no alert "
            "fires, and every dashboard stays green."
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
            "Here is the situation, and it is worth picturing before any code. "
            "[[slnc 300]] A shopper is looking at a product page for an espresso "
            "machine. The page shows the machine, the price, the description — "
            "and underneath all of that, a row of suggestions. People who "
            "bought this also bought. Those suggestions come from a completely "
            "separate service, called Recommendations, running somewhere else. "
            "[[slnc 350]] This morning, Recommendations has stopped answering. "
            "[[slnc 250]] Now, notice what I did not say. I did not say it is "
            "refusing connections, because that would actually be easy — you'd "
            "get an error back straight away and you'd know. [[slnc 300]] What "
            "it is doing is worse and much more common. It accepts the "
            "connection, it says nothing at all, and three seconds later your "
            "call gives up and throws a timeout. [[slnc 300]] Every single call "
            "does that, for as long as the outage lasts. Three seconds, "
            "nothing, three seconds, nothing. [[slnc 250]] And hold on to one "
            "detail, because the whole video turns on it: nobody would miss "
            "these suggestions. They are the least important thing on the page."
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
            "Ask a room of developers what to do about a call that failed, and "
            "somebody will say: try it again. [[slnc 300]] And they are reaching "
            "for something reasonable. The previous pattern in this series is "
            "retry with backoff, and for a dropped connection or a router that "
            "reset, trying again is exactly right. [[slnc 350]] So here is that "
            "answer, applied here. A loop that makes up to three attempts. If "
            "an attempt times out, it swallows the timeout and goes round "
            "again. If all three fail, it gives up and serves the page with no "
            "suggestions on it. [[slnc 300]] I want to be fair to this code. "
            "There is no bug in it. It compiles, it is easy to read, it always "
            "returns a correct page, and every test written against it passes. "
            "[[slnc 300]] Let's run it against a service that has stopped "
            "answering, and watch the clock."
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
            "Read the left-hand column, because that is the whole story. "
            "[[slnc 300]] Zero to three thousand: timeout. Three thousand to six "
            "thousand: timeout. Six thousand to nine thousand: timeout. "
            "[[slnc 300]] The shopper waited nine seconds. And then they got a "
            "page with no suggestions on it — which is precisely, identically, "
            "the page they would have had at zero seconds if we had never "
            "called at all. [[slnc 350]] So every one of those nine seconds "
            "bought absolutely nothing. [[slnc 250]] And there is a second cost, "
            "pointing the other way. A service that is already on its knees "
            "just received three times as much traffic from us as it would "
            "have done if we had asked once. We are not helping it recover. We "
            "are standing on it. [[slnc 300]] Retry is not a bad pattern. It is "
            "the wrong pattern for this, and the difference is a single "
            "question that I'll come to in a moment."
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
            "There are three costs here, and almost everybody finds the first "
            "two and stops. [[slnc 300]] One: nine seconds of a shopper's life, "
            "spent to arrive at the same page they'd have had immediately. "
            "[[slnc 250]] Two: triple the traffic, aimed at something already "
            "struggling. [[slnc 300]] The third one is the one that actually "
            "takes the shop down, and it is worth saying slowly. [[slnc 250]] "
            "While your code is sitting there waiting for an answer that is "
            "never coming, it is holding a thread. That thread is doing "
            "nothing. It cannot serve anybody else. And threads are finite — a "
            "web server has a pool of them, maybe a couple of hundred. "
            "[[slnc 350]] So now imagine a thousand shoppers browsing product "
            "pages during this outage. That is a thousand threads, each held "
            "open for nine seconds, waiting on a feature that nobody would "
            "have missed. [[slnc 300]] When the pool runs out, there are no "
            "threads left for anything — including checkout. [[slnc 350]] Let me "
            "say that as plainly as I can. The espresso machines stop selling, "
            "because the suggestions are broken."
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
            "Forget software for thirty seconds and think about the fuse box in "
            "a house. [[slnc 300]] When something goes badly wrong with the "
            "wiring, the fuse trips. The power to that circuit is cut. "
            "[[slnc 250]] And here is the important bit: it stays tripped. "
            "[[slnc 300]] A fuse does not flick itself back on hopefully every "
            "few seconds to see how things are going. If it did, it would be "
            "useless — the fault is still there, and all that hopeful flicking "
            "is exactly the thing the fuse exists to prevent. [[slnc 350]] What "
            "actually happens is that later on, somebody walks over to the box "
            "and flips the switch back on. Once. To see. [[slnc 300]] If the "
            "lights come on, good, we're back. If it trips again immediately, "
            "fine — it stays off, and they go and find the actual problem. "
            "[[slnc 350]] That is the entire pattern. Stop calling. Wait. Let "
            "one call through to find out. And I'd rather you remembered the "
            "fuse box than any of the class names coming up."
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
            "There are three states, and one piece of vocabulary that catches "
            "absolutely everybody, so let's deal with it now. [[slnc 300]] The "
            "healthy state — the everything-is-fine state, where calls go "
            "through normally — is called closed. [[slnc 300]] I know. "
            "[[slnc 250]] If that sounds backwards, it is because you are "
            "thinking of a door. A closed door stops you. But this name comes "
            "from electrical circuits, and a closed circuit is one where the "
            "current flows. It is complete. It works. [[slnc 350]] So: closed "
            "means healthy, calls go through, and failures in a row are being "
            "counted. Open means tripped — calls are refused without being "
            "made at all. [[slnc 300]] And half-open is that moment at the fuse "
            "box with a finger on the switch: exactly one call is allowed "
            "through, to see what happens. [[slnc 350]] Think of a wire, not a "
            "door, and the rest of this video will make sense."
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
            "In code the whole decision fits in one method, and there are only "
            "three questions in it. [[slnc 300]] First question: am I currently "
            "tripped, and if so, is the waiting period over? If I am tripped "
            "and the wait is not over, I throw immediately without making any "
            "call at all. That is the important line — no call is made. If the "
            "wait is over, I move to half-open and let this one through. "
            "[[slnc 350]] Second question: did the call work? If it did, I reset "
            "the count of failures back to zero and hand the answer back. "
            "[[slnc 300]] Now, notice I said reset, not decrement, and that word "
            "matters. The count is of failures in a row — consecutive failures. "
            "A service that answers you three times and fails once is not down. "
            "It is having a bad moment, and a bad moment is retry's job, not "
            "this one's. [[slnc 350]] Third question: if the call failed, have I "
            "now failed enough times in a row? In this project the threshold is "
            "three. At three, it trips, notes the time, and stops calling. "
            "[[slnc 300]] That's it. That is the mechanism, end to end."
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
            "Same outage, six shoppers, now with a breaker. And once again the "
            "left-hand column is the argument, so let me read it to you. "
            "[[slnc 300]] The first page: zero to three thousand, timeout, "
            "failure one of three. The second: three thousand to six thousand, "
            "timeout, failure two. The third: six thousand to nine thousand, "
            "timeout — and that is three in a row, so the breaker trips. "
            "[[slnc 350]] Now the fourth shopper arrives. Nine thousand to nine "
            "thousand. Refused, no call made. [[slnc 250]] Fifth shopper: nine "
            "thousand to nine thousand. Sixth: nine thousand to nine thousand. "
            "[[slnc 350]] The clock stopped moving. [[slnc 300]] That is what I "
            "want you to hear. Once the breaker is open, serving a page costs "
            "nothing at all, because nothing leaves the building. Six pages "
            "were served, three calls were actually made, three were refused, "
            "and the grand total for all six is nine seconds — the same nine "
            "seconds that retry spent on one single shopper. [[slnc 350]] And "
            "every one of those six pages is a page somebody can buy an "
            "espresso machine from. [[slnc 300]] Now let me be honest about the "
            "trade, because this part gets skipped. The first three shoppers "
            "paid three seconds each. A breaker never protects the people who "
            "discover an outage. It protects everybody after them. What it "
            "prevents is the outage being rediscovered, at full price, by every "
            "shopper for as long as it lasts."
        ),
    ),
    dict(
        key="10-roles",
        kind="diagram",
        title="The Pieces, And What Each One Decides",
        body=None,
        narration=(
            "Let me put the pieces in order, in words, because there are only a "
            "few of them. [[slnc 300]] At the centre there is one class, called "
            "CircuitBreaker. It holds three things: which state it is in, how "
            "many failures in a row it has seen, and the moment it tripped. "
            "[[slnc 300]] And here is the thing worth noticing about it. It takes "
            "a piece of work to run and it runs it. It has never heard of "
            "product pages. It has never heard of money, or shoppers, or "
            "espresso machines. That is exactly why one copy of this class can "
            "serve every caller in the project. [[slnc 350]] Underneath it sits "
            "the state — closed, open, or half-open — and a clock. And the "
            "clock is the half-open mechanism, entirely. There is no scheduler "
            "here. There is no background thread waking up to retry. The "
            "breaker simply compares the current time against the moment it "
            "tripped, on whatever call happens to arrive next. Recovery is "
            "discovered by ordinary traffic. [[slnc 350]] On the other side there "
            "are four callers, and they are the interesting part. The product "
            "page, which treats suggestions as optional. Checkout, which treats "
            "payment as essential. A third one that invents a receipt — we'll "
            "come to that one. And a fourth that has no breaker at all and just "
            "retries, which is act one, kept in the project on purpose so the "
            "comparison is something you can run rather than something I "
            "assert. [[slnc 350]] All four share one breaker class. Nothing about "
            "the breaker changes between them. What changes is the catch block "
            "— and that is the only place the pattern leaves you a decision."
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
            "Meanwhile, somewhere else, somebody has fixed Recommendations. "
            "[[slnc 300]] At nine seconds the breaker is open and a call is "
            "refused instantly. Then the clock reaches fourteen thousand, which "
            "is five seconds after it tripped, and the next shopper to arrive "
            "gets a different answer. Half-open: letting one call through. "
            "[[slnc 300]] That call takes twenty milliseconds and comes back with "
            "two suggestions. So the breaker closes, and normal service "
            "resumes. [[slnc 350]] Read the last line again, because it is the "
            "nicest property of this pattern. Nobody was paged. Nobody logged "
            "into anything. Nobody deployed anything. The shop noticed, all by "
            "itself, that the outage was over. [[slnc 350]] And notice how cheap "
            "the finding-out was. One call. If Recommendations had still been "
            "down, that one shopper would have waited three seconds, the "
            "breaker would have reopened for another full five, and everybody "
            "else would have carried on being served instantly. [[slnc 300]] The "
            "single call is the whole point of half-open. If you let all the "
            "waiting calls through instead, you have simply recreated the "
            "stampede on a timer."
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
            "Everything up to here is the mechanism, and the mechanism is the "
            "easy half. [[slnc 350]] Here is the sentence the rest of this video "
            "depends on. A breaker does not make failures disappear. It makes "
            "them fail fast. [[slnc 300]] The call still failed. The shopper "
            "still isn't getting what they asked for. All that changed is that "
            "they found out in no time at all instead of in three seconds. "
            "[[slnc 350]] So what is that speed actually worth? And the honest "
            "answer is: it depends entirely on what you were calling. "
            "[[slnc 300]] On the product page it bought us something lovely. "
            "Suggestions are optional, so there is something true we can say "
            "instead — we have no suggestions to show you right now — and the "
            "page goes out without them and the shopper buys the espresso "
            "machine anyway. [[slnc 350]] Now ask the same question about "
            "checkout, where the thing that is failing is taking the money. "
            "[[slnc 300]] There is no substitute for taking the money. There is "
            "nothing a shop can serve you instead."
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
            "So here is checkout, wired to the same breaker class, with the "
            "same threshold and the same wait. And when the breaker refuses, it "
            "does not invent anything. It tells the shopper the truth: we "
            "cannot take payment at the moment, your basket is saved. "
            "[[slnc 350]] Five shoppers were told that. Zero cards were charged. "
            "[[slnc 300]] Which raises a fair question — if there is no fallback "
            "here, is the breaker worth having at all? [[slnc 350]] Yes, and for "
            "two reasons. [[slnc 250]] The first is in the timestamps. The first "
            "shopper got that message after three seconds of spinner. The "
            "fourth and fifth got exactly the same message instantly. Same "
            "words, same outcome, and telling somebody their basket is safe "
            "straight away instead of after three seconds of watching a "
            "spinner is a genuinely better product. [[slnc 350]] The second "
            "reason is the one from earlier. Without the breaker, every one of "
            "those five shoppers holds a thread open for three seconds to "
            "discover the same outage. Make it a thousand shoppers and you have "
            "lost the whole shop, not just checkout. [[slnc 300]] A fast, honest "
            "no is a real feature."
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
            "And now the last one, which I'd like you to sit with for a moment. "
            "[[slnc 350]] This class is wired identically to the honest one. Same "
            "dependency, same breaker, same threshold, same shape. The only "
            "difference is one catch block. When payments cannot be reached, "
            "instead of throwing, it returns a made-up receipt. [[slnc 350]] Look "
            "at what happens. The shopper is thanked. They are shown a receipt. "
            "Nothing throws an exception. No alert fires. Every dashboard in "
            "the building is green. And the warehouse is going to ship an "
            "espresso machine that nobody paid for. [[slnc 350]] Cards actually "
            "charged: zero. [[slnc 300]] Now, the lesson here is not that "
            "fallbacks are bad — the product page's fallback is excellent, and "
            "it is the reason the shop kept selling this morning. [[slnc 300]] "
            "The rule that tells the two apart is one word, and it is this. An "
            "empty list of suggestions is true. The shop really does have no "
            "suggestions to show. [[slnc 350]] A receipt for money that never "
            "moved is not true. [[slnc 300]] And a fallback that hides a real "
            "failure is worse than the error it replaced — because the error "
            "would have been noticed in seconds, and this will be noticed at "
            "the end of the month."
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
            "Before I finish, the costs — because every pattern has them and "
            "this one is usually sold without any. [[slnc 300]] First, and I said "
            "it earlier but it is worth repeating: a breaker does not protect "
            "the people who find the outage. Somebody always pays full price. "
            "[[slnc 300]] Second, it can be tuned badly in both directions. Set "
            "the threshold to one and a single wobble takes a perfectly healthy "
            "service out of use. Set the reset wait to a minute and your shop "
            "stays degraded for a full minute after the dependency came back. "
            "[[slnc 350]] Third, it is not free to reason about. There is now a "
            "piece of state that changes what your code does, and the same call "
            "behaves differently depending on what happened five seconds ago. "
            "For a call that is fast and local, or one that runs once at "
            "startup, that is not a trade worth making. [[slnc 350]] And finally, "
            "the honest one. In production you would probably reach for a "
            "library rather than write this yourself, and that is fine. But a "
            "library gives you the state machine, the threshold and the timer. "
            "[[slnc 300]] It cannot tell you whether the thing you say instead is "
            "true. That part is yours."
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
            "That's the circuit breaker. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository, and everything runs offline with nothing installed "
            "but a Java development kit — there is no network in this project "
            "at all, and no resilience library either. [[slnc 300]] If you try "
            "one exercise, try this one. Find the line that moves the breaker "
            "into half-open, delete it, and just let every waiting call through "
            "once the wait is over. Then run the demo again with the service "
            "still down. [[slnc 300]] Every caller pays three seconds, "
            "simultaneously, against something already on its knees — and you "
            "will have built the stampede that the pattern exists to prevent. "
            "[[slnc 350]] And then sit with the harder question, the one no "
            "exercise can answer for you. Somewhere in the system you work on "
            "there is a catch block that returns something reassuring when a "
            "dependency fails. [[slnc 300]] Is what it says true? [[slnc 350]] "
            "Because that is the real lesson here. The state machine is the "
            "easy half. A breaker makes failures fast, not invisible, and a "
            "fallback is only legitimate if what it tells the person waiting is "
            "actually true. [[slnc 300]] If this helped, a like genuinely does "
            "help other people find it, and subscribe if you would like the "
            "rest of the series. [[slnc 250]] Thanks for watching, and I'll see "
            "you in the next one."
        ),
    ),
]

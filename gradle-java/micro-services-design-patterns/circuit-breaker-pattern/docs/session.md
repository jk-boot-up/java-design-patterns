# Session Guide — Circuit Breaker

A one-hour session. It has two distinct halves, and the second is the one worth
protecting: the mechanism takes twenty minutes and is not difficult, while the
question of *what to do when the breaker refuses* is a genuine design argument that
most treatments of this pattern skip entirely.

**Audience:** developers who know Java. No distributed-systems experience assumed.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. Say what closed, open and half-open mean, out loud, without hesitating over which
   one is the healthy state.
2. State the question that separates retry from a breaker, in one sentence.
3. Explain why a refusal costs nothing, by pointing at a clock rather than at code.
4. Describe how the breaker recovers without anybody deploying anything, and say why
   the probe is one call rather than all of them.
5. Decide whether a given dependency has a legitimate fallback, and justify the answer
   with the word *true*.
6. Explain why an outage in an optional feature can take down checkout.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and the one piece of backwards vocabulary |
| 0:05–0:14 | The problem: retry, applied to an outage |
| 0:14–0:22 | The pattern, from a fuse box |
| 0:22–0:32 | Code walkthrough, and act two's timestamps |
| 0:32–0:44 | The half that gets left out: choosing a fallback |
| 0:44–0:56 | Exercises |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And The Vocabulary

```bash
cd micro-services-design-patterns/circuit-breaker-pattern
./gradlew test
```

26 tests, green, in about a second.

Then get the vocabulary out of the way before it can confuse anybody, because it will:

> One piece of jargon, and it reads backwards. **Closed is the healthy state.** A
> closed circuit is one where current flows, so calls go through. An open circuit is a
> broken one. If that feels the wrong way round, you are thinking of a door. Think of
> a wire.

Say it, write it on the board, and leave it there for the hour.

Then the honest warning:

> There is no network in this project and no Resilience4j. Services are objects you
> can tell to be down. The clock only moves when we move it, so a five-second reset
> wait costs no real time. You will learn the shape of the pattern and the decision
> it forces on you. You will not learn how to configure a particular library.

## 0:05–0:14 — The Problem

Set the scene in words before any code:

> The product page shows an espresso machine, and under it a row of suggestions from a
> separate Recommendations service. This morning Recommendations has stopped
> answering. Not refusing — that would be easy. It accepts the connection, says
> nothing, and three seconds later the call times out. Every call.

Ask the room what to do. Somebody will say "retry". They are reaching for the previous
pattern in the category, which is exactly the intended mistake.

Run act one:

```bash
./gradlew run
```

```
      0ms ->  3000ms  Recommendations  TIMEOUT   no answer in 3000ms
   3000ms ->  6000ms  Recommendations  TIMEOUT   no answer in 3000ms
   6000ms ->  9000ms  Recommendations  TIMEOUT   no answer in 3000ms
  the shopper waited 9000ms for a page with nothing extra on it,
  and a service that is already down received 3 more calls.
```

Draw out all three costs, and ask the room for them rather than listing them:

- nine seconds for a page identical to the one they'd have had at zero seconds
- three times the traffic aimed at a service on its knees
- **and the one they will not say** — for those nine seconds a request thread is idle.
  A thousand shoppers browsing during the outage is a thousand threads held open on a
  feature nobody needs, and when they run out, checkout stops working too.

Land it hard: *the espresso machines stop selling because the suggestions are broken.*

## 0:14–0:22 — The Pattern, From A Fuse Box

> When something is badly wrong with the wiring, the fuse trips. And it **stays**
> tripped. It does not flick itself back on hopefully every few seconds. The point is
> not to punish the toaster; it is to stop the fault setting the house on fire.
> Later somebody walks over and flips the switch back on — once — to see.

Three states on the board: closed, open, half-open. Then the question that separates
this pattern from the previous one, and it is worth having the room say it back:

> Retry asks: *did that call fail?*
> A breaker asks: **is the next attempt plausibly going to work?**

Dropped connection — yes, retry. Failed the last twenty calls — no, break.

## 0:22–0:32 — Code Walkthrough, And The Timestamps

**`CircuitBreaker.call`** — the whole thing is about a hundred lines. Ask the room to
find the three decisions. They are: am I open and is the wait over; did it work; and
have I now failed enough times.

Point at the word **consecutive** in `onSuccess`:

```java
state = BreakerState.CLOSED;
consecutiveFailures = 0;
```

Ask why a success resets rather than decrements. Answer: a service that answers three
times and fails once is not down. It is having a bad moment, and that is retry's job.

Then run act two and **do not talk about the code at all** — talk about the left-hand
column:

```
      0ms ->  3000ms  Recommendations  TIMEOUT
   3000ms ->  6000ms  Recommendations  TIMEOUT
   6000ms ->  9000ms  Recommendations  TIMEOUT   -> OPENED
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made
   9000ms ->  9000ms  Recommendations  REFUSED
   9000ms ->  9000ms  Recommendations  REFUSED
  6 pages served, 3 calls made, 3 refused, total 9000ms
```

Ask: **what stopped happening?** Let them find it. The clock stopped moving. Once the
breaker is open a page costs nothing to serve.

Be honest about the trade while you are here: the first three shoppers paid full
price. A breaker never protects the people who discover the outage. It protects
everybody after them.

Then act three, which people enjoy:

```
  14000ms -> 14000ms  Recommendations  HALF-OPEN letting one call through to test
  14000ms -> 14020ms  Recommendations  OK        [SKU-2001, SKU-2002]
  14020ms -> 14020ms  Recommendations  CLOSED    the probe worked, calls resume
  state: CLOSED -- nobody deployed anything to make that happen.
```

Ask where the scheduler is. There isn't one — the breaker compares the clock on
whatever call next arrives. Then ask why the probe is *one* call and not all of them.

## 0:32–0:44 — The Half That Gets Left Out

This is the part people remember. Spend the full twelve minutes, and resist finishing
the mechanism discussion into it.

Open with the sentence the rest depends on:

> A breaker does not make failures disappear. It makes them fail **fast**. What that
> speed buys you depends entirely on what you were calling.

### On the product page, speed buys a fallback

Suggestions are optional. The page goes out without them, the shopper still buys the
espresso machine. Easy — and ask the room *why* it was easy, because the answer is the
next section.

### At checkout, there is nothing to fall back to

Show `CheckoutService.pay`, then run act four:

```
  5 shoppers were told honestly that we cannot take payment
  0 cards were charged
```

Ask the room directly: **is the breaker worth having here at all?**

Let them argue. Then land it: what it buys is a fast, honest "no" instead of a
spinner. Both messages say the same thing; one arrives in three seconds, the other in
a hundredth of one. And it stops a thousand shoppers each holding a thread open to
discover the same outage.

### And then act five

Do not introduce this. Just run it.

```
  the shopper was shown receipt chg-assumed-ok and thanked
  cards actually charged: 0
  nothing threw, no alert fired, and the warehouse will ship an
  espresso machine nobody paid for.
```

Let the room sit with it. Then show that `PretendItWorkedCheckoutService` is wired
identically to `CheckoutService` — same dependency, same breaker, same shape — and the
difference is one `catch` block.

Ask for the rule that tells the two fallbacks apart. Steer until somebody says it:

> An empty list of suggestions is **true**. A receipt for money that never moved is
> **not true**.

Close the section: a fallback that hides a real failure is worse than the error it
replaced, because the error would have been noticed in seconds and this will be
noticed at the end of the month.

## 0:44–0:56 — Exercises

### Exercise 1 — Make one success not reset the count (everyone)

In `onSuccess`, delete `consecutiveFailures = 0;`. Run the tests.

`successResetsTheCount` fails. Ask what the breaker now does to a service that fails
one call in four, forever — and whether that service is actually down.

### Exercise 2 — Probe with everything (everyone)

In `call`, when the wait is over, let *all* waiting calls through instead of moving to
`HALF_OPEN` — drop the state change and just fall through.

Then ask what happens at 14000ms if Recommendations is still down: every caller pays
three seconds, simultaneously, against a service that is still on its knees. The one
call is the whole point of half-open.

### Exercise 3 — Tune it badly, in both directions (discussion, then code)

Change the threshold to 1, run the demo. Then change it back and set the reset wait to
60000, run it again.

Threshold 1: a single wobble trips a healthy service out of use. Wait 60000: the shop
stays degraded for a minute after Recommendations recovered. Ask which mistake they
would rather make on a Friday, and why the answer differs for suggestions and for
payments.

### Exercise 4 — Stretch: write the fallback test

`FallbackChoiceTest` has a test named `aDishonestFallbackHidesTheOutage`. Read it,
then discuss: could a test have caught act five *before* somebody thought to write
that test? What would it have asserted?

Chase it — assert that a receipt implies a charge? assert the two counts match? Then
land the conclusion: the breaker cannot know, the type system cannot know, and the
only thing that catches it is somebody asking "is this true?" out loud in a review.
That has no tidy ending, which is why it is last.

## 0:56–1:00 — Wrap-Up

Six sentences, spoken, no slides:

1. Closed means healthy and calls flow; open means tripped and calls are refused;
   half-open is one call being let through to see.
2. Retry asks whether that call failed. A breaker asks whether the next one is
   plausibly going to work.
3. Retry against a real outage is nine seconds and triple the traffic.
4. Once open, calls cost nothing — the clock stops moving.
5. It closes itself with one cheap probe, and nobody deploys anything.
6. A breaker makes failures fast, not invisible — and a fallback is only legitimate
   if what it says is true.

## Facilitator Notes

**Fix the vocabulary in the first five minutes.** If "open" is still ambiguous at
0:30, every sentence after that costs double. Write closed = current flows on the
board and point at it.

**Do not let the mechanism eat the second half.** The state machine is interesting and
the room will happily discuss thresholds for twenty minutes. Cut it at 0:32 even
mid-sentence; the fallback argument is what they will still be thinking about on
Monday.

**Somebody will say "just use Resilience4j".** Largely right for production, and not
an interruption. The answer: a library gives you the state machine, the threshold and
the timer. It cannot tell you whether your fallback is true.

**Somebody will ask about bulkheads.** That is the next pattern in the category, and
the honest answer is that a breaker protects you from *one* dependency's outage while
a bulkhead limits how much of your process any one dependency can consume. Note it and
move on.

**If the room is senior**, cut the code walkthrough to five minutes and spend the time
on Exercise 3 and Exercise 4. Most senior rooms have a story about a fallback that
lied, and that story is worth more than anything on the slides.

## Materials Checklist

- [ ] JDK 21 on every laptop, verified with `./gradlew test` before the session
- [ ] `./gradlew run` output on screen, all five acts, large enough to read the
      timestamps from the back of the room
- [ ] "CLOSED = current flows" written on the board before anybody arrives
- [ ] `docs/animation.html` open in a browser tab for 0:22–0:32
- [ ] `CheckoutService` and `PretendItWorkedCheckoutService` side by side, ready for
      0:40

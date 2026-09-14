# Session Guide — Retry with Backoff

A one-hour session. Its shape is unusual in a specific way: the naive version
*works*. It rescues checkouts, it throws no exceptions, and all five of its tests
pass. The room has to be walked all the way to a bank statement before the problem
becomes visible, and that walk is the session.

**Audience:** developers who know Java. No distributed-systems experience assumed.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. Say which failures are worth retrying and which are not, and give the rule in one
   sentence.
2. Explain why backoff exists, in terms of the service being called rather than
   politeness.
3. Explain what jitter is for, and why it is invisible with one caller.
4. Describe the lost-reply failure and say why the caller cannot detect it.
5. Define an idempotency key, say what it must be derived from, and say who has to
   keep the record for it to mean anything.
6. Point at the one line whose position separates one charge from two.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and what this project is not |
| 0:05–0:14 | The problem: a fifth of the checkouts fail for no reason |
| 0:14–0:22 | The pattern, from an engaged tone |
| 0:22–0:32 | Code walkthrough: two decisions and forty lines |
| 0:32–0:44 | The half that is usually skipped: the reply that got lost |
| 0:44–0:56 | Exercises |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And An Honest Warning

```bash
cd micro-services-design-patterns/retry-pattern
./gradlew test
```

21 tests, green, in about a second.

Then say the honest thing up front:

> There is no network in this project, no Spring Retry and no Resilience4j. The
> payment gateway is an object you can tell to time out, to decline, or — the
> interesting one — to take the money and then lose the reply. The clock only moves
> when we move it, so the backoff costs no real time. What you will learn is the
> shape of the pattern and the trap inside it. What you will not learn is how to
> configure a particular library.

## 0:05–0:14 — The Problem

Set the scene in words before any code:

> The shop takes card payments through somebody else's gateway, on the other side of
> the internet. About one call in five fails for a reason that has nothing to do
> with the payment — a dropped connection, a router that reset. The bank is fine.
> The money is there. And every one of those is a shopper who filled a basket,
> entered a card, and got an error page. Most of them do not come back.

Ask the room what to do. Somebody will say "just try again". They are right, and
the rest of the hour is about what "just" is hiding.

Run act one:

```bash
./gradlew run
```

```
      0ms ->    50ms  Payments         TIMEOUT   request never arrived
     50ms ->    50ms  Retrier          RETRYABLE attempt 1 failed: Payments did not answer
    153ms ->   153ms  Retrier          WAITED    103ms before attempt 2
    153ms ->   203ms  Payments         CHARGED   chg-1 £449.99
  card charged 1 time, £449.99 in total
```

A checkout that would have failed went through, and it cost the shopper 153
milliseconds. Let the room enjoy that for a moment — the pattern genuinely works and
they should believe in it before it is complicated.

**Then point at 103ms and ask why it is not 100.** Park the answer until 0:22.

## 0:14–0:22 — The Pattern, From An Engaged Tone

You ring someone and the line is engaged. You redial. Still engaged, so you wait a
moment and try once more. Draw out three things:

- You **judged the failure**. Engaged is temporary. "This number is no longer in
  service" is not, and you would not redial that twenty times.
- You **waited longer each time**, and not out of politeness — if the line is busy,
  the only thing that will help is time passing.
- Everybody redialling instantly is *why* the line is busy.

Then the sentence that sets up the second half of the session:

> Now imagine that when you redial, it turns out the other person had already
> answered the first time and you simply did not hear them. You would be having the
> conversation twice. A phone call is harmless to repeat. Taking money is not.

Now the two halves on screen:

1. The failure is genuinely temporary.
2. Doing the operation twice cannot do it twice.

Say plainly: everyone thinks about the first. The second is the one that charges
people twice, and we are coming back to it.

## 0:22–0:32 — Code Walkthrough

Keep it brisk. The whole retrier is about forty lines.

**`Retrier.call`** — a loop, a wait, a try, a catch. Ask where the decisions are.
There are exactly two.

**`worthRetrying`** first, because it is one line:

```java
return failure instanceof GatewayTimeoutException;
```

Ask why it is written as a *whitelist* rather than "retry unless it is a decline".
Answer: the opposite rule eventually retries a null pointer exception in your own
code four hundred times, to get four hundred identical crashes.

Run act two:

```
      0ms ->    50ms  Payments         DECLINED  the bank said no
     50ms ->    50ms  Retrier          PERMANENT not retrying: card declined for ORD-5001
  the gateway was asked 1 time
```

One attempt, fifty milliseconds, a clear answer. The naive loop takes three attempts
and three delays to arrive at the same "no".

**`RetryPolicy.delayBeforeAttempt`** next. Backoff is a multiply. Then answer the
103ms question:

> Jitter. Each caller waits a slightly different amount. With one caller it looks
> like pointless noise. With a thousand callers who all failed at the same instant,
> waiting exactly 100ms each, the stampede simply repeats on a timer.

There is a test called *two callers that fail together do not retry together*. Show
the name; it is worth more than the assertion.

**`CheckoutService.pay`** last, and slowly — it is three lines and one of them is the
punchline:

```java
PaymentRequest request = PaymentRequest.forOrder(orderId, amount);
Retrier retrier = new Retrier(policy, clock, log);
return retrier.call("payment for " + orderId, () -> payments.charge(request));
```

Do not explain why the first line is outside the lambda yet. Just note that it is,
and that you will come back to it in about four minutes.

## 0:32–0:44 — The Half That Is Usually Skipped

This is the part people remember. Spend the full twelve minutes.

### The failure you cannot see

Describe it before showing anything:

> The request arrives at the gateway. The card **is** charged. The reply is lost on
> the way home.

Then ask the room: **what does the caller see?**

Let them work it out. A timeout. Exactly the same timeout as act one. Press the
point — is there a flag? a header? a status code? No. There is nothing, and that is
not a gap in this project, it is a property of networks.

### Act three

```
      0ms ->    50ms  Payments         CHARGED-THEN-LOST chg-1 taken, reply lost
    153ms ->   203ms  Payments         REPLAYED  key already charged, returning chg-1
  card charged 1 time, £449.99 in total
```

Ask how it survived, given that the caller could not tell what had happened. Answer:
it stopped trying to. It carried the same key, and the gateway recognised it.

Now `PaymentRequest.forOrder`, and ask what the key is derived from. The order, and
nothing else. Ask what would happen if the attempt number were in there. Let
somebody say it out loud before you show act four.

### Act four

```
      0ms ->    50ms  Payments         CHARGED-THEN-LOST chg-1 taken, reply lost
     50ms ->    50ms  NaiveCheckout    RETRYING  attempt 1 failed, going again immediately
     50ms ->   100ms  Payments         CHARGED   chg-2 £449.99
  card charged 2 times, £899.98 in total
```

**Ask who is at fault.** Somebody will blame the gateway. Push back: the gateway was
handed a key it had never seen, which by definition means a new job. It behaved
perfectly. Every double charge in this project is the caller's doing.

Then read the output for what is *not* in it. No exception. No error log. No failing
test — `NaiveCheckoutServiceTest` is five passing tests and one of them asserts
£899.98. The order looks perfect. The evidence is a phone call two days later.

Finally, put the two `pay` methods side by side and let the room find the
difference themselves. It is where one line sits.

## 0:44–0:56 — Exercises

### Exercise 1 — Make the careful class naive (everyone)

In `CheckoutService.pay`, move the `PaymentRequest.forOrder(...)` line *inside* the
lambda. Run the tests.

`aLostReplyDoesNotChargeTwice` fails. Ask what it takes, in review, to notice that
line being in the wrong place — and whether anyone in the room would have caught it.

### Exercise 2 — Delete the classification (everyone)

Change `worthRetrying` to `return true`. Run act two.

The declined card is now asked three times, with two waits, to produce the same
"no". Ask what the shopper experiences, and what the gateway's owner sees in their
traffic graphs on a day when a lot of cards are declining.

### Exercise 3 — Turn off the jitter (discussion, then code)

Swap `RetryPolicy.threeAttempts(seed)` for `threeAttemptsNoBackoff()` in the demo.
Everything still passes and act one gets *faster*.

That is the discussion: the thing you just removed costs you time, buys you nothing
measurable in this demo, and is the reason a thousand-caller system does not
oscillate. How would you argue for keeping it in a code review where someone calls
it premature?

### Exercise 4 — Stretch

The retrier takes a `Supplier<T>` and has no idea what it is retrying. Discuss what
it would take for it to *refuse* to retry an operation that is not safe to repeat.

Let the room chase it: a marker interface? an annotation? a wrapper type? Then land
the conclusion — the retrier cannot know, and pushing the check into the type system
is the only honest answer. That is a genuinely good design conversation and it has
no tidy ending, which is why it is last.

## 0:56–1:00 — Wrap-Up

Six sentences, spoken, no slides:

1. Retrying turns a network blip into a completed checkout, and that is real money.
2. Retry only the failures you recognise as temporary; everything else is a definite
   answer.
3. Back off, because a struggling service needs room rather than traffic.
4. Add jitter, because a thousand callers waiting the same amount are one wave.
5. The dangerous failure is the reply lost after the work was done, and the caller
   cannot detect it — so stop trying to, and carry a key.
6. Build the request outside the retry. That one line is the difference between one
   charge and two.

## Facilitator Notes

**Do not reveal the lost reply early.** The session depends on the room believing
the naive loop is fine for the first half hour. If somebody raises double charging
at 0:10, thank them, write "act four" on the board, and hold it.

**Somebody will say "just use Resilience4j".** They are largely right for production
and it is not an interruption. The answer: a library gives you the backoff and the
classification; it cannot give you the idempotency key, and the key is the half that
costs money.

**Somebody will ask about circuit breakers.** That is the next pattern in the
category, and the right answer is that retry has its own failure mode — retrying a
service that is properly down turns a slow system into a dead one. Note it and move
on.

**If the room is senior**, cut the code walkthrough to six minutes and spend the
time on Exercise 4 and on real war stories about duplicate charges. Most senior
rooms have one.

## Materials Checklist

- [ ] JDK 21 on every laptop, verified with `./gradlew test` before the session
- [ ] `./gradlew run` output on screen, all four acts, large enough to read
- [ ] `docs/animation.html` open in a browser tab for 0:32–0:44
- [ ] The two `pay` methods side by side, ready to show at 0:44
- [ ] A whiteboard for the lost-reply sketch — request out, charge made, reply gone

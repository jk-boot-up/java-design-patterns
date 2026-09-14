# Retry with Backoff

**In plain words:** if a call fails for a reason that might not happen again, try
it once or twice more — but wait a little longer before each attempt, and be sure
that trying twice cannot do the job twice.

**Everyday analogy:** you ring someone and the call does not connect. You redial.
If it still does not connect you wait a moment before trying again, rather than
jabbing the button thirty times — partly because jabbing will not help, and partly
because everybody jabbing at once is *why* the line is busy. Waiting longer each
time is what "backoff" means.

In the shop, the flaky thing is the payment gateway. It fails about one call in
five, and almost always works on the next attempt: a dropped connection, not a
declined card. Failing a customer's checkout for that is throwing money away.

## The two halves, and the one people skip

A retry is safe when **both** of these are true:

1. The failure is genuinely temporary.
2. Doing the operation twice cannot do it twice.

The first half is the one everybody thinks about. The second half is the one that
charges people twice for an espresso machine. Nothing a retrier does can supply it
— it has to come from the caller, as an *idempotency key*: a value that says to the
gateway "if you have seen this key before, you have already done this job; do not
do it again, just tell me what happened last time".

## What the demo prints

Four acts, same order, same £449.99, same flaky gateway. The number to watch is
always the last line: how many times the card was charged.

### 1. A timeout that recovers — the case retrying is for

```
      0ms ->    50ms  Payments         TIMEOUT   request never arrived
     50ms ->    50ms  Retrier          RETRYABLE attempt 1 failed: Payments did not answer
    153ms ->   153ms  Retrier          WAITED    103ms before attempt 2
    153ms ->   203ms  Payments         CHARGED   chg-1 £449.99
    203ms ->   203ms  Retrier          RECOVERED payment for ORD-5001 succeeded on attempt 2
  card charged 1 time, £449.99 in total
```

A checkout that would have failed went through. Note the wait: 103 milliseconds,
not 100. The extra three are *jitter* — a small random amount added to every wait
so that a thousand callers who failed at the same instant do not all come back at
the same instant.

### 2. A declined card — the case retrying is not for

```
      0ms ->    50ms  Payments         DECLINED  the bank said no
     50ms ->    50ms  Retrier          PERMANENT not retrying: card declined for ORD-5001
  the gateway was asked 1 time
```

A refused card is refused for a reason, and the reason is still true a hundred
milliseconds later. Retrying it buys nothing, costs the shopper three delays, and
turns one clear answer into a vague one. Telling a timeout apart from a decline is
half of what this pattern is.

### 3. The reply is lost *after* the card is charged

```
      0ms ->    50ms  Payments         CHARGED-THEN-LOST chg-1 taken, reply lost
     50ms ->    50ms  Retrier          RETRYABLE attempt 1 failed: Payments did not answer
    153ms ->   203ms  Payments         REPLAYED  key already charged, returning chg-1
  card charged 1 time, £449.99 in total
```

This is the realistic failure and the dangerous one. From the caller's side it
looks *exactly* like act 1 — a timeout, nothing more. It cannot tell whether the
request was lost on the way out or the receipt was lost on the way home. It does
not have to: the retry carried the same key, the gateway recognised it, and handed
back the charge it had already made.

### 4. The same failure, with the loop everybody writes first

```
      0ms ->    50ms  Payments         CHARGED-THEN-LOST chg-1 taken, reply lost
     50ms ->    50ms  NaiveCheckout    RETRYING  attempt 1 failed, going again immediately
     50ms ->   100ms  Payments         CHARGED   chg-2 £449.99
  card charged 2 times, £899.98 in total
```

The shopper paid twice for one espresso machine. Read the output again and notice
what is *not* there: no exception, no error log, no failing test. The order looks
perfect. The only evidence is on a bank statement, and it surfaces as a phone call
two days later.

`NaiveCheckoutService` is three lines and has three faults, none of which shows up
as a failure:

- it builds the request **inside** the loop, so every attempt carries a new key;
- it waits not at all, so when the gateway is slow because it is overloaded, this
  is the overload;
- it cannot tell a timeout from a decline, so it asks the bank three times.

The first of those is the double charge, and it is a one-line difference.
`CheckoutService` builds the request *outside* the retry. That is the entire fix.

## Run it

```bash
./gradlew run     # the four acts above
./gradlew test    # 21 tests
```

## The tests are the proof

- `RetryTest` — a transient timeout recovers on attempt two; three timeouts give up
  honestly with nothing charged; the waits go 100, 200, 400; jitter stays inside its
  band and separates two callers; a declined card is not retried even once and is
  reported in 50ms rather than after three delays; and a lost reply after a real
  charge still charges the card exactly once.
- `NaiveCheckoutServiceTest` — **every test in it passes**, including
  `itDoubleChargesOnALostReply`, which asserts £899.98 leaving the customer's
  account. That is why it is written down: the bug is not detectable by asking
  "did it throw".
- `DemoRunsTest` — the demo is teaching material, so a test keeps it working.

No test sleeps. `SimulatedClock` only moves when the retrier moves it, so the
backoff costs nothing in wall-clock time and the suite finishes in about a second.

## One JVM, no infrastructure

No Docker, no Spring Retry, no Resilience4j, no network. `PaymentGateway` is an
ordinary object that can be told to time out, to decline, or — the interesting one
— to take the money and then lose the reply. A JDK is all you need.

## Where this sits

Retry is what you do when the instance you chose does not answer, so it follows
naturally from load balancing: the obvious retry is a retry against a *different*
instance. The pattern immediately after this one, the circuit breaker, exists
because retry has a failure mode of its own — retrying a service that is properly
down turns a slow system into a dead one.

The idempotency key introduced here gets a project of its own later, in
`idempotent-consumer-pattern`, where the same idea protects a message that is
delivered twice.

## Learning Material

| Document | What it covers |
| --- | --- |
| [`docs/problem-statement.md`](docs/problem-statement.md) | One call in five failing, the three-line loop that fixes it, and the shopper it charges twice |
| [`docs/retry-pattern-explained.md`](docs/retry-pattern-explained.md) | The pattern from an engaged tone, the two decisions, and the half that is usually skipped |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types, and the arrow that is missing — the retrier has never heard of payments |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | One attempt step by step, then all four acts as sequences, plus why jitter exists |
| [`docs/animation.html`](docs/animation.html) | The same checkout meeting three different failures, one step at a time, in a browser |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What you need to know, what you explicitly do not, and 60-second primers on idempotency and backoff |
| [`docs/session.md`](docs/session.md) | A one-hour taught session with exercises |
| [`docs/spec.md`](docs/spec.md) | The generated specification, with measured test counts and timings |
| [`docs/youtube.md`](docs/youtube.md) | Title, description and chapters for the video |
| [`video/README.md`](video/README.md) | The video pipeline, the scene list, and how to rebuild it |

### The pattern in one picture

![Class diagram](docs/images/class-diagram.png)

### Video

The narrated walkthrough is built from [`video/scenes.py`](video/scenes.py) by
[`video/build_video.sh`](video/build_video.sh). It runs about sixteen minutes
across sixteen scenes, and the rendered file is not committed — see the
repository README for why — so producing it takes about ten minutes on macOS.

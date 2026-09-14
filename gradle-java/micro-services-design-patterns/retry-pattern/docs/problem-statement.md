# Problem Statement

## Scenario

The shop takes card payments through an external payment gateway. It is somebody
else's service, on the other side of the internet, and it behaves the way such
services behave: it works almost all the time, and about one call in five fails
for a reason that has nothing to do with the payment. A dropped connection. A
router that reset. A load balancer that closed a socket a fraction early.

None of those are the bank refusing the card. The bank is fine. The money is
there. The request simply did not make the round trip.

The checkout calls the gateway, does not get an answer, and has to decide what to
tell the shopper.

## Attempt One: Tell The Shopper It Failed

The first version of the checkout does the obvious thing. It calls the gateway
once, and if the call throws, the checkout fails.

```java
Receipt receipt = payments.charge(request);   // one attempt, and that is that
```

This is not lazy code. It is honest code: something went wrong, so it says so.

The trouble is what it says so *about*. One call in five is failing for a reason
that will very probably not happen again in a hundred milliseconds, and every one
of those is a shopper who filled a basket, entered a card, and got an error page.
Most of them do not come back and try again. The shop is throwing away a fifth of
its revenue to a network blip.

## Attempt Two: Just Try Again

So somebody writes the loop everybody writes first. Three attempts, in a loop, and
give up if all three fail.

```java
for (int attempt = 1; attempt <= 3; attempt++) {
    try {
        PaymentRequest request = new PaymentRequest(orderId, amount,
                "key-" + orderId + "-attempt-" + attempt);
        return payments.charge(request);
    } catch (RuntimeException e) {
        // try again
    }
}
```

That is `NaiveCheckoutService` in this project, and it is worth being fair to it.
It works. It rescues checkouts that would have failed. It has no dependencies, it
is three lines long, and every reviewer who has ever looked at it has approved it.

## Why That Hurts

It has three faults, and the important thing about all three is that **not one of
them produces a failing test, an exception, or a line in an error log**.

**One — it charges the shopper twice.** The request is built *inside* the loop, so
each attempt carries a different idempotency key. Now consider the failure that
actually happens most often on a real payment gateway: the request arrives, the
card *is* charged, and the reply is lost on the way back. The caller sees a
timeout. It cannot tell that case apart from "the request never arrived", because
from its side they are identical. So it tries again, with a new key, and the
gateway — behaving perfectly correctly — treats it as a new order and takes the
money a second time.

The demo's fourth act prints exactly that: `card charged 2 times, £899.98 in
total`. The order looks perfect. Nothing threw. The only evidence is on a bank
statement, and it arrives as a phone call two days later.

**Two — it waits not at all.** It retries as fast as the network allows. When the
gateway is slow because it is overloaded, a thousand callers each firing three
immediate attempts *are* the overload. The retry makes the outage worse and then
fails anyway.

**Three — it cannot tell a timeout from a declined card.** A refused card is
refused for a reason: no funds, wrong expiry, a block on the account. That reason
is still true a hundred milliseconds later. The naive loop asks the bank three
times and is told "no" three times, which costs the shopper three delays and turns
one clear answer into a vague one.

## The Question This Project Answers

Trying again is obviously right and obviously dangerous at the same time. So:

- Which failures are worth retrying, and which are a definite "no" that no amount
  of persistence will change?
- How long should you wait between attempts, and why is waiting *longer each time*
  the rule rather than waiting a fixed amount?
- Why does every caller need to wait a slightly *different* amount?
- And the one that costs real money: what has to be true about the operation
  before repeating it is safe at all — and why can no retrier, however carefully
  written, supply that itself?

## The Goal

A checkout that survives a flaky network without ever charging a card twice,
that reports a declined card immediately rather than after three delays, and that
gives a struggling gateway room to recover instead of piling on.

The difference between that and the naive loop turns out to be one line moved and
one question asked about each failure. Both are in
[`retry-pattern-explained.md`](retry-pattern-explained.md).

# Retry with Backoff, Explained

## In One Sentence

If a call fails for a reason that might not happen again, try it once or twice
more — waiting a little longer before each attempt, and only if doing the job
twice cannot actually *do* it twice.

## Everyday Analogy: The Engaged Tone

You ring someone and the call does not connect. You redial. It still does not
connect, so you wait a moment and try once more.

Notice what you did without thinking about it.

You **judged the failure**. The line was engaged, which is temporary, so redialling
is sensible. If instead a recorded voice had said "this number is no longer in
service", you would not have redialled twenty times. That is a permanent answer,
and persistence does not change permanent answers.

You **waited longer each time**. Not out of politeness — out of realism. If the
line is busy, the thing that will make the next attempt succeed is time passing.
Redialling instantly cannot help, and if everybody redials instantly, everybody
jabbing at once is part of *why* the line is busy.

And here is the part that has no everyday equivalent, which is why it is the part
people get wrong. Imagine that when you redial, the other person's phone rings
again — and they had already answered the first time, and you simply did not hear
them. You would be having the conversation twice. A phone call is harmless to
repeat. **Taking money is not.**

## The Two Halves, And The One People Skip

A retry is safe when **both** of these are true:

1. The failure is genuinely temporary.
2. Doing the operation twice cannot do it twice.

Everybody thinks about the first half. The second half is the one that charges
somebody twice for an espresso machine, and nothing a retrier does can supply it.
It has to come from the caller.

## The Pattern

The retrier is a small class with exactly two decisions in it.

```java
public <T> T call(String what, Supplier<T> action) {
    for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
        long delay = policy.delayBeforeAttempt(attempt);
        if (delay > 0) {
            clock.advance(delay);
        }
        try {
            return action.get();
        } catch (RuntimeException failure) {
            if (!worthRetrying(failure)) {
                throw failure;          // a "no" does not become a "yes"
            }
        }
    }
    throw lastFailure;
}
```

Decision one is `worthRetrying`. Decision two is `delayBeforeAttempt`. Everything
else is bookkeeping.

## Decision One: Is This Failure Worth Another Go?

In this project the rule is one line:

```java
return failure instanceof GatewayTimeoutException;
```

A timeout might not happen again, so it is retryable. A `CardDeclinedException`
will happen again every single time, so it is not.

Notice the shape of that line, because it is deliberate. It retries what it
*recognises*, and treats everything else as permanent. The opposite rule — "retry
unless I recognise it" — is the one that eventually retries a null pointer
exception in your own code four hundred times, at four hundred times the cost, to
get four hundred identical crashes.

The demo's second act shows what this buys. A declined card is reported after one
attempt, in fifty milliseconds:

```
      0ms ->    50ms  Payments         DECLINED  the bank said no
     50ms ->    50ms  Retrier          PERMANENT not retrying: card declined for ORD-5001
  the gateway was asked 1 time
```

The naive loop asks three times and takes three delays to reach the same answer.
The shopper waits longer to be told the same thing, and the gateway did twice the
work for nothing.

## Decision Two: How Long To Wait

Two words describe the answer, and both mean something specific.

**Backoff** means the waits get longer: a hundred milliseconds, then two hundred,
then four hundred. The reason is not manners. If the gateway is failing because it
is overloaded, the only thing that will make the next attempt succeed is the
gateway getting some room, and a caller that retries instantly is taking room away
rather than giving it.

**Jitter** means each caller waits a slightly *different* amount. Look closely at
the first act:

```
    153ms ->   153ms  Retrier          WAITED    103ms before attempt 2
```

One hundred and three milliseconds, not one hundred. The extra three are the
jitter. With a single caller that looks like pointless noise. With a thousand
callers it is the whole point: a thousand callers who all failed at the same
instant, all waiting exactly a hundred milliseconds, come back as one wave at
exactly the same instant. The stampede simply repeats on a delay. Spreading them
over a band turns the wave into a trickle.

There is a test named for precisely this — *two callers that fail together do not
retry together* — and it is the cheapest insurance in the project.

## The Half That Is Usually Skipped: The Reply That Got Lost

Here is the failure that makes retrying genuinely dangerous, and it is the
realistic one.

The request arrives at the gateway. The card **is** charged. The reply is lost on
the way home.

From the caller's side, that is indistinguishable from "the request never
arrived". Same exception, same timeout, same everything. There is no flag to
check, no header to read, no clever piece of code that can tell the two apart —
and that is not a limitation of this project, it is a property of networks.

So what does a careful caller do? It stops trying to tell them apart, and makes
the difference not matter.

```java
public static PaymentRequest forOrder(String orderId, Money amount) {
    return new PaymentRequest(orderId, amount, "key-" + orderId);
}
```

That is an **idempotency key**: a value the caller attaches to the request which
means "if you have already seen this key, you have already done this job — do not
do it again, just tell me what happened last time".

Read what the key is derived from. The order, and nothing else. Not the attempt
number. Not the clock. Not a random value. If any of those crept in, every attempt
would carry a different key and the gateway would have no way of recognising the
repeat.

The third act is the payoff:

```
      0ms ->    50ms  Payments         CHARGED-THEN-LOST chg-1 taken, reply lost
     50ms ->    50ms  Retrier          RETRYABLE attempt 1 failed: Payments did not answer
    153ms ->   203ms  Payments         REPLAYED  key already charged, returning chg-1
  card charged 1 time, £449.99 in total
```

The card was charged once. The caller never found out which kind of failure it had
suffered, and never needed to.

## The One-Line Difference

`CheckoutService` and `NaiveCheckoutService` differ by where one line sits.

```java
// CheckoutService — built once, outside the retry
PaymentRequest request = PaymentRequest.forOrder(orderId, amount);
return retrier.call("payment for " + orderId, () -> payments.charge(request));
```

Move that first line inside the lambda and every attempt invents a fresh key, and
the careful class becomes the naive one. That is the whole of the difference
between charging a shopper once and charging them twice, and it is why this is
worth a video rather than a footnote.

It is also worth saying who is at fault in act four, because it is not who people
assume. The gateway is behaving perfectly. It honours keys correctly, it charges
each key exactly once, and it declines cards when the bank declines them. Every
double charge in this project is the caller's doing.

## What It Costs

**Time, and the shopper pays it.** A recovered checkout in act one took 203
milliseconds instead of 50. Retrying is not free; it is a trade of latency for
success rate, and there are calls where the shopper would rather have the error
quickly.

**Load, exactly when you can least afford it.** Three attempts per caller against a
struggling service is three times the traffic at the moment it is least able to
cope. Backoff and jitter reduce that; they do not remove it.

**A hard requirement on the thing you are calling.** Retrying is only safe against
an operation that can be repeated safely, and most interesting operations are not
— taking money, sending an email, shipping a parcel. Making them repeatable is
work at the other end, not something a retry loop can decide on your behalf.

**A new failure mode.** Retrying a service that is properly down turns a slow
system into a dead one: every caller now holds threads open three times as long,
waiting on something that will never answer. That is not an argument against
retrying. It is why the next pattern in this category exists.

## When Not To Use It

- **When the operation is not safe to repeat and you cannot make it safe.** No key,
  no retry. This is not a preference; it is the rule.
- **When the failure is a definite answer.** A declined card, a validation error, a
  404, a 401. Retrying these is asking the same question louder.
- **When the caller is a person waiting.** Three attempts with backoff can easily
  take a second. Sometimes an honest quick error is the better product.
- **When the service is already known to be down.** At that point you want a
  circuit breaker, not persistence.

## What To Remember

1. Retrying turns a network blip into a completed checkout, and that is worth real
   money.
2. Retry only failures you *recognise* as temporary. Everything else is permanent.
3. A declined card retried three times is three "no"s and three delays.
4. Back off — waits get longer — because a struggling service needs room, not
   traffic.
5. Add jitter, because a thousand callers waiting the same amount are one wave.
6. The dangerous failure is the reply that got lost after the work was done, and
   the caller cannot detect it.
7. So don't try to. Carry an idempotency key derived from the order and nothing
   else, and let the other end recognise the repeat.
8. Build the request *outside* the retry. That one line is the difference between
   one charge and two.

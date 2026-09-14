# The Circuit Breaker Pattern, Explained

## In One Sentence

Count the failures; once a service has failed enough times in a row, stop calling it
altogether for a while and fail instantly instead — then let one call through later
to find out whether it has recovered.

## Everyday Analogy: The Fuse Box

There is a fuse box somewhere in your house, and it is where this pattern gets both
its name and its three states.

When something goes badly wrong with the wiring, the fuse trips. And here is the part
worth noticing: it *stays* tripped. It does not flick itself back on hopefully every
few seconds to see whether the fault has gone away. The point of tripping is not to
punish the toaster. It is to stop the fault setting the house on fire.

Later, somebody walks over and flips the switch back on — once — to see what happens.
If the fault has gone, everything runs and life carries on. If it has not, the fuse
trips again immediately, and nothing was harmed by finding out.

That is the entire pattern. A counter, a decision to stop, and one careful test
afterwards.

## The Vocabulary, Which Reads Backwards

One piece of jargon, and it trips up almost everybody the first time.

**Closed is the healthy state.** A closed circuit is one where current flows, so
calls go through. An **open** circuit is a broken one, so calls do not.

So when someone says "the breaker is open", they mean the bad thing has happened and
calls are being refused. If that feels the wrong way round, you are thinking of a
door rather than a wire. Think of the wire.

There is a third state, **half-open**, which is the moment somebody is standing at the
fuse box with a finger on the switch: exactly one call is allowed through, to see.

## Retry Is A Different Question

This project sits next to the Retry pattern, and confusing the two is the most common
mistake in this area, so it is worth being precise about the difference.

Retry asks: *did that call fail?*

A breaker asks: **is the next attempt plausibly going to work?**

For a dropped connection, or a router that reset, the answer is yes — the next
attempt very well might work, so retry. For a service that has failed the last twenty
calls in a row, the answer is no. Calling it again is not optimism; it is three more
seconds gone, one more thread held open, and one more call aimed at something that is
already struggling.

Applied to a real outage, retry makes everything worse, and the demo's first act
measures exactly how much worse:

```
  the shopper waited 9000ms for a page with nothing extra on it,
  and a service that is already down received 3 more calls.
```

## The Pattern

The whole rule fits in one breath. While the breaker is **closed**, every call goes
through and consecutive failures are counted. When the count reaches the threshold,
the breaker **opens**. While it is open, no call is made at all — the caller is
refused instantly. After the reset wait has passed, one single call is allowed
through: if it works, the breaker closes and the count goes back to zero; if it
fails, the breaker opens again for another full wait.

```java
public <T> T call(Supplier<T> action) {
    if (state == BreakerState.OPEN) {
        if (clock.millis() - openedAt < resetAfterMillis) {
            callsRefused++;
            log.note(serviceName, "REFUSED", "circuit open, no call made");
            throw new CircuitOpenException(serviceName);
        }
        // The wait is over. Let exactly one call through and see.
        state = BreakerState.HALF_OPEN;
        log.note(serviceName, "HALF-OPEN", "letting one call through to test");
    }

    try {
        callsMade++;
        T answer = action.get();
        onSuccess();
        return answer;
    } catch (RuntimeException failure) {
        onFailure(failure);
        throw failure;
    }
}
```

Note the word **consecutive**. One success resets the count to zero. A service that
answers three times and fails once is not down — it is a service having a bad moment,
and that is the retry pattern's job, not this one's.

## What It Buys: Read The Timestamps

The second act serves six product pages during the outage.

```
      0ms ->  3000ms  Recommendations  TIMEOUT   no answer in 3000ms
   3000ms ->  6000ms  Recommendations  TIMEOUT   no answer in 3000ms
   6000ms ->  9000ms  Recommendations  TIMEOUT   no answer in 3000ms
   9000ms ->  9000ms  Recommendations  OPENED    3 failures in a row, not calling for 5000ms
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made
   9000ms ->  9000ms  ProductPage      DEGRADED  page served without suggestions, no call made
  6 pages served, every one of them buyable, none with suggestions
  3 calls reached Recommendations, 3 were refused without a call
  total time 9000ms
```

The thing to look at is the left-hand column, and specifically the fact that it stops
moving. Nine thousand, nine thousand, nine thousand. Once the breaker is open a page
costs *nothing* to serve.

Say that in plain terms: the first three shoppers paid for the outage, and everybody
after them got their page instantly. That is the trade the pattern makes. It does not
make the outage disappear — three people still waited three seconds each — it stops
the outage being rediscovered, at full price, by every single shopper for as long as
it lasts.

There is a test that takes this further: twenty more pages after the trip, and the
clock does not advance by a single millisecond.

## It Lets Itself Back In

The third act is the one people find slightly magical, and it is worth being clear
that there is no magic in it.

```
   9000ms ->  9000ms  Recommendations  REFUSED   circuit open, no call made
  14000ms -> 14000ms  Recommendations  HALF-OPEN letting one call through to test
  14000ms -> 14020ms  Recommendations  OK        [SKU-2001, SKU-2002]
  14020ms -> 14020ms  Recommendations  CLOSED    the probe worked, calls resume
  page: Barista Pro Espresso Machine, 2 suggestion(s)
  state: CLOSED -- nobody deployed anything to make that happen.
```

Five seconds after it opened, the breaker lets exactly one call through. That call
succeeds, so the breaker closes and normal service resumes — and nobody was paged,
nobody logged in, nobody deployed anything.

Note how cheap the probe is. It is *one* call. If Recommendations were still down,
that one shopper would wait three seconds, the breaker would open again for another
full five, and everybody else would carry on being served instantly. Recovery is
tested with a single volunteer rather than by throwing the whole queue at the door.

## The Half That Gets Left Out

Almost every tutorial on this pattern ends where the section above ends: breaker,
fallback, happy shopper. That is the easy half, and it is easy because of something
specific about the product page which nobody says out loud.

**A breaker does not make failures disappear. It makes them fail quickly.** What the
speed buys you depends entirely on what you are calling.

On the product page, speed buys a fallback. Suggestions are optional, so an empty row
of suggestions is a *true* statement — the shop genuinely has no suggestions to show
right now — and the shopper can still buy the espresso machine, which is the only
thing the shop needed from that page.

At checkout, there is nothing to fall back to. There is no substitute for taking the
money.

```java
public String pay(String orderId, Money amount) {
    try {
        return breaker.call(() -> payments.charge(orderId, amount));
    } catch (CircuitOpenException refused) {
        log.note("Checkout", "HONEST-NO", "told the shopper at once, card untouched");
        throw new CheckoutUnavailableException(
                "We cannot take payment at the moment. Your basket is saved.");
    } catch (ServiceUnavailableException failed) {
        log.note("Checkout", "HONEST-NO", "told the shopper after a timeout");
        throw new CheckoutUnavailableException(
                "We cannot take payment at the moment. Your basket is saved.");
    }
}
```

So is the breaker worthless here? No — and this is the sentence worth taking away.
What it buys at checkout is **a fast, honest "no" instead of a spinner.** Five
shoppers were told plainly that the shop cannot take payment right now, their baskets
were saved, and no card was touched. It also stops a thousand shoppers each spending
three seconds discovering the same outage, and stops their thousand waiting threads
from taking down the parts of the shop that still work.

Telling somebody "not right now, your basket is safe" in a hundredth of a second is a
genuinely better product than three seconds of spinner followed by the same answer.

## The Fallback That Lies

And then there is the fifth act, which exists because "add a fallback" is the advice
that comes attached to this pattern, and it is only good advice when there is
something *true* to fall back to.

```java
/** Always succeeds. That is the bug. */
public String pay(String orderId, Money amount) {
    try {
        return breaker.call(() -> payments.charge(orderId, amount));
    } catch (RuntimeException anything) {
        log.note("Checkout", "PRETENDED", "returned a receipt for money that never moved");
        return "chg-assumed-ok";
    }
}
```

Run it and every dashboard goes green:

```
  the shopper was shown receipt chg-assumed-ok and thanked
  cards actually charged: 0
  nothing threw, no alert fired, and the warehouse will ship an
  espresso machine nobody paid for.
```

Nothing was thrown. Nothing was logged as an error. The shopper was thanked for their
order. And the warehouse will ship an espresso machine that nobody paid for.

The distinction is exactly this: an empty list of suggestions is **true**. A receipt
for money that never moved is **not true**. A fallback that hides a real failure is
worse than the error it replaced, because the error would have been noticed in
seconds and this will be noticed at the end of the month.

## What It Costs

**Some shoppers still pay full price.** Three of them, in this demo. A breaker never
protects the people who discover the outage; it protects everybody after them.

**Tuning is a real decision, and both directions hurt.** Set the threshold too low
and a brief wobble trips a healthy service out of use. Set the reset wait too long
and the shop stays degraded for minutes after the dependency recovered. There is no
universally right pair of numbers, only numbers that suit a particular dependency.

**The breaker knows nothing about what to do instead.** `CircuitBreaker` holds no
fallback and has never heard of product pages or payments, which is what makes it
reusable — and also means it cannot stop you inventing a fallback that lies.

**One breaker per dependency, not one per application.** A breaker that mixes
Recommendations and Payments would let an outage in the optional feature refuse calls
to the one that takes money, which is the exact failure the pattern exists to prevent.

## When Not To Use It

- **When failures are isolated rather than sustained.** One dropped connection is a
  retry, not a trip. That is what *consecutive* is guarding against.
- **When the call is already instant.** The value here is the timeout you stop
  paying. Against something that fails in a millisecond there is very little to save.
- **When there is no acceptable behaviour on refusal.** Not a reason to skip the
  breaker, but a reason to think hard before adding a fallback — see act five.
- **When you have one process and one dependency and no threads to protect.** The
  pattern is about containing a failure so it does not spread; with nothing to spread
  to, it is ceremony.

## What To Remember

1. Closed means healthy and calls flow. Open means tripped and calls are refused.
   Half-open means one call is being let through to see.
2. Retry asks "did that fail?"; a breaker asks "is the next attempt plausibly going
   to work?"
3. Retry against a real outage is nine seconds of waiting and triple the traffic
   aimed at something already struggling.
4. *Consecutive* failures. One success resets the count, because a bad moment is not
   an outage.
5. Once open, calls cost nothing — read the timestamps and watch them stop moving.
6. It closes itself, with one cheap probe, and nobody deploys anything.
7. A breaker does not make failures disappear. It makes them fail fast. What that
   speed buys depends on what you are calling.
8. An empty list of suggestions is true. A receipt for money that never moved is not.
   A fallback that hides a real failure is worse than the error it replaced.

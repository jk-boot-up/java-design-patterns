# Problem Statement

## The Scenario

The shop's product page shows an espresso machine, and underneath it a short row of
suggestions: *shoppers who looked at this also looked at these*. The suggestions come
from a separate service called Recommendations.

This morning Recommendations has stopped answering.

Not *refusing* — that would be easy. It accepts the connection, and then says
nothing, and three seconds later the call gives up with a timeout. Every call. There
is no fast failure to notice and no error to catch quickly; there is just three
seconds of silence, over and over, for as long as the outage lasts.

## Attempt One: Retry, Because Retry Works

The obvious move, and the one most teams make, is to reach for the pattern that
worked last time. A call failed, so try it again.

```java
for (int attempt = 1; attempt <= ATTEMPTS; attempt++) {
    try {
        return new ProductPage(sku, "Barista Pro Espresso Machine",
                recommendations.suggestionsFor(sku), false);
    } catch (ServiceUnavailableException e) {
        log.note("ProductPage", "RETRYING", "attempt " + attempt + " timed out");
    }
}
return new ProductPage(sku, "Barista Pro Espresso Machine", List.of(), true);
```

This is not a silly thing to write. Retrying genuinely is the right answer to a
dropped connection or a router that reset, and it works often enough that it starts
to look like the right answer to every failed call.

Here is what it does to an outage:

```
      0ms ->  3000ms  Recommendations  TIMEOUT   no answer in 3000ms
   3000ms ->  3000ms  ProductPage      RETRYING  attempt 1 timed out
   3000ms ->  6000ms  Recommendations  TIMEOUT   no answer in 3000ms
   6000ms ->  6000ms  ProductPage      RETRYING  attempt 2 timed out
   6000ms ->  9000ms  Recommendations  TIMEOUT   no answer in 3000ms
   9000ms ->  9000ms  ProductPage      RETRYING  attempt 3 timed out
  page: Barista Pro Espresso Machine, 0 suggestion(s) (Recommendations left out)
  the shopper waited 9000ms for a page with nothing extra on it,
  and a service that is already down received 3 more calls.
```

Nine seconds. For a page whose extra feature the shopper would never have missed.

## Why That Hurts

**The shopper waited nine seconds to be shown nothing extra.** The page they
eventually got is identical to the page they would have got at zero seconds. Every
one of those nine seconds bought precisely nothing.

**A service that is already down received three times the traffic.** Ten shoppers
make that ninety seconds of waiting and thirty calls into a service on its knees. A
test in this project asserts both numbers. Whatever chance Recommendations had of
recovering, its callers have just reduced it.

**And the third cost is the one that takes the shop down.** For those nine seconds a
request thread is sitting idle, waiting for an answer that is not coming. Threads are
finite. A thousand shoppers browsing product pages during the outage are a thousand
threads held open on a feature nobody needs — and when they run out, checkout stops
working too. The espresso machines stop selling because the *suggestions* are broken.

That last sentence is the whole problem in one line. An outage in an optional
feature has been allowed to become an outage in the shop.

## The Question This Project Answers

Retry asks: *did that call fail?* The right question during an outage is different:

> **Is the next attempt plausibly going to work?**

For a dropped connection, yes — retry. For a service that has failed the last twenty
calls in a row, no. Calling it again is not optimism, it is arithmetic: three more
seconds gone, one more thread held, one more call aimed at something that is already
struggling, and the same answer at the end of it.

## The Second Half, Which Is Harder

Once you can fail fast, you have bought yourself a choice about what to do instead —
and that choice is where this pattern is usually taught badly.

On the product page the answer is easy. Serve the page without suggestions and say
so. The shopper can still buy the espresso machine, which is the only thing the shop
actually needed from that page.

At checkout there is no such answer. There is nothing a shop can substitute for
taking the money. So what does the breaker buy there — and what happens to a team
that assumes every dependency must have a fallback, and invents one?

```
  the shopper was shown receipt chg-assumed-ok and thanked
  cards actually charged: 0
```

## The Goal

Build something that:

1. Notices when a dependency has stopped working, rather than rediscovering it on
   every single call.
2. Stops calling it, instantly and without a timeout, while it is down.
3. Finds out on its own when it has recovered, without anybody deploying anything.
4. Leaves the decision about *what to do instead* with the caller — because the
   right answer at checkout is not the right answer on a product page.
5. Makes it obvious why a fallback that hides a real failure is worse than the
   error it replaced.

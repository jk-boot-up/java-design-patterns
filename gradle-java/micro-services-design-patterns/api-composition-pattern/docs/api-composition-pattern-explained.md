# API Composition, Explained

## In One Sentence

To build one page out of data owned by several services, ask them all at once, wait
for the slowest, and assemble the answer yourself — having decided beforehand which
of them the page cannot do without.

## Everyday Analogy: The Sandwich From Three Shops

You want a sandwich. There is no shop that sells the finished thing, so you need
bread from the baker, tomatoes from the grocer, and cheese from the deli.

Two things follow immediately, and between them they are the whole pattern.

**First: go to all three at once.** If you walk to the baker, come home, walk to the
grocer, come home, walk to the deli and come home, lunch takes three trips. Send
three people at the same time and lunch takes one trip — the longest one. You have
not made any shop faster. You have stopped waiting for one before starting the next.

**Second: decide in advance what happens if a shop is closed.** No bread means no
sandwich; that is not a partial lunch, it is no lunch. No tomatoes means a sandwich
without tomatoes, which is fine, as long as you do not tell anyone there were
tomatoes on it.

That second decision is the difficult one, it has nothing to do with programming, and
it has to be made *before* you get to the shops.

## The First Half: Sum Versus Maximum

Three calls in a queue cost the sum of their latencies:

```
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     90ms ->   210ms  Shipping         OK
  the shopper waited 210ms: 30 + 60 + 120, added up
```

The same three calls, with the two that can leave together leaving together:

```
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     30ms ->   150ms  Shipping         OK
    150ms ->   150ms  Composer         GATHERED  2 call(s) in 120ms, 0 failed
  the shopper waited 150ms: 30, then the slower of 60 and 120
```

Look at the left-hand column. Catalog and Shipping both leave at 30ms. Catalog comes
back at 90 and Shipping at 150, and the page is finished the moment the slower of the
two lands. Sixty milliseconds have gone, and the sixty that went were the ones
Shipping spent waiting for an answer it never used.

**Sequential calls cost the sum. Parallel calls cost the maximum.** That sentence is
the entire mechanical content of the pattern.

## It Is Not One Flat Fan-Out

Notice what this project does *not* do: it does not send all three calls at zero
milliseconds.

It cannot. Catalog has to be told which skus to look up, and only Orders knows which
skus are on the order. So the shape is one call, and then two together:

```java
Order order = orders.fetch(orderId);

Fanout fanout = new Fanout(clock, log);
Fanout.Branch<Map<String, String>> names =
        fanout.add("catalog", () -> catalog.namesFor(order.skus()));
Fanout.Branch<DeliveryStatus> delivery =
        fanout.add("shipping", () -> shipping.statusFor(orderId));
fanout.awaitAll();
```

The demo says so in as many words: *Catalog cannot go first — only Orders knows which
skus to ask about.*

This is where "just parallelise it" comes unstuck in real systems. Working out which
calls genuinely depend on which is most of the job, and the answer is usually a
couple of waves rather than one flat burst.

## The Second Half: A Failed Branch Is Not A Failed Page

Here is the quieter thing `Fanout` does, and it matters at least as much as the
timing. A branch that throws does not bring down the fan-out. The exception is caught
and parked on that branch:

```java
private void run() {
    try {
        value = call.get();
    } catch (RuntimeException thrown) {
        failure = thrown;
    }
}
```

Which lets the composer ask, afterwards, one branch at a time, whether *that
particular* absence is fatal. Two methods express the two answers:

- `value()` rethrows the failure — for data the page genuinely needs.
- `valueOr(fallback)` substitutes something — for data the page can do without.

The whole required-versus-optional decision comes down to which of those two the
composer calls.

## Required And Optional, Decided In Advance

In this project:

- **Orders is required.** If it fails, the composer never even builds a fan-out — the
  call throws before the fan-out exists. `itRefusesToBuildAPageWithoutTheOrder` and
  `itStopsWhenTheOrderIsMissing` assert both the error and the fact that Catalog was
  never troubled.
- **Catalog is optional.** Without it the page shows sku codes where the product names
  should be. The quantities and the money are untouched, because they were never
  Catalog's to know.
- **Shipping is optional.** Without it the delivery section says it cannot check.

Act three shows the difference against the sequential version, on exactly the same
outage:

```
  sequential: Shipping did not answer -- no page at all
             the order and the product names had already arrived. Both thrown away.
  composed:
    SKU-KETTLE   Stainless Steel Kettle   x1  £34.99
    SKU-MUG      Blue Stoneware Mug       x4  £35.96
    delivery: unknown, we cannot check this right now
  missing: [delivery status]
```

Same failure. One shopper sees an error page. The other sees what they bought, what
it cost, and an honest note about the one thing that could not be checked.

And act four shows the classification working in the other direction — the composer
refusing to build a page at all when Orders is down, which is the correct answer, not
a gap in the pattern.

## The Page Must Not Lie About What It Does Not Know

This is the part worth arguing about in a review.

`DeliveryStatus.unknown()` says *"we cannot check this right now"*. It would have been
easy to write "in transit" instead — nearly always true, reads better, nobody
complains.

Don't. A shopper who is told their parcel is in transit will not ring up about the
one that never left. The page is allowed to say it does not know. It is not allowed
to make something up. `itDoesNotInventADeliveryStatus` is a test whose entire purpose
is to stop somebody being helpful here.

`OrderDetailsPage.missingSections()` exists for the same reason at the level of the
whole page. A page that quietly drops the delivery section when Shipping is down
looks exactly like a page for an order that has not shipped yet, and the shopper
cannot tell the two apart. **Naming the gap is what makes a partial answer honest
rather than merely convenient.**

## What It Buys: Read The Arithmetic

The timing is the obvious win, and it is the smaller one.

```
  each service up 99.900% of the time -> 43.2 min down a month
  a page needing all three: 99.700% -> 129.5 min down a month
  with only Orders required: 99.900% -> 43.2 min down a month
```

Availabilities **multiply**. A page that requires three services is up only when all
three are up at once, so three services at 99.9% give a page at 99.7% — over two
hours a month instead of forty-three minutes.

The way out is not better services. There is no realistic amount of engineering that
turns 99.9% into 99.97% across three teams. The way out is **needing fewer of them**,
and that is precisely what the required-and-optional classification buys: once only
Orders is required, the page renders whenever Orders is up, and the other two outages
cost a gap on the page instead of the page.

`Availability` computes these numbers and `AvailabilityTest` pins them, so this
document cannot drift away from the code.

## What It Costs

**The page is only as fast as its slowest dependency.** Parallelism removes the
addition; it does not remove the maximum. `theSlowestDependencySetsThePace` sets
Shipping to 400ms and the page goes to 430ms. No restructuring will beat that while
Shipping is on the critical path.

**The page is only as available as the product of its *required* dependencies.**
Optional dependencies are the only lever you have, and there is a limit to how much
of a page can honestly be optional. A page where everything is optional is a page
that says nothing.

**Somebody has to make a product decision per dependency.** That is real design work
and it does not compress into configuration. It also has to be revisited whenever a
dependency is added, which is exactly when nobody remembers to.

**The fan-out is load.** One page view became three calls. Ten thousand shoppers
became thirty thousand calls, and Catalog now has to be sized for traffic it never
used to see.

## When Not To Use It

When the numbers cannot be lived with, composition has run out of road, and the
honest answer is to stop assembling on demand. If the page needs six services, or one
of them is unavoidably slow, or it is read a thousand times more often than the data
changes, keep a copy that is **already assembled** and read that instead. That is
CQRS, and it is the next pattern rather than a failure of this one.

Also skip it when there is genuinely only one service to ask. A fan-out of one is a
method call wearing a costume.

## What To Remember

1. Sequential calls cost the sum of their latencies; parallel calls cost the maximum.
2. It is rarely one flat fan-out — work out which calls genuinely depend on which, and
   you usually get a couple of waves.
3. A branch that fails must not destroy the answers the other branches already
   returned.
4. Classify every dependency as required or optional **before** the outage. It is a
   product decision, not a technical one.
5. A required dependency failing means an honest error, and that is correct
   behaviour, not a gap.
6. An optional dependency failing means a page with a named hole in it.
7. Never invent a plausible value for missing data. Say you do not know.
8. Availabilities multiply. Every required dependency you add makes the page worse
   than any service in it.
9. The page can never be faster than its slowest dependency, no matter how the calls
   are arranged.
10. When the timing or the arithmetic stops working, the answer is a pre-assembled
    copy, not more parallelism.

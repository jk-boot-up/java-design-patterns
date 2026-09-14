# Problem Statement

## The Scenario

A shopper clicks "my orders" and opens one of them. The page they expect is
unremarkable. It shows the order reference, a line for each thing they bought with
the product name and the price, the total, and underneath all of that, where the
parcel currently is.

One page. One screen. Nothing clever on it.

But the shop was split into services some time ago, and now no single service knows
enough to build that page:

- **Orders** knows the order: which skus, how many of each, what they cost.
- **Catalog** knows what a sku is actually called. `SKU-KETTLE` means nothing to a
  shopper; *Stainless Steel Kettle* does.
- **Shipping** knows the carrier and where the parcel has got to.

There is no database join available any more, because the previous project in this
category took it away on purpose. Each service owns its own data. So somebody has to
fetch three things and stitch them together, and that somebody is the code behind the
page.

## Attempt One: Three Calls, One After Another

This is what everybody writes first, and it is genuinely three lines:

```java
Order order = orders.fetch(orderId);
Map<String, String> names = catalog.namesFor(order.skus());
DeliveryStatus delivery = shipping.statusFor(orderId);
```

It works. It returns exactly the right page. Every test in
`SequentialOrderDetailsComposerTest` passes, `itBuildsTheRightPage` included. A code
review would wave it through without a comment, because there is nothing in those
three lines to object to.

## Why That Hurts

The cost is not in the code. It is in the timeline:

```
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     90ms ->   210ms  Shipping         OK
  the shopper waited 210ms: 30 + 60 + 120, added up
```

Read the second and third lines together. Shipping did not start until 90ms, so it
spent sixty milliseconds waiting for Catalog's answer — **and then did not use it.**
Shipping needs the order id, which arrived at 30ms. It had everything it needed and
sat there anyway.

That is the first cost: sequential calls are charged the *sum* of their latencies.
Three, five, eight dependencies and the page gets slower every time somebody adds
one, and nobody ever notices the moment it happened.

The second cost only shows up during an outage. Suppose Shipping is down:

```
  sequential: Shipping did not answer -- no page at all
             the order and the product names had already arrived. Both thrown away.
```

The order arrived. The product names arrived. Then the third call threw, the method
threw with it, and the shopper was shown an error page assembled out of two perfectly
good answers that nobody looked at. `itLosesWorkAlreadyDone` asserts exactly that.

## The Arithmetic Nobody Does Until It Is Too Late

And there is a third cost, which is the one that changes how you design things.

If each of the three services is up 99.9% of the time — which is a good service, and
allows it about forty-three minutes of downtime a month — then how good is the page?

It is *not* 99.9%. The page is up only when all three are up **at the same moment**,
and probabilities of independent things all happening are multiplied, not averaged:

```
  each service up 99.900% of the time -> 43.2 min down a month
  a page needing all three: 99.700% -> 129.5 min down a month
```

Three excellent services make a page worse than any one of them. Over two hours of
downtime a month, from three services that each behaved impeccably, because their
outages mostly do not overlap.

Add a fourth dependency and it gets worse again. `everyExtraDependencyCosts` pins
that in a test, so the claim cannot drift away from the code.

## The Question This Project Answers

Not "how do I call three services?" — you already know how to do that.

The question is: **what is this page allowed to do when one of the three does not
answer?**

Because there is an answer that is better than "show an error" and worse than "make
something up", and getting to it requires a decision that no framework can make for
you.

## The Second Half, Which Is Harder

Sending the calls together is arithmetic. It takes an afternoon and it is the part
every article about this pattern covers.

The half that is actually difficult is classifying each dependency, in advance, as
one the page cannot live without or one it can:

- Without **Orders** there is nothing. A page with no order on it is not a partial
  page, it is a blank one, and the shopper should get an honest error.
- Without **Catalog** the page can show sku codes instead of product names. Ugly, but
  the quantities and the money are still correct, because those were never Catalog's
  to know.
- Without **Shipping** the page can say, in plain words, that it cannot check the
  delivery status right now.

That classification is a product decision, not a technical one. Somebody who knows
what the page is *for* has to make it — and they have to make it before the outage,
because the middle of an outage is the worst possible time to be deciding what a page
means.

And there is a trap waiting inside it. Once you have decided Shipping is optional,
you need something to show instead, and "in transit" is very nearly always true. It
is also the wrong thing to write, and the reason is not technical either: a shopper
who is told the parcel is in transit will not ring up about the one that never left.

## The Goal

A composer that:

1. Sends the calls that can go together, together — so the page costs the slowest
   dependency rather than the sum of all of them.
2. Respects the dependencies that are real: Catalog cannot be asked which skus to
   name until Orders has said what they are.
3. Does not let one branch's failure destroy the answers the others already returned.
4. Knows in advance which dependencies are required and which are optional, and
   refuses to build a page when a required one is missing.
5. Says out loud what it does not know, rather than quietly leaving a hole that looks
   like an answer.

# Session Guide — API Composition

A one-hour session. It has two distinct halves, and the second is the one worth
protecting: the parallelism takes fifteen minutes and is arithmetic, while deciding
what a page is allowed to do when a dependency is missing is a genuine product
argument that most treatments of this pattern skip entirely.

**Audience:** developers who know Java. No distributed-systems experience assumed.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. State, in one sentence, the difference in cost between sequential and parallel
   calls.
2. Explain why this page is *not* one flat fan-out of three, and point at the
   dependency that forces the shape.
3. Describe what a fan-out must do with a branch that throws, and why.
4. Classify a given dependency as required or optional, and say who in their
   organisation is actually qualified to make that call.
5. Explain why a page must not invent a plausible value for data it does not have.
6. Compute, roughly, what adding a fourth required dependency does to a page's
   availability — and say why better services are not the answer.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and the page we are building |
| 0:05–0:14 | The problem: three calls in a queue |
| 0:14–0:24 | Sending them together, and why it is not a flat fan-out |
| 0:24–0:34 | The branch that fails, and required versus optional |
| 0:34–0:44 | Availabilities multiply |
| 0:44–0:56 | Exercises |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And The Page

```bash
cd micro-services-design-patterns/api-composition-pattern
./gradlew test
```

22 tests, green, in about a second.

Then describe the page in words before showing any code, because everybody has seen
it and nobody has thought about it:

> A shopper opens one of their orders. The page shows the order reference, a line for
> each thing they bought with its name and price, the total, and where the parcel
> currently is. Utterly unremarkable. Now: three different services own those facts,
> and there is no join any more.

Then the honest warning:

> There is no network in this project, no HTTP client, and no `CompletableFuture`.
> Services advance a fake clock instead of waiting. You will learn the shape of the
> pattern and the decisions it forces on you. You will not learn how to configure a
> particular HTTP library.

## 0:05–0:14 — The Problem

Show the three lines first, and defend them:

```java
Order order = orders.fetch(orderId);
Map<String, String> names = catalog.namesFor(order.skus());
DeliveryStatus delivery = shipping.statusFor(orderId);
```

Ask the room what is wrong with it. Let them look. The useful answer is *nothing* —
there is no bug, it returns the right page, and every test passes.

Then run act one:

```bash
./gradlew run
```

```
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     90ms ->   210ms  Shipping         OK
  the shopper waited 210ms: 30 + 60 + 120, added up
```

Ask: **which of those three calls needed the answer from the one before it?**

Let them find it. Catalog needed the skus, so it genuinely waited for Orders.
Shipping needed only the order id, which arrived at 30ms — and it waited sixty
milliseconds for Catalog's answer and then never looked at it.

Land it: *sequential calls cost the sum. Nobody ever notices the day the page got
slower, because the cost is not in the code, it is in the timeline.*

## 0:14–0:24 — Sending Them Together

Run act two, and read the left-hand column rather than talking about `Fanout`:

```
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     30ms ->   150ms  Shipping         OK
  the shopper waited 150ms: 30, then the slower of 60 and 120
```

Ask what changed. The answer is on one column: both optional calls now leave at 30ms.

> Sequential calls cost the sum of their latencies. Parallel calls cost the maximum.

Now the question that makes this section worth ten minutes rather than three:

> Why did we not send all three at zero milliseconds?

Steer until somebody says it: Catalog has to be told *which* skus to name, and only
Orders knows. The shape is one call, then two together. Then generalise:

> Working out which calls genuinely depend on which is most of the job. "Just
> parallelise it" is where this comes unstuck in real systems, and the honest answer
> is usually a couple of waves rather than one flat burst.

If the room is curious about how it works without threads, show `Fanout.awaitAll`:
the clock is wound back to the departure time before each branch, and forward to the
slowest arrival at the end. Do not spend more than two minutes here.

## 0:24–0:34 — The Branch That Fails

Run act three and let the two halves of the output sit side by side:

```
  sequential: Shipping did not answer -- no page at all
             the order and the product names had already arrived. Both thrown away.
  composed:
    SKU-KETTLE   Stainless Steel Kettle   x1  £34.99
    delivery: unknown, we cannot check this right now
  missing: [delivery status]
```

Same outage. One shopper gets an error page built out of two perfectly good answers
nobody looked at; the other gets their order.

Show the mechanism, which is four lines inside `Branch.run` — a `catch` that parks the
failure instead of letting it escape — and then the two accessors:

```java
public T value()                { if (failure != null) throw failure; return value; }
public T valueOr(T fallback)    { return failure == null ? value : fallback; }
```

Then say the thing worth remembering:

> Required versus optional is not configuration in this project, and it is not an
> annotation. It is which of those two methods the composer calls. One line per
> dependency, written deliberately by somebody who knows what the page is *for*.

Then run act four without introducing it:

```
  composed: Orders did not answer -- and that is correct
  a page with no order on it is not a partial page, it is a blank one
  Catalog was never called: 0 calls
```

Ask whether that is a bug. It is not — and being able to say "this one is required"
is as much a part of the pattern as being able to degrade. A composer that degrades
everything will eventually show somebody a page about nothing.

### The argument to actually have

Point at `DeliveryStatus.unknown()` and ask the room what they would have written
instead. Somebody will suggest "in transit", and they should — it is nearly always
true and it reads better.

Then land it:

> A shopper who is told their parcel is in transit will not ring up about the one
> that never left. The page is allowed to say it does not know. It is not allowed to
> make something up.

`itDoesNotInventADeliveryStatus` is a test that exists purely to stop somebody being
helpful here. Ask the room who, in their organisation, gets to make that call — and
watch them realise it is not an engineer.

## 0:34–0:44 — Availabilities Multiply

Ask the room to guess before running it:

> Three services. Each is up 99.9% of the time. How available is a page that needs
> all three?

Most rooms say 99.9%. Then run act five:

```
  each service up 99.900% of the time -> 43.2 min down a month
  a page needing all three: 99.700% -> 129.5 min down a month
  with only Orders required: 99.900% -> 43.2 min down a month
```

Let the two-hours-a-month number sit for a moment.

> Three services that each behaved impeccably combine into a page that is worse than
> any of them, because the page is up only when all three are up at the same moment,
> and their outages mostly do not overlap.

Then the question that ties the hour together:

> So how do you fix it? Make the services better?

No — there is no realistic engineering that takes three teams from 99.9% to 99.97%.
The fix is **needing fewer of them**, and that is exactly what the last section's
classification bought. Once Catalog and Shipping are optional, the page is up
whenever Orders is up, and the other two outages cost a gap instead of the page.

## 0:44–0:56 — Exercises

### Exercise 1 — Make Shipping required (everyone)

In `OrderDetailsComposer.pageFor`, change `delivery.valueOr(DeliveryStatus.unknown())`
to `delivery.value()`. Run the tests.

`itReturnsAPartialPageWhenShippingIsDown` and `itSurvivesTwoOptionalFailures` fail.
One line turned an optional dependency into a required one, and the page's
availability just dropped by an hour a month. Ask whether a code review would have
caught it.

### Exercise 2 — Break the fan-out (everyone)

In `Fanout.awaitAll`, delete `clock.moveTo(leftAt);` from inside the loop, so branches
no longer start from the same moment.

`bothBranchesLeaveTogether` and `itPaysForTheSlowestBranchOnly` fail, and the page
costs 210ms again. You have rebuilt the sequential composer without touching the
composer.

### Exercise 3 — Add a fourth dependency (discussion, then arithmetic)

Suppose the page must also show a loyalty-points balance from a fourth service at
99.9%. Work out the new availability on paper, then check it against
`everyExtraDependencyCosts`.

Then discuss: is loyalty points required or optional? Who decides? What does the page
say when it is missing? Most teams have never been asked these three questions about
a dependency they already shipped.

### Exercise 4 — Stretch: write the dishonest fallback

Change `DeliveryStatus.unknown()` to return `new DeliveryStatus("Royal Mail", "in
transit", "tomorrow")` and run the demo. Everything passes except the one test
written to stop you.

Then discuss: could a test have caught this if nobody had thought to write that one?
Chase it — assert the carrier is not made up? assert it matches something Shipping
said? Then land it: the type system cannot know, the fan-out cannot know, and the
only thing that catches it is somebody asking "is this true?" out loud in a review.
That has no tidy ending, which is why it is last.

## 0:56–1:00 — Wrap-Up

Six sentences, spoken, no slides:

1. Sequential calls cost the sum of their latencies; parallel calls cost the maximum.
2. It is rarely one flat fan-out — find which calls genuinely depend on which.
3. A branch that fails must not destroy the answers the other branches returned.
4. Classify every dependency as required or optional before the outage, not during it.
5. Never invent a plausible value for data you do not have; name the gap instead.
6. Availabilities multiply, so the only real lever is needing fewer required
   dependencies — and when that runs out, keep a copy already assembled.

## Facilitator Notes

**Do not let the parallelism eat the hour.** It is the easy half, it demos beautifully,
and a room will happily discuss thread pools until 0:50. Cut it at 0:24 even
mid-sentence. What they will still be thinking about on Monday is the delivery status
that says "in transit".

**Make them guess the availability number before you run act five.** The pattern only
lands if they have been wrong out loud first. If you show the number before the
guess, it is trivia.

**Somebody will say "just use GraphQL" or "that is what a BFF is for".** Largely right,
and not an interruption. The answer: those are places to *put* this pattern. They
give you the fan-out. Neither of them can tell you whether Shipping is optional.

**Somebody will ask about caching.** Good instinct, wrong section — say that keeping a
copy already assembled is the next pattern, CQRS, and that it is what you reach for
when the timing or the arithmetic here stops working. Note it and move on.

**If the room is senior**, cut the code walkthrough to five minutes and spend the time
on Exercise 3 and Exercise 4. Most senior rooms have a story about a page that lied
during an outage, and that story is worth more than anything on the slides.

## Materials Checklist

- [ ] JDK 21 on every laptop, verified with `./gradlew test` before the session
- [ ] `./gradlew run` output on screen, all five acts, large enough to read the
      timestamps from the back of the room
- [ ] "sum vs maximum" written on the board before anybody arrives
- [ ] [`animation.html`](animation.html) open in a browser tab for 0:14–0:34
- [ ] `SequentialOrderDetailsComposer` and `OrderDetailsComposer` side by side, ready
      for 0:14

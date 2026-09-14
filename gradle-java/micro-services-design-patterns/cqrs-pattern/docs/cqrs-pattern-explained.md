# CQRS, Explained

## In One Sentence

Stop asking the same question over and over: let the side that changes things
announce what it did, and keep a copy of the answer permanently ready for the side
that only reads.

CQRS stands for Command Query Responsibility Segregation, which is a long name for
a short idea. Commands change things. Queries read things. They are different jobs,
they have different shapes, and this pattern stops pretending they are one job.

## Everyday Analogy: The Departures Board

Stand in a railway station and look up at the departures board.

It is a copy. The truth about which train leaves from which platform lives with the
signal box and the control room, not on that board. Nobody built the board by
ringing the control room every time somebody glanced at it — thousands of people
glance at it, and the control room would spend its entire day answering the same
question.

Instead the board is **told**. When something changes, a message goes out, and the
board updates. In between messages it simply sits there, already correct, costing
nothing to read.

Three things about that board are worth carrying into the code.

**It can be a few seconds behind.** A platform changes, and for a moment the board
still says the old one. This is tolerable because it corrects itself almost
immediately, and because everyone understands what a board is.

**It is told, rather than guessing.** This is the difference between a departures
board and a printed timetable pinned to a wall. The timetable is a cache: it was
right when it was printed, it has no idea what has happened since, and the only
thing that will ever fix it is somebody printing a new one on a schedule.

**Nobody boards a train because the board said so.** The board says the train exists.
The guard, and your ticket, decide whether you get on. If the board is wrong, the
guard is still right. That is the single most important rule in this whole pattern,
and act five exists to make it impossible to forget.

Now the online shop.

## Act One — Composing The Page On Every View

The order history page is assembled from two services: ask Orders what the customer
bought, ask Catalog what the products are called, stitch the answers together. It is
done properly — the catalog call is batched, there is no loop.

Three views of that page:

```
  3 views cost 270ms and 6 service calls
  every view rebuilt a page identical to the last one
```

Ninety milliseconds and two live service calls, each time, to rebuild something that
did not change. And be clear about the scale: an order is placed once and its page
is viewed by the customer, by the confirmation email, by a support agent, by the
customer again next week. The facts changed once. The shop paid a thousand times.

## Act Two — The Page Kept Ready By The Events

Now the write side announces what it does. An order is placed, and an event goes out
saying so. Something listens, does the assembly work **once**, and keeps the finished
rows.

```
     80ms ->    85ms  ReadModel   SERVED   2 row(s), 0 other services called
     85ms ->    90ms  ReadModel   SERVED   2 row(s), 0 other services called
     90ms ->    95ms  ReadModel   SERVED   2 row(s), 0 other services called
  3 views cost 15ms and 0 service calls
```

Five milliseconds, and — the number that matters more than the milliseconds — **zero
other services called.** The order history page no longer depends on Catalog being
up. `readsSurviveAnOutage` asserts exactly that: Orders goes down, and the page still
renders.

And then the demo says the honest thing, in the demo's own words:

```
  the work did not vanish: Catalog was called 1 time when the order was placed
```

The work moved. It did not disappear. It is now paid once, at write time, instead of
once per view — and `theCostMovesToTheWriteSide` is a test rather than a claim.

That trade is only worth making because of the ratio. A shop places one order and
shows the page a thousand times. Invert that ratio — write far more often than you
read — and this pattern is a straightforward loss.

## Act Three — Eventually Consistent, Shown Honestly

Here is the part most explanations mention in a sentence and move past.

```
  ord-5001 is placed, paid for, and final
  events still in flight: 3
  rows on the customer's order history page: 0
```

The order is real. The money has moved. And the customer is looking at an order
history page with nothing on it.

That is not a bug, and no amount of careful coding removes it. It is the shape of
the pattern: the copy is updated by a message, and for as long as the message is in
flight, the copy is behind.

```
  events delivered -> rows on the page: 2
  the window is however long delivery takes, and it closes by itself
```

Two things make this survivable, and you need both. The window is short. And it
closes **by itself** — nobody has to notice, intervene, or run anything.
`theStalenessWindowIsReal` and `theWindowClosesByItself` are separate tests on
purpose, because they are separate promises.

What you must do is decide, page by page, whether that window is acceptable. For an
order history page, almost certainly. For the screen a warehouse worker uses to
decide what to put in a box, almost certainly not.

## Act Four — The Cache That Cannot Know It Is Wrong

This is where a read model stops being "a cache with extra steps".

Catalog renames a product. Both copies of the page are asked what the kettle is
called.

```
  cache says:      Stainless Steel Kettle
  read model says: Brushed Steel Kettle
  the cache will keep saying that for 300 seconds, because nothing tells it otherwise
  the read model was corrected by the same event that made it wrong
```

Read those last two lines slowly, because they are the difference.

The cache stored rows. It does not know what a product name is, it was never told
about the rename, and there is no mechanism by which it could have been told. The
only thing that will ever fix it is the clock running out — which
`itIsCorrectedByATimerAndNothingElse` asserts, and `aRenameCannotInvalidateIt`
asserts from the other side.

The read model was corrected by the very same event that made it wrong. Not later.
Not on a schedule. By the fact itself.

And `thereIsNoFreeSetting` closes the escape route. You cannot tune your way out of
this: a short expiry throws away the savings you bought the cache for, and a long
expiry means confidently showing people things that stopped being true.

A cache is a copy that cannot know it is wrong. A read model is a copy that is told.

## Act Five — The Last Kettle

And now the rule that has to survive contact with production.

```
  read model still shows on the shelf: 1
  the ledger actually has: 0
  a second shopper arrives and the read model says yes
  the ledger refused: cannot reserve 1 of SKU-KETTLE, only 0 left
  it was the write side that saved the shop, because the sale was decided there
```

The read model is inside its staleness window and says a kettle is available. It is
wrong. A second shopper tries to buy it, and nothing bad happens — because the sale
was not decided by the read model. It was decided by the stock ledger, on the write
side, which holds the actual number and refuses.

> **Show a read model's stock number. Never sell against it.**

`theWriteSideIsWhereASaleIsDecided` is the test. It is the one to remember when
somebody proposes reading a balance, a stock level or an entitlement from a
projection in order to decide something.

And then a last line that is easy to skim past:

```
  and a read model is throwaway: rebuilt from 6 events, 2 rows back
```

The read model is not data you have to protect. It is derived. Delete it, replay the
events, and it comes back — which is what `itRebuilds` demonstrates. That is a
genuinely liberating property: you can change the shape of a page, rebuild the
projection from history, and you have lost nothing. The write side holds the truth,
and `theWriteSideIsIndependent` asserts that it does not care whether anybody is
projecting at all.

## The Mechanism

There is less to it than the name suggests.

```java
public void apply(ShopEvent event) {
    // an order was placed, a product was renamed, stock changed
    // -- update the rows we keep ready
}
```

A write service that publishes what it did. An event bus. A listener that keeps a
prepared answer. A query API that reads the prepared answer and calls nobody.

There is no framework in this project, no message broker, and no database. The
lesson is not in the plumbing.

## What It Buys

- **Reads get cheap.** Ninety milliseconds and two service calls become five
  milliseconds and none.
- **Reads stop depending on other services.** The page survives an outage in a
  service it used to need.
- **The read shape is free.** A projection can be shaped exactly like the page it
  serves, instead of being the shape the write side needed.
- **Corrections arrive as facts**, not as expiries.

## What It Costs

- **Eventual consistency, in public.** Act three is the cost, and it is a cost you
  pay in front of customers.
- **More moving parts.** An event bus, a projection, and a second place where the
  same facts live.
- **A rule you have to keep.** Nothing in the type system stops somebody selling
  against a read model. Only a test, a review, and people remembering.
- **Write-time work.** You did not remove the composition; you moved it.

## When Not To Use It

- **Reads and writes are roughly balanced.** The whole trade is funded by the ratio.
- **The page cannot be stale, at all.** Then you want the write side, not a copy.
- **The composition is already cheap** — one fast local query is not worth a
  projection.
- **You want it for speed alone and have not measured.** A read model is a permanent
  second copy of your data. That is a real commitment for a page nobody complained
  about.

## What To Remember

1. Commands change things, queries read things, and they are different jobs.
2. Composing on every view is correct and gets more expensive the more popular you
   get — and nothing will ever alert you to it.
3. A cache is a copy that cannot know it is wrong. Its only correction is a timer.
4. A read model is a copy that is **told** — by the same events that changed the
   truth.
5. The work did not vanish. It moved to write time, and the ratio is what makes that
   a good deal.
6. The staleness window is real, and act three shows it at its most alarming: a paid
   order not yet on the page.
7. It closes by itself. That is what makes it survivable.
8. Reads stop depending on the services they used to compose from — which is
   availability, not just latency.
9. **Never sell against a read model.** The write side is where a decision is made.
10. A read model is throwaway. Rebuild it from the events and you have lost nothing.

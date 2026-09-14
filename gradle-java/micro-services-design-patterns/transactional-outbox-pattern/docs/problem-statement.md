# Problem Statement

## The Scenario

A customer checks out. Two things have to happen.

The order has to be saved, so the shop knows it exists and can charge for it. And the rest
of the business has to be told, so the confirmation email goes out, the warehouse starts
picking, and the analytics pipeline counts the sale.

The order goes in a database. The announcement goes on a message broker. So the checkout
code does the obvious thing:

```java
database.saveOnItsOwn(order);
broker.publish(new OutboxMessage(...));
```

Two lines. Nobody would question them in a review.

## What Goes Wrong

There is a gap between line one and line two. It is very small, and it is real.

```
Act 2 - the same two lines, and a deploy lands in between
  the process died between the save and the publish
      0ms ->     0ms  OrderDb    COMMIT  order ord-8002 on its own
      0ms ->     0ms  Orders     DIED    after the save, before the publish
  the order in the database: Order[orderId=ord-8002, total=£70.95]
  events delivered: 0, emails sent: 0
```

The order is real. The customer will be charged for it. Nobody will ever be told.

Read the worst part slowly: **there is nothing left anywhere that knows a message was
owed.** No retry can help, because nothing knows there is anything to retry. This is not a
message that failed to send; it is a message that stopped existing.

And the failure does not need a disaster. A deploy landing mid-request will do it, which is
also one of the most common reasons a request dies at all.

There are four tests in `NaiveOrderServiceTest`, and they pass:

- `theHappyPathIsFine` — most of the time, it does work
- `theCrashIsNarrow` — the window really is tiny
- `theOrderSurvives` — the database did its job perfectly
- `theEventIsLostForever` — and the announcement is simply gone

Four passing tests that describe a shop which silently loses orders.

## The Tempting Fix, And Why It Is Not One

**"Swap the two lines."** Publish first, then save. Now a crash in the gap announces an
order that does not exist, and the warehouse picks a parcel nobody paid for. The gap did not
close; it changed which of the two lies you tell.

**"Wrap it in a transaction."** A database transaction covers the database. It has no
authority over a message broker, which is a different process on a different machine. When
the transaction rolls back, the message it already published does not come back.

**"Retry the publish in a `finally`."** The process is dead. There is no `finally`.

**"Use a distributed transaction across the database and the broker."** This exists, and
almost nobody does it, because both participants must hold locks while waiting for the other
and most brokers do not support it at all.

## The Question This Project Answers

You need two things to be true together — the order exists, and the announcement was made —
and they live in two systems that cannot agree on anything.

So: how do you make a database write and a message send happen as one atomic act, when only
one of them is a database?

## The Second Half, Which Is Harder

Getting the message out is the easy part. Three facts about it are not, and this project
spends most of its time on them.

**The relay is not retry logic.** Nobody writes a retry in this pattern. The retry is a
consequence of where the message is kept — an unsent row is still there next time, and that
is all "retry" means here.

**Delivery is at-least-once, not exactly-once.** The relay can publish a message and die
before recording that it did. It will publish it again. Act 5 shows the customer's inbox
with the same confirmation in it twice.

**That duplicate is not fixable here.** It belongs to whoever receives the message. This
project's job is to be honest that the duplicate exists and to make it recognisable.

## The Goal

1. Make the order and the announcement one commit, with no window between them.
2. Keep checkout working while the broker is down.
3. Get every message delivered eventually, without anybody writing retry logic.
4. Show the crash that produces a duplicate, rather than claiming it cannot happen.
5. Make the duplicate identifiable, so the receiver has something to work with.
6. Say plainly what the guarantee is: never lost, sometimes twice.

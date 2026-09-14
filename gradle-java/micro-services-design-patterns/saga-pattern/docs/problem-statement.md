# Problem Statement — Saga

## The Scenario

An online shop. A customer clicks Place Order, and five things have to happen:

1. Reserve the stock, so nobody else can buy the last kettle.
2. Take the money.
3. Create the order.
4. Schedule a shipment with a courier.
5. Send the confirmation email.

Each of those lives in a different service, with its own database. There is no single
database underneath them, and that is not an accident — it is the previous project in this
category, Database per Service, working as intended.

So the obvious code is four calls in a row inside a `try` block. `NaiveCheckoutService` is
exactly that, and it compiles, and it reads perfectly well.

## What Goes Wrong

The fourth call fails. No courier covers the delivery address.

Here is what `./gradlew run` prints for that case, with no saga:

```
Act 5 - the same failure, without a saga
  returned: null
  card charged: £70.95
  kettles still reserved: 1
  order state: CONFIRMED
  shipments scheduled: 0
  nothing threw. A line went into a log.
```

Read those five lines as one sentence: **the customer has paid for a parcel that will never
be sent.** The stock is held for a sale that will not happen. The order says CONFIRMED. The
shop has seventy pounds ninety-five that it is not entitled to.

And nothing crashed. The exception was caught, a line went into a log, and the method
returned null. Every test in `NaiveCheckoutServiceTest` passes — including
`theFailureIsSilent`, `theMoneyStaysTaken`, `theStockStaysReserved` and
`theOrderStaysConfirmed`, which are passing tests asserting that the shop is broken.

## Why That Hurts

The log line is read for the first time three weeks later by somebody investigating a
complaint. Until then there is no alert, no failed build, no red dashboard. The only person
who knows is the customer.

Multiply by every checkout that hits a courier refusal, a declined card, or a service
having a bad afternoon, and the shop accumulates money it should not have, stock nobody can
buy, and orders that will never ship — with no list of which ones.

## The Tempting Fix, And Why It Is Not One

Somebody will say `@Transactional`. Put it on `placeOrder` and let the database sort it out.

That annotation is the most dangerous thing you could add to that file, because it looks
like it solves the problem and it does not. It wraps the method in a transaction **on this
service's own database**. It has no reach into Stock's database, none into Payments, and
none whatsoever over the card network. Rolling back a transaction that never touched the
money does not bring the money back.

The second suggestion is a distributed transaction — two-phase commit across all five
services. That does technically exist, and the reason nobody does it is that it requires
every service to hold a lock open while it waits for the others. A courier API that takes
two seconds now holds a lock on your stock table for two seconds. Under load the shop stops.

## The Question This Project Answers

If you cannot hold the five steps open until they all agree, and you cannot roll them back,
what do you do instead?

The answer is to let each step commit on its own, immediately — and to pair each one with
the action that cancels it out. Reserve stock, release stock. Take the money, refund it.
Create the order, cancel it. When a step fails, walk backwards through the steps that
already succeeded and undo them.

That is a saga, and the whole algorithm is about twenty lines in `SagaOrchestrator.run`.

## The Second Half, Which Is Harder

The mechanism is easy. What it costs is not, and this project spends most of its length on
three costs that are usually skipped.

**Compensation is not rollback.** A rollback leaves no trace. A refund is a new fact. The
demo prints the payment ledger after a compensated saga and it has *two* lines, not zero: a
charge and a refund. The customer saw the money leave and come back, and may well ring up
to ask why. `aRefundIsANewFactNotAnErasure` is that test.

**A compensation can fail too.** The refund is a network call to somebody else's service,
and it can be refused. When that happens the shop is in a state no code in this project can
fix: money taken, refund impossible. `SagaOutcome` has three values rather than two for
exactly this reason, and the third is `NEEDS_HUMAN_HELP`. In a real shop that is a row in a
queue a person works through, and not having one does not make the situation go away.

**Some steps cannot be undone at all.** There is no unsend on an email. Act four moves the
confirmation email before the shipping step and shows the result: the order is cancelled,
the money is back, and "your order is confirmed" is still sitting in the customer's inbox.
Nothing in the code is broken — the *sequence* is. Steps that cannot be undone go last.

## The Goal

By the end of this project you should be able to:

1. Say why `@Transactional` protects nothing across a service boundary, without hedging.
2. Describe a saga in one sentence: steps that commit as they go, each paired with its
   compensation, unwound in reverse when one fails.
3. Explain why compensation runs in reverse rather than forward.
4. State the difference between a rollback and a compensation, and why a ledger of a
   compensated saga has two lines rather than none.
5. Name the third outcome, say what it means operationally, and insist on having one.
6. Order the steps of a flow so that the irreversible ones come last.

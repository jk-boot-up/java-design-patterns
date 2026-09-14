# The Saga Pattern, Explained

## In One Sentence

A saga is a sequence of steps that each commit immediately and on their own, where every
step is paired with an action that cancels it out — so that when a step fails, the steps
that already succeeded can be walked backwards and undone.

## Everyday Analogy: Booking A Holiday

You are booking a holiday over the phone. Flight, hotel, hire car.

You cannot hold all three open until you are happy with all three. The airline will not
keep a seat unconfirmed while you ring the hotel, and the hotel will not hold a room while
you ring the car hire company. So you book them one at a time, and each booking is final the
moment you make it.

Then the car hire company says they have nothing that week.

You do not have a magic button that makes the last twenty minutes not have happened. What
you have is the cancellation policy for each thing you booked. So you ring the hotel and
cancel the room, then ring the airline and cancel the flight. You end up back where you
started — approximately.

Approximately, because three things are different from the way you started.

The airline charged a cancellation fee, so it cost you something. Your bank statement shows
a charge and a refund rather than nothing at all. And if you had already texted your family
to say the holiday was booked, no amount of cancelling unsends that text.

Every hard part of the saga pattern is in that paragraph.

## Act One — It Usually Works

```
      0ms ->    30ms  Stock            OK        res-1
     30ms ->   130ms  Payments         OK        chg-1
    130ms ->   150ms  Orders           OK        ord-9001
    150ms ->   210ms  Shipping         OK        shp-1
    210ms ->   250ms  Email            OK        emailed cust-7
    250ms ->   250ms  Saga             COMPLETED ord-9001 for £70.95
  no transaction spanned any of that. Each step committed on its own.
```

Five services, five steps, one order. Nothing clever happens and that is the point of
showing it first.

Read the last line carefully, because it is the thing that makes everything afterwards
necessary. **No transaction spanned any of that.** By the time payment is taken, the stock
reservation is already committed and there is nothing holding it open. By the time shipping
is called, the money is already gone. `everyStepIsAlreadyCommittedWhenTheNextOneStarts` is
that fact written as a test.

## Act Two — The Courier Refuses

```
    130ms ->   150ms  Orders           OK        ord-9002
    180ms ->   180ms  Saga   STEP-FAILED schedule shipment: no courier covers ...
    180ms ->   200ms  Orders           OK        cancelled ord-9002
    200ms ->   300ms  Payments         OK        refunded chg-1
    300ms ->   330ms  Stock            OK        released res-1
    330ms ->   330ms  Saga   COMPENSATED everything undone, customer owes nothing
  kettles back on the shelf: 20 of 20
  money the shop is holding: £0.00
  order state: CANCELLED
```

The shipping step fails, and the orchestrator walks backwards. Order cancelled, payment
refunded, stock released. The shop is back where it started and the customer owes nothing.

**Why backwards?** Not tidiness. Later steps can depend on earlier ones. The order has to be
cancelled before the payment is refunded, or finance is briefly looking at a confirmed order
with no money against it. `itCompensatesInReverse` pins the order down.

And then the demo prints something most explanations leave out:

```
  and note what the payment ledger looks like:
    CHARGE £70.95  chg-1
    REFUND -£70.95  ref-2
  two lines, not zero. A refund is a new fact, not an erasure.
```

**Compensation is not rollback.** A rollback leaves no trace — the database behaves as
though the write never happened. A refund is a new event that happens to cancel out an
earlier one. The net is zero, but the history is two lines, the customer saw the money leave
and come back, and in a real shop the card network may keep its fee.
`aRefundIsANewFactNotAnErasure` is the test, and it is the sentence to quote when somebody
describes a saga as "rollback for microservices".

## Act Three — The Refund Fails As Well

```
    200ms ->   300ms  Payments         FAILED    no answer
    300ms ->   300ms  Saga   UNDO-FAILED take payment: Payments did not answer
    300ms ->   330ms  Stock            OK        released res-1
    330ms ->   330ms  Saga   NEEDS-HUMAN could not undo [take payment]
  money the shop is holding that it should not: £70.95
```

A compensation is a call to somebody else's service over a network. It can be slow, it can
be refused, and it can fail outright. So what happens when the *refund* fails?

Two things, and both are deliberate.

**The unwinding carries on.** The payment could not be refunded, but the order was still
cancelled and the stock was still released. A saga that gave up at the first refusal would
leave more broken than it had to. `unwindingCarriesOn` asserts that.

**The outcome says so, out loud.** `SagaOutcome` has three values, not two: `COMPLETED`,
`COMPENSATED`, and `NEEDS_HUMAN_HELP`. The third one names a state no code in this project
can fix — the shop is holding money it is not entitled to and cannot give back automatically.

In a real shop that outcome is a row in a queue that a person works through. Building the
saga without one is choosing not to find out when this happens.
`aFailedCompensationNeedsAHuman` is the test, and it is the most important one in the
project.

## Act Four — The Email, Sent Too Early

```
Act 4 - the confirmation email, sent too early
  emails in the customer's inbox: 1
    "your order ord-9004 is confirmed"
  the order is cancelled and the money is back, and that email is still sitting there
  there is no unsend.
```

This act runs the same five steps with the email moved before the shipping step. Then
shipping fails.

Everything unwinds. The order is cancelled, the money is refunded, the stock goes back. And
the customer has a message in their inbox telling them their order is confirmed, which it is
not. There is no `compensate` that can help, because there is no unsend. The only available
fix is a second email apologising — which is, once again, a new fact rather than an erasure.

`SagaStep.canBeCompensated()` returns false for that step, the orchestrator records it as a
step it could not undo, and the saga reports `NEEDS_HUMAN_HELP`. Nothing in the code is
broken. **The sequence is.**

Which gives the rule: **steps that cannot be undone go last, after everything that might
fail.** `theEmailGoesLast` asserts it for the correct ordering, and
`theEmailCannotBeCompensated` asserts the consequence of getting it wrong.

## Act Five — Without A Saga

```
  returned: null
  card charged: £70.95
  kettles still reserved: 1
  order state: CONFIRMED
  shipments scheduled: 0
  a @Transactional annotation on that method would have covered its own database
  and nothing else.
```

The same failure, through `NaiveCheckoutService`: four calls in a `try` block. The customer
is charged for a parcel that will never be sent, and nothing threw.

This act is last on purpose. By the time you reach it you have seen what the alternative
costs, so the comparison is honest rather than rhetorical.

## The Mechanism

The whole thing is two pieces.

**A step that carries its own reversal.** `SagaStep` has `execute`, `compensate`, and
`canBeCompensated`. If that looks familiar it should — it is the Command pattern's `execute`
and `undo` under different names, and the reason is the same: an operation that carries its
own reversal can be sequenced, logged and unwound by code that knows nothing about what any
particular one does.

**An orchestrator that walks them.** `SagaOrchestrator.run` goes forward through the steps
keeping a list of the ones that succeeded. If one throws, it stops and walks that list
backwards calling `compensate`. It never throws; it always returns an outcome.
`itAlwaysReturnsAnOutcome` is a test, because a saga that can itself blow up has no way to
report what state the shop is in.

## Orchestration Versus Choreography

This project is an **orchestrator**: one class holds the sequence. The flow can be read in
one file and tested in one place, and the price is that every service knows the orchestrator
exists.

The alternative is **choreography**: each service publishes an event and the next one reacts
to it. Nothing is in charge, which couples the services less — and means nobody can answer
"what happens when an order is placed" without reading five codebases.

For a flow as important as checkout, being able to read it in one file is usually worth more.
For something peripheral, choreography is often the better trade. Neither is the right
answer everywhere.

## What It Buys

- Each step commits immediately, so nothing holds a lock across a network call.
- A failure part-way through leaves the shop consistent rather than half-finished.
- The failure is *visible*: an outcome object, not a log line nobody reads.
- The state that genuinely needs a person is named and reported rather than hidden.

## What It Costs

- Every step needs a compensation written, tested, and kept working.
- There is a window where the shop is inconsistent — between the failure and the end of the
  unwinding. Nothing is holding it steady during that window.
- Compensations leave traces. Two ledger lines, a phone call, a bank fee.
- Some things cannot be compensated, so the ordering of steps becomes a design decision
  with consequences.
- You need somewhere for `NEEDS_HUMAN_HELP` to go, and somebody to work through it.

## When Not To Use It

- **When one service can do the whole job.** If every write is in one database, use a
  database transaction. It is stronger and simpler, and a saga would be a worse version of it.
- **When no step can be compensated.** A saga needs an undo for most of its steps. If the
  flow is irreversible end to end, the pattern has nothing to offer.
- **When the inconsistency window is unacceptable** and cannot be shortened — some
  regulated flows genuinely need a stronger guarantee, and the honest answer is to redesign
  the boundaries rather than reach for a saga.

## What To Remember

1. You cannot hold a transaction across services, so let each step commit and pair it with
   an undo.
2. `@Transactional` covers its own database and nothing else. It is not a distributed
   transaction and it never was.
3. Compensation runs in reverse, because later steps depend on earlier ones.
4. Compensation is not rollback. A refund is a new fact, and the ledger shows two lines.
5. A compensation can fail. There are three outcomes, not two.
6. The unwinding carries on past a failed compensation rather than giving up.
7. Steps that cannot be undone go last.
8. `NEEDS_HUMAN_HELP` is not a defeat. It is the saga doing the one useful thing left:
   telling somebody.

# Session Guide — Saga

A one-hour session. The mechanism takes ten minutes: steps that commit as they go, each
paired with an undo, unwound in reverse. Everything worth the hour is what comes after —
that compensation is not rollback, that a compensation can itself fail, and that some things
cannot be undone at all.

Protect the last twenty-five minutes. A room that leaves thinking a saga is "rollback for
microservices" has learned something worse than nothing.

**Audience:** developers who know Java and have used a database transaction. No
distributed-systems experience assumed.

**Format:** laptops open. Everything runs offline with a JDK. There is no broker and no
database to install, which is worth saying at the start because people will ask.

## Learning Objectives

By the end, a participant can:

1. Say why `@Transactional` protects nothing across a service boundary, without hedging.
2. Describe a saga in one sentence and write the `SagaStep` interface from memory.
3. Explain why compensation runs in reverse.
4. State the difference between a rollback and a compensation, using the two-line ledger.
5. Name the third outcome and say what it means operationally.
6. Order the steps of a flow they own so that irreversible ones come last.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check |
| 0:05–0:15 | Act five first: the shop that took the money |
| 0:15–0:25 | The mechanism, and act one |
| 0:25–0:35 | Act two, and the two-line ledger |
| 0:35–0:45 | Act three: when the undo fails too |
| 0:45–0:55 | Act four, the ordering rule, and exercises |
| 0:55–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check

```bash
cd micro-services-design-patterns/saga-pattern
./gradlew test
```

All green, in about a second.

## 0:05–0:15 — Act Five, First

Start at the end. Open `NaiveCheckoutService` and read it aloud — four calls in a `try`
block — and ask the room what is wrong with it. Most will say nothing.

Then run the demo and read act five:

```
  returned: null
  card charged: £70.95
  kettles still reserved: 1
  order state: CONFIRMED
  shipments scheduled: 0
```

Read those five lines as one sentence: **the customer has paid for a parcel that will never
be sent.** Then say the quiet part: nothing threw, nothing alerted, and the log line gets
read three weeks later by somebody investigating a complaint.

Then show the four tests in `NaiveCheckoutServiceTest` — `theFailureIsSilent`,
`theMoneyStaysTaken`, `theStockStaysReserved`, `theOrderStaysConfirmed`. They pass. They are
passing tests asserting that the shop is broken.

**Somebody will say `@Transactional`.** Wait for it, and take it seriously, because it is
the most important misconception in the session:

> It wraps the method in a transaction on *this service's own database*. It has no reach
> into Stock's database, none into Payments, and none over the card network. Rolling back a
> transaction that never touched the money does not bring the money back.

Then mention two-phase commit, briefly, and why nobody uses it: every participant holds a
lock while waiting for the others, so one slow courier API stops the shop.

## 0:15–0:25 — The Mechanism, And Act One

The mechanism is small and should feel small. Put `SagaStep` on the screen:

```java
String name();
void execute(SagaContext context);
void compensate(SagaContext context);
default boolean canBeCompensated() { return true; }
```

Ask whether anyone recognises it. Somebody will say Command — `execute` and `undo`. Agree,
and then state the one difference that matters: an in-memory `undo` always works, and a
compensation is a network call that can be refused.

Then `SagaOrchestrator.run`. Forward, keeping a list. On a failure, backwards through that
list. That is all of it.

Then act one, and point at the last line:

```
  no transaction spanned any of that. Each step committed on its own.
```

`everyStepIsAlreadyCommittedWhenTheNextOneStarts` is that fact as a test, and it is what
makes compensation the only tool available.

## 0:25–0:35 — Act Two, And The Ledger

```
  kettles back on the shelf: 20 of 20
  money the shop is holding: £0.00
  order state: CANCELLED
```

First, the order of the undo. Ask why it goes order, then payment, then stock rather than
the other way. Let them work it out: finance should never see a confirmed order with no
money against it.

Then the part most treatments skip. Put this on the screen and stop:

```
    CHARGE £70.95  chg-1
    REFUND -£70.95  ref-2
  two lines, not zero. A refund is a new fact, not an erasure.
```

Put the sentence on the board and leave it there:

> **Compensation is not rollback.**

The net is zero. The history is not. The customer saw the money leave and come back and may
well ring up to ask why, and the card network may keep its fee.
`aRefundIsANewFactNotAnErasure` is the test.

## 0:35–0:45 — Act Three

Ask the question before showing the output: *what happens if the refund fails?*

Let the room sit with it. It is genuinely uncomfortable, and the discomfort is the lesson.

```
    300ms ->   300ms  Saga   UNDO-FAILED take payment: Payments did not answer
    330ms ->   330ms  Saga   NEEDS-HUMAN could not undo [take payment]
  money the shop is holding that it should not: £70.95
```

Two things to land, and insist on both:

1. **The unwinding carries on.** The stock was still released. A saga that gave up at the
   first refusal would leave more broken than it had to — `unwindingCarriesOn`.
2. **The outcome says so.** `SagaOutcome` has three values, not two.

Then ask the room what `NEEDS_HUMAN_HELP` *is* in their own system. The answer is a queue, a
ticket, a dashboard, a person. If they do not have one, this outcome silently becomes the
same as act five.

## 0:45–0:55 — Act Four, The Rule, And Exercises

```
  emails in the customer's inbox: 1
    "your order ord-9004 is confirmed"
  there is no unsend.
```

The email step is moved before shipping, and shipping fails. Everything unwinds, and the
customer still has a message saying their order is confirmed.

Make the rule explicit, and make somebody say it back:

> **Steps that cannot be undone go last, after everything that might fail.**

Then ask for irreversible steps in systems they own. Emails, texts, push notifications,
anything that talks to a third party, anything a customer can see. The list is longer than
people expect.

### Exercise 1 — Break the order (everyone)

Swap two steps in `PlaceOrderSteps.allOf` so payment comes before stock. Run act two and
read the timeline. Discuss what the customer experiences differently.

### Exercise 2 — Make a compensation fail (everyone)

Call `stock.failNextRelease(1)` before running act two. Watch the outcome become
`NEEDS_HUMAN_HELP`, and notice which other compensations still ran.

### Exercise 3 — Add a sixth step (pairs)

Add a loyalty-points step with its own compensation. Where in the sequence does it go, and
why? If points can be spent immediately, is it even compensatable?

### Exercise 4 — Discussion: orchestration or choreography

For a flow they own: would they rather read it in one file, or have no service know about a
coordinator? There is no right answer; the useful part is naming what each costs.

## 0:55–1:00 — Wrap-Up

Five sentences:

1. You cannot hold a transaction across services, so each step commits and carries its own
   undo.
2. `@Transactional` covers its own database and nothing else.
3. Compensation runs in reverse, because later steps depend on earlier ones.
4. Compensation is not rollback — a refund is a new fact, and the ledger has two lines.
5. There are three outcomes, and the third one needs a person and a queue to put them in.

## Facilitator Notes

- **Start at act five, not act one.** The pattern is boring until the room has felt the
  problem. Ten minutes on the broken version is the best investment in the hour.
- **Wait for `@Transactional`.** Do not pre-empt it. Someone saying it out loud and being
  shown why it fails is worth more than you asserting it first.
- **"Isn't this just a try/finally?"** will come up. Take it seriously: the differences are
  that the undo is a network call that can fail, that the order is reversed, and that there
  is a third outcome. A `finally` block has none of those.
- **"Why not just retry the shipping call?"** — a good instinct, and the answer is that
  retrying is the *previous* project and is the right first move. The saga is what happens
  when retrying has run out.
- **The two-line ledger is the emotional centre of the session.** Do not summarise it.
  Show it, stop, and ask what the customer's bank statement looks like.
- **Timings assume a group that argues.** The mechanism section compresses. Acts three and
  four do not.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` run once beforehand so nothing downloads live
- [ ] A terminal with a font big enough to read act two's timeline from the back
- [ ] [`animation.html`](animation.html) open in a browser tab for the unwinding
- [ ] [`uml-diagram.md`](uml-diagram.md) open for the five acts as sequences
- [ ] A whiteboard, for "compensation is not rollback" and the ordering rule

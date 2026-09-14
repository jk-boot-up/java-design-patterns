# Session Guide — Transactional Outbox

A one-hour session. The mechanism takes eight minutes: put the message in the database, in
the same transaction, and sweep it later. Everything worth the hour is on either side of
that — the gap that makes it necessary, and the duplicate it leaves behind.

Protect the last twenty minutes. A room that leaves thinking this pattern gives
exactly-once delivery has learned something actively dangerous.

**Audience:** developers who know Java and have used a database transaction. No broker
experience assumed.

**Format:** laptops open. Everything runs offline with a JDK. There is no broker and no
database to install, which is worth saying at the start because people will ask.

## Learning Objectives

By the end, a participant can:

1. Explain the gap between a database write and a message publish, and why reversing the
   two lines does not close it.
2. Describe the outbox in one sentence and draw the two rows in one commit.
3. Say why the relay is not retry logic.
4. State the delivery guarantee as "never lost, sometimes twice" and say where the
   duplicate comes from.
5. Name what the receiving side needs in order to cope, and say why it is not this
   project's job.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check |
| 0:05–0:15 | The two lines, and the gap |
| 0:15–0:25 | The out-tray, and act three |
| 0:25–0:35 | Act four: the broker is down |
| 0:35–0:50 | Act five: the duplicate, and what it costs |
| 0:50–1:00 | Exercises and wrap-up |

## 0:00–0:05 — Setup Check

```bash
cd micro-services-design-patterns/transactional-outbox-pattern
./gradlew test
```

All green, in about a second.

## 0:05–0:15 — The Two Lines

Put `NaiveOrderService.placeOrder` on the screen and read it aloud. Two lines: save the
order, publish the event. Ask the room what is wrong with it. Most will say nothing.

Then run act two:

```
      0ms ->     0ms  OrderDb  COMMIT  order ord-8002 on its own
      0ms ->     0ms  Orders   DIED    after the save, before the publish
  events delivered: 0, emails sent: 0
```

Read those lines as one sentence: **the order is real, the customer will be charged, and
nobody will ever be told.**

Then push on the part people miss. Ask: *what would retry this?* Let the silence sit. The
answer is nothing, because nothing anywhere recorded that a message was owed. This is not a
failed send. It is a message that stopped existing.

**Somebody will say "swap the two lines".** Take it seriously and then take it apart:
publish first, crash second, and the warehouse picks a parcel nobody paid for. The gap did
not close; you chose a different lie.

**Somebody will say "wrap it in a transaction".** A database transaction covers the
database. The broker is a different process on a different machine and will not join it.

## 0:15–0:25 — The Out-Tray

Use the analogy before the code. A letter goes in the out-tray on your desk at the same
moment you file your own copy. The post room comes round later and delivers it. Locked
door? It comes back and goes out on the next round.

Then the code, which should feel anticlimactic:

```java
database.begin()
        .save(order)
        .save(outboxMessage)
        .commit();
```

Two rows. One commit. `bothOrNeither` and `oneCommitOnly` are the tests.

Then the thing worth pointing at explicitly: **`OrderService` has no reference to the broker
at all.** Not a failed call, not an optional one — none. `theServiceNeverTalksToTheBroker`
keeps it that way.

Then `OutboxRelay.sweep()`: read unsent, publish, mark sent. Three lines.

## 0:25–0:35 — Act Four

```
  first sweep, broker still down: published 0
  messages still in the out-tray: 2
  broker comes back. Second sweep: published 2
  nobody wrote any retry logic.
```

Ask where the retry is. People will look for it. There isn't one.

Put the sentence on the board:

> **The retry is not code. It is a consequence of where the message is kept.**

Then the second, quieter win: two customers checked out fine while the broker was
unreachable. The broker being down was not a checkout outage.
`checkoutDoesNotDependOnTheBroker` is the test, and in most rooms this is the point at
which somebody thinks of a production incident they have had.

## 0:35–0:50 — Act Five, And The Bill

Ask the question before showing the output: *what if the relay publishes and then dies?*

```
  times message msg-1 was delivered: 2
  emails in the customer's inbox: 2
    "your order ord-8006 for £70.95 is confirmed"
    "your order ord-8006 for £70.95 is confirmed"
```

Three things to land, in this order:

1. **This is not fixable here.** Publishing and marking-sent are two systems, so there is a
   gap — the same gap, one level down. You can only choose which way it falls.
2. **The choice is deliberate.** Mark sent first and you lose messages. Publish first and
   you duplicate them. This pattern picks duplication, and the name for that is
   at-least-once delivery.
3. **The message id was the same both times.** `theDuplicateIsRecognisable`. That id is the
   entire handover to the receiving side.

Then ask the room to imagine the receiver is Payments rather than Notifications. Two emails
is embarrassing. Two charges is a phone call from your CEO.

## 0:50–1:00 — Exercises And Wrap-Up

### Exercise 1 — Move the gap (everyone)

Change the relay to mark the message sent *before* publishing, then run act five. Watch the
message disappear instead of duplicating. Discuss which failure you would rather have.

### Exercise 2 — Sweep order (everyone)

Queue three orders without sweeping, then sweep once. Read the timeline and confirm the
order of delivery. Does your system depend on that order? Should it?

### Exercise 3 — Discussion: who runs the relay?

Polling job, or tailing the database log? What happens if the relay is quietly dead for six
hours? How would anybody find out?

### Wrap-up: four sentences

1. A database write and a broker publish cannot be made atomic, so put the message in the
   database.
2. The service that owns the data never calls the broker.
3. Retry is not code here; it is a consequence of the message still being in the tray.
4. Delivery is at-least-once: never lost, sometimes twice — and the duplicate is the
   receiver's problem to solve.

## Facilitator Notes

- **Start with the naive version, not the pattern.** The outbox is boring until the room
  has felt the loss. Ten minutes on the two lines is the best investment in the hour.
- **Make somebody say "swap the lines".** It is the most instructive wrong answer in the
  session and it arrives on its own in almost every room.
- **"Isn't this just a queue table?"** Yes, essentially — and the insight is *which*
  database it lives in. A queue table in a separate database has exactly the original
  problem.
- **Do not let "exactly once" go unchallenged.** If somebody says it, stop and go to act
  five. This is the one misconception that causes real damage downstream.
- **The duplicate is a handover, not a failure.** Frame the end of the session as owing the
  next team a stable message id, not as an apology.
- **Timings assume a group that argues.** The mechanism section compresses. Act five does
  not.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` run once beforehand so nothing downloads live
- [ ] A terminal with a font big enough to read act four's timeline from the back
- [ ] [`animation.html`](animation.html) open in a browser tab for the gap
- [ ] [`uml-diagram.md`](uml-diagram.md) open for the five acts as sequences
- [ ] A whiteboard, for "the retry is not code" and "never lost, sometimes twice"

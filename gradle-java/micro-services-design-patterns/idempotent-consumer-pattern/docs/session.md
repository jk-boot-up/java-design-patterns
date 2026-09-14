# Session Guide — Idempotent Consumer

A one-hour session. The mechanism takes five minutes: write the handled id in the same
transaction as the effect. Everything worth the hour is on either side of it — the two ways
a `HashSet` loses, and the question of whether you needed a dedupe store at all.

Protect the last fifteen minutes. A room that leaves reaching for a dedupe table on every
consumer has learned the mechanism and missed the lesson.

**Audience:** developers who know Java and have used a database transaction. No broker
experience assumed.

**Format:** laptops open. Everything runs offline with a JDK. There is no broker and no
database to install, which is worth saying at the start because people will ask.

## Learning Objectives

By the end, a participant can:

1. Say why a broker delivers the same message twice, and why that is a contract rather than
   a bug.
2. Give the two reasons a set of seen ids in memory does not work.
3. Write the handled-id record into the same transaction as the effect, and say why that
   single commit is the whole pattern.
4. Recognise a naturally idempotent handler, and rewrite an "add" into a "set".
5. State the two costs: a table somebody operates, and an expiry window that is a guess.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check |
| 0:05–0:15 | The duplicate, and the obvious fix |
| 0:15–0:25 | Acts two and three: the two ways it loses |
| 0:25–0:35 | Act four: one commit |
| 0:35–0:50 | Act five: did you need any of this? |
| 0:50–1:00 | Exercises and wrap-up |

## 0:00–0:05 — Setup Check

```bash
cd micro-services-design-patterns/idempotent-consumer-pattern
./gradlew test
```

All green, in about a second.

## 0:05–0:15 — The Duplicate

Start with the broker, not the consumer. Ask the room: the broker sends a message and gets
no acknowledgement back. What should it do?

Let them argue. The answer is that it sends it again, because sending twice is recoverable
and losing a message is not. That is at-least-once delivery, and it is what they are running
in production whether or not anybody told them.

Then run act one:

```
     10ms ->    10ms  Broker         REDELIVERY msg-1 -- the acknowledgement was lost
     15ms ->    15ms  Notifications  SKIPPED    msg-1 -- already seen
  confirmations queued: 1
```

A `HashSet` of ids caught it. The test passes. Ask whether anybody would merge this — most
will say yes, and they are right to, because it is correct about *what* to do.

## 0:15–0:25 — The Two Ways It Loses

Run act two, and read the one line that matters out loud:

```
  the database survived the deploy. The HashSet did not.
```

Then the sentence people miss: a restart is frequently *why* the acknowledgement went
missing. The redelivery and the wiped memory are a pair, not a coincidence.

Then act three, with no restart at all:

```
      5ms ->     5ms  NotifDb        COMMIT  a confirmation on its own
      5ms ->     5ms  Notifications  DIED    after queueing the email, before remembering the id
  confirmations queued: 2
```

Ask what these two failures have in common. Push until somebody says it: **the memory is not
in the same place, or the same moment, as the work.**

Then land the stakes:

> Two emails is embarrassing. If this consumer had been Payments, it would have been two
> charges.

## 0:25–0:35 — One Commit

Put it on the screen and let it be anticlimactic:

```java
database.begin()
        .queueConfirmation(confirmationFor(message))
        .recordHandled(message.messageId())
        .commit();
```

Then run act four and read the three consequences:

```
    after a restart, confirmations queued: 1
    the process died before the commit, and nothing at all was written: 0 confirmation(s), 0 id(s)
    after the redelivery, confirmations queued: 1
```

The restart does not matter because the memory is in the database. The crash does not matter
because a crash before the commit leaves nothing, so the redelivery does the work cleanly
for the first time.

Put the sentence on the board:

> **Exactly once, out of a broker that only promises at least once — and the exactly-once
> lives in one ordinary database transaction.**

## 0:35–0:50 — Did You Need Any Of This?

Run act five. Three things, in order.

**The handler that needed nothing.** Setting a status to `SHIPPED` twice sets it to
`SHIPPED`. No store, no transaction, no expiry policy.

**The handler that could be rewritten.**

```
  "add 70 loyalty points" twice  ->  running total: 140
  "set the points for this order to 70"  ->  points awarded: 70 after handling it twice
```

Same business outcome; the second cannot be got wrong by a duplicate. Ask the room to name a
handler in their own system that could be rewritten this way. Most rooms find one inside two
minutes.

**The cost of the store, which is a guess.**

```
    a minute later, with a thirty second memory, the same message arrives again: 2 confirmation(s)
```

Ask what window they would pick, and then ask them to defend it. Too short and a duplicate
after a long broker outage looks new. Too long and it is a large table somebody operates.
There is no derived answer.

## 0:50–1:00 — Exercises And Wrap-Up

### Exercise 1 — Break the commit (everyone)

Split the transaction in `IdempotentNotificationConsumer` into two separate writes, then run
act three. Watch act three's failure come straight back.

### Exercise 2 — Rewrite a handler (everyone)

Take `LoyaltyPointsConsumer.handle` and make it idempotent without touching the dedupe
store. Compare your version to `awardForOrder`.

### Exercise 3 — Discussion: where does the effect live?

If handling the message sent a real email through a third party rather than queueing a row,
the effect and the record could not share a transaction. What would you do instead, and what
would "handled" even mean?

### Wrap-up: four sentences

1. Brokers deliver at-least-once, so duplicates are the contract.
2. A set of seen ids in memory loses to a deploy, and loses to a crash.
3. Write the handled id in the same transaction as the effect. Both, or neither.
4. Ask first whether the handler is already idempotent, or can be rewritten to be — that is
   always the cheaper answer.

## Facilitator Notes

- **Start with the broker, not the consumer.** If the room does not accept that duplicates
  are guaranteed, the rest of the hour is a solution to a problem they think they do not
  have.
- **Do not mock the `HashSet`.** It is a good instinct, wrong only about storage. Rooms
  defend it better and learn more if it is taken seriously.
- **"Can't we just use exactly-once delivery?"** This comes up every time. The exactly-once
  the room has heard of is built the same way — a dedupe store on the receiving side — just
  somebody else's.
- **Do not let act five get cut for time.** A room that leaves adding a dedupe table to every
  consumer has been made worse at this, not better.
- **The expiry window is the honest ending.** Resist the urge to give a recommended number.
  The lesson is that it is a decision with consequences in both directions.
- **Timings assume a group that argues.** The mechanism section compresses. Act five does
  not.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` run once beforehand so nothing downloads live
- [ ] A terminal with a font big enough to read act four's timeline from the back
- [ ] [`animation.html`](animation.html) open in a browser tab for the redelivery
- [ ] [`uml-diagram.md`](uml-diagram.md) open for the five acts as sequences
- [ ] A whiteboard, for "exactly once out of at least once" and the two loyalty-points lines

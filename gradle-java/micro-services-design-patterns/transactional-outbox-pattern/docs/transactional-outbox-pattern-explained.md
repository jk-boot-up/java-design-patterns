# The Transactional Outbox Pattern, Explained

## In One Sentence

Instead of writing to your database and then sending a message, write the message *into*
your database in the same transaction as the data — and let a separate process come round
later, pick up the written-down messages, and send them.

## Everyday Analogy: The Out-Tray

Think about how a busy office used to work before email.

You finish a piece of work and it needs to go to another department. You could walk it over
yourself — but then you are standing in a corridor instead of doing your job, and if the
other department's door is locked you are stuck holding it.

So you do not. You put the letter in the out-tray on the corner of your desk, at the same
moment as you file your own copy. Filing and out-tray, one movement, and you go back to
work.

Someone from the post room comes round every twenty minutes, takes whatever is in the tray,
and delivers it. If the other department is closed, the post room brings the letter back and
it goes out on the next round. Nobody had to invent a policy for that. It is simply what
happens when the letter stays in the tray until it has definitely been delivered.

And the one flaw is exactly the pattern's one flaw. If the post room delivers your letter
and then loses track of whether it did, it will deliver it again. The other department gets
it twice. That is annoying, and it is a great deal better than never getting it at all.

## Act One — Two Lines, And They Work

```
      0ms ->     0ms  OrderDb        COMMIT   order ord-8001 on its own
      0ms ->    15ms  Broker         OK       accepted msg-ord-8001
      7ms ->     7ms  Notifications  EMAILED  message msg-ord-8001
  orders saved: 1, events delivered: 1, emails sent: 1
```

Save the order, publish the event. One order, one event, one email.

This is what every test the author writes will see, and it is why the bug survives to
production. `theHappyPathIsFine` is that test, and it passes.

## Act Two — A Deploy Lands In Between

```
      0ms ->     0ms  OrderDb  COMMIT  order ord-8002 on its own
      0ms ->     0ms  Orders   DIED    after the save, before the publish
  events delivered: 0, emails sent: 0
  the order is real. The customer will be charged. Nobody will ever be told.
```

The gap between the two lines is tiny — `theCrashIsNarrow` says so explicitly — and tiny is
not zero. At a thousand orders an hour, tiny happens.

The important sentence is the one after: **nothing is left anywhere that knows a message was
owed.** There is no failed send to retry, no dead-letter queue, no error. There is an order,
and a silence.

Swapping the lines does not help. Publish first, crash second, and the shop has announced an
order it never saved.

## Act Three — Put The Message In The Database

```
  after the commit, before any sweep:
    orders saved: 1, messages waiting in the out-tray: 1, events delivered: 0
  Orders never called the broker. Now the relay comes round:
      0ms ->     0ms  OrderDb  COMMIT       1 order(s) and 1 outbox message(s) together
      0ms ->    15ms  Broker   OK           accepted msg-1
     15ms ->    15ms  OrderDb  MARKED-SENT  msg-1
```

Here is the whole idea. The order service writes two rows — the order, and the message it
owes — in **one transaction**. Then it stops. It does not call the broker at all, and
`theServiceNeverTalksToTheBroker` is the test that pins that down.

Because both rows are in one commit, there is no instant at which one exists without the
other. `bothOrNeither` and `oneCommitOnly` assert exactly that. A crash before the commit
leaves nothing; a crash after it leaves both.

Then a separate component, the relay, sweeps the out-tray: read the unsent rows, publish
them, mark them sent.

## Act Four — The Broker Is Down, And Nobody Notices

```
  two customers checked out while the broker was unreachable
  first sweep, broker still down: published 0
  messages still in the out-tray: 2
  broker comes back. Second sweep: published 2
  nobody wrote any retry logic. The retry is a consequence of where the message is kept.
```

Two things happen here that are worth separating.

**Checkout kept working.** It never needed the broker, so the broker being down is not a
checkout outage. `checkoutDoesNotDependOnTheBroker` is the test.

**The messages waited, and then went.** No retry loop, no backoff configuration, no
scheduled-retry table. An unsent row is still an unsent row on the next sweep.
`nothingIsLostWhenTheBrokerIsDown` and `theTrayIsCollectedInOrder` cover it.

That is the sentence to remember: **the retry is not code, it is a consequence of where the
message is kept.**

## Act Five — What The Guarantee Costs

```
  the broker took the message. Emails sent: 1
  but the relay died before writing down that it had, so the out-tray still holds: 1
  ...
  times message msg-1 was delivered: 2
  emails in the customer's inbox: 2
    "your order ord-8006 for £70.95 is confirmed"
    "your order ord-8006 for £70.95 is confirmed"
```

The relay publishes, and then dies before it can mark the row as sent. The row is still
unsent, so the next sweep publishes it again. The customer gets the email twice.

You cannot engineer this away. Publishing and marking-as-sent are in two different systems,
so there is a gap between them — which is, exactly, the gap this whole pattern was invented
to close, reappearing one level down.

What you can do is choose which way the gap falls. Mark sent *first* and a crash loses the
message. Publish first and a crash duplicates it. **The pattern chooses to duplicate**, and
that choice has a name: at-least-once delivery. `deliveryIsAtLeastOnce` is the test.

The fix is not in this project. It belongs to whoever receives the message. What this
project owes the receiver is a way to spot the duplicate, and it provides one: the message
id was identical both times. `theDuplicateIsRecognisable` asserts it.

## The Mechanism

Three pieces, and none of them is clever.

**An outbox row.** `OutboxMessage` is a record with a message id, a type, and the payload,
stored in the same database as the business data.

**One transaction.** `OrderDatabase.begin()` returns a `Transaction` that can save an
`Order` and an `OutboxMessage` and then `commit()` both. Nothing is visible until the
commit — `writesAreHeldUntilTheCommit` proves it.

**A relay.** `OutboxRelay.sweep()` reads the unsent rows, publishes each to the broker, and
marks each sent. If publishing fails, the row is left where it is.

In a real system the relay is either a polling job like this one, or a process tailing the
database's replication log. The choice affects latency and load, not the guarantee.

## What It Buys

- The data and the announcement are one atomic act, with no window between them.
- Checkout does not depend on the broker being up.
- Every message is delivered eventually, with no retry logic written by anybody.
- Messages go out in the order they were written down.

## What It Costs

- **Latency.** The message goes out on the next sweep, not immediately.
- **A moving part.** Somebody has to run and monitor the relay. A relay that is quietly
  dead looks exactly like a quiet shop.
- **Table growth.** Sent rows accumulate and need clearing out.
- **Duplicates.** At-least-once, forever. This is not tunable.
- **A dependency on the next pattern.** The receiving side has to cope with duplicates, or
  the guarantee you bought is a bill you passed downstream.

## When Not To Use It

- **When losing the message genuinely does not matter.** Some analytics events are like
  this. Be honest about which ones.
- **When the message is not about data you are writing.** If there is no database
  transaction to join, there is no outbox to be part of.
- **When your broker and database genuinely support a distributed transaction and you have
  a strong reason** — rare, and the operational cost is usually worse than duplicates.

## What To Remember

1. A database write and a broker publish cannot be made atomic, so do not try.
2. Write the message into the database, in the same transaction as the data.
3. The service that owns the data never calls the broker at all.
4. A separate relay sweeps the out-tray, publishes, and marks rows sent.
5. Retry is not code here. It is a consequence of the message still being in the tray.
6. The broker being down is not a checkout outage.
7. Delivery is at-least-once: never lost, sometimes twice.
8. The duplicate is somebody else's problem, and the least you owe them is a stable message
   id to recognise it by.

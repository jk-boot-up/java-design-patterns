# Problem Statement

A message broker will deliver the same message twice. Not because it is broken — because
that is what it promises. The question this project answers is what the code on the
receiving end is supposed to do about it.

## The Scenario

Our online shop publishes an `OrderPlaced` message when a customer checks out. The
notification service receives it and queues a confirmation email.

Then the acknowledgement back to the broker gets lost — a network blip, a restart, a
timeout — and the broker, having no way to know the message was handled, sends it again.
That is at-least-once delivery, and it is the only thing almost every real broker offers.

So the same `OrderPlaced` for order `ord-7002` arrives at the notification service twice,
and the customer must still receive exactly one email.

## The Obvious Answer, And The Test That Blesses It

Keep a set of the message ids you have already seen. If the id is in the set, skip it.

```java
if (seen.contains(message.messageId())) {
    return;
}
seen.add(message.messageId());
database.queueConfirmationOnItsOwn(confirmationFor(message));
```

Act one of the demo runs exactly this, and it works:

```
     10ms ->    10ms  Broker         REDELIVERY msg-1 -- the acknowledgement was lost
     15ms ->    15ms  Notifications  SKIPPED    msg-1 -- already seen
  confirmations queued: 1
```

`theObviousTestPasses` and `differentIdsAreBothHandled` are both green. This is the version
that ships.

## What Goes Wrong

**The memory is in the wrong place.** The set of seen ids lives in a field, in a process.
Act two restarts the process between the two deliveries:

```
      5ms ->     5ms  NotifDb        COMMIT     a confirmation on its own
     10ms ->    10ms  Notifications  RESTARTED  and its memory of what it has handled is empty
     15ms ->    15ms  NotifDb        COMMIT     a confirmation on its own
  confirmations queued: 2
    "your order ord-7002 for £70.95 is confirmed"
    "your order ord-7002 for £70.95 is confirmed"
```

The database survived the deploy. The `HashSet` did not. `theMemoryLivesInTheProcess` is the
test that pins this down.

And the pairing is not unlucky. A restart is one of the most common reasons an
acknowledgement goes missing in the first place, so the redelivery and the empty memory tend
to arrive together.

**There is a gap even without a restart.** Act three does the work and then dies before
recording the id:

```
      5ms ->     5ms  NotifDb        COMMIT  a confirmation on its own
      5ms ->     5ms  Notifications  DIED    after queueing the email, before remembering the id
  confirmations queued: 2
```

The email was queued and the id was not remembered, so the redelivery queued it again. Two
separate writes, and a gap between them — `theGapIsTheProblem` is the test.

Two confirmation emails is embarrassing. Had this consumer been the payments service, it
would have been two charges on a customer's card.

## The Question This Project Answers

Not "how do I spot a duplicate" — a set of ids spots it fine. The question is:

**how do I make remembering that I handled the message part of the same act as handling
it?**

## The Second Half, Which Is Less Comfortable

Three things this pattern does not let you off:

- **The store is a real table you now operate.** It grows with every message, so its rows
  have to expire, and the expiry window is a number somebody chooses rather than derives.
  Too short and a duplicate arriving after a long broker outage looks new. Too long and it
  is a large table with a retention policy attached. `theWindowIsAGuess` asserts the failure
  directly.
- **The effect and the record must share one transaction.** If they do not, you have
  rebuilt act three with extra steps.
- **Sometimes you do not need any of it.** Setting a shipment status to `SHIPPED` twice sets
  it to `SHIPPED`. Some handlers are naturally idempotent, and some can be rewritten to be —
  "add 70 points" doubles, "set the points for this order to 70" does not. Reaching for a
  dedupe table before asking that question is the most common mistake in this area.

## The Goal

By the end of this project you should be able to:

1. Say why at-least-once delivery is what you get, and why exactly-once is not on offer from
   the broker.
2. Explain why a set of seen ids in memory is not a solution, in one sentence about deploys.
3. Write the record of having handled a message into the same transaction as its effect.
4. Recognise a naturally idempotent handler, and rewrite an "add" into a "set" where you can.
5. State the two costs — a table to operate, and an expiry window that is a guess.
6. Say what the sending side owes you: a stable message id, and nothing else.

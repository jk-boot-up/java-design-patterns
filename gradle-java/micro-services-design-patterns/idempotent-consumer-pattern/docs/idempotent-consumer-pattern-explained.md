# The Idempotent Consumer Pattern, Explained

## In One Sentence

Handling the same message twice has the same effect as handling it once, because the record
of having handled it is written in the same transaction as its effect.

## An Everyday Analogy: The Ticket Stub

You hand your ticket to somebody at the door of a concert. They do not just glance at it and
wave you through — they tear it, and keep the stub, in the same motion as letting you in.

If you come back round with the same ticket, the stub is already in their box and you do not
get in twice.

Now notice what would go wrong if the two halves came apart. If the doorman let you in and
then intended to tear the ticket afterwards, a shift change in between would let you walk
back in. If the doorman only remembered faces rather than keeping stubs, the next doorman on
would remember nothing at all.

That is the whole pattern. The record and the effect are one act, and the record lives
somewhere that outlives the person doing the checking.

Our worked example is an online shop, and the effect is a confirmation email.

## Act One — A Set Of Ids, And It Works

The notification service receives `OrderPlaced` for `ord-7001`, queues the confirmation, and
adds the message id to a `HashSet`. The acknowledgement to the broker is lost, so the broker
delivers the same message again. The id is in the set, and the second delivery is skipped.

```
     10ms ->    10ms  Broker         REDELIVERY msg-1 -- the acknowledgement was lost
     15ms ->    15ms  Notifications  SKIPPED    msg-1 -- already seen
  confirmations queued: 1
```

One email. The test passes. This is the version everybody writes, and it is worth being
clear that it is not stupid — it is correct about *what* to do, and wrong only about *where
to keep the evidence*.

## Act Two — The Deploy

Same two deliveries, and a restart in between.

```
     10ms ->    10ms  Notifications  RESTARTED  and its memory of what it has handled is empty
  confirmations queued: 2
    "your order ord-7002 for £70.95 is confirmed"
    "your order ord-7002 for £70.95 is confirmed"
```

The database survived the deploy. The `HashSet` did not.

And this is not a rare coincidence. A restart is frequently *why* the acknowledgement went
missing, so the redelivery and the wiped memory arrive as a pair much more often than
chance would suggest.

## Act Three — The Gap

Take the restart away and there is still a hole. The consumer queues the email, and then
dies before it records the id.

```
      5ms ->     5ms  NotifDb        COMMIT  a confirmation on its own
      5ms ->     5ms  Notifications  DIED    after queueing the email, before remembering the id
  confirmations queued: 2
```

Two writes, two moments, and a gap between them. Anything that can die can die in that gap.
Two emails is embarrassing; if this consumer had been the payments service it would have
been two charges.

## Act Four — One Commit

The fix is to stop treating "do the work" and "remember that I did it" as two things.

```java
database.begin()
        .queueConfirmation(confirmationFor(message))
        .recordHandled(message.messageId())
        .commit();
```

Two rows. One commit. Both, or neither.

```
      5ms ->     5ms  NotifDb        COMMIT   1 confirmation(s) and 1 handled id(s) together
     15ms ->    15ms  Notifications  IGNORED  msg-1 -- handled already
  confirmations queued: 1, handled ids stored: 1
```

Then the demo runs the two failures that beat the `HashSet` straight at it:

```
    after a restart, confirmations queued: 1
    the process died before the commit, and nothing at all was written: 0 confirmation(s), 0 id(s)
    after the redelivery, confirmations queued: 1
```

The restart no longer matters, because the memory is in the database. The crash no longer
matters, because a crash before the commit leaves nothing at all, and the redelivery then
does the work cleanly for the first time.

**Exactly once, out of a broker that only promises at least once.** That sentence is the
whole point, and it is worth noticing where the exactly-once lives: not in the broker, and
not in the network. It lives in one ordinary database transaction on the receiving side.

## Act Five — The Handler That Needed None Of This

Before reaching for a dedupe store, ask whether the handler needs one.

`ShipmentStatusConsumer` sets the status of an order to `SHIPPED`. Handle that message
twice and the status is `SHIPPED`.

```
  status of ord-7006: SHIPPED, orders known: 1
  no dedupe store, no transaction, no expiry policy.
```

That is a **naturally idempotent** operation, and it is always the better answer when it is
available: no table, no transaction, nothing to operate.

And often a handler that is not naturally idempotent can be rewritten into one that is.
Awarding loyalty points is the classic:

```
  "add 70 loyalty points" twice  ->  running total: 140 points for a 70 pound order
  "set the points for this order to 70"  ->  points awarded: 70 after handling it twice
```

Same business outcome, and the second form cannot be got wrong by a duplicate. `addingTwiceDoublesIt`
and `theRewriteBeatsTheStore` are the two tests, side by side, and they are the most useful
pair in the project.

## What It Costs

**A table you now operate.** Every handled id is a row. The table grows for as long as
messages arrive, so the rows have to be cleared out, which means somebody owns a retention
job and somebody gets paged when it stops running.

**An expiry window that is a guess.** The demo makes this explicit rather than glossing it:

```
    handled, confirmations queued: 1
    a minute later, with a thirty second memory, the same message arrives again: 2 confirmation(s)
```

The duplicate came back after the memory of it had expired, and the consumer treated it as
new. `theWindowIsAGuess` asserts that outcome deliberately. Too short a window and a
duplicate arriving after a long broker outage looks new. Too long and the table is large.
There is no correct number; there is a number you choose and defend.

**A transaction that must actually cover both.** The pattern only works if the effect and
the record commit together. If the effect goes to one system and the record to another, you
are back in act three, with extra machinery.

**Latency and contention, in a busy system.** Every message now reads and writes the dedupe
table.

## When Not To Use It

- **When the handler is already idempotent.** Setting a value, replacing a document, marking
  a flag. Add nothing.
- **When it can be rewritten to be idempotent.** Turn increments into assignments where the
  business allows it. This is cheaper than any store.
- **When the effect is not in a database you control.** If handling the message sends a real
  email through a third party, the effect and the record cannot share a transaction, and you
  need a different conversation about what "handled" means.
- **When duplicates genuinely do not matter.** A metrics ping counted twice is a rounding
  error, not an incident. Be honest about which of your messages these are.

## What To Remember

1. Brokers promise at-least-once delivery. Duplicates are a feature of the contract, not a
   bug in somebody's code.
2. A set of seen ids in memory is not a solution, because a deploy empties it — and a deploy
   is often what caused the redelivery.
3. Even without a restart, doing the work and recording the id as two separate writes leaves
   a gap that a crash fits through.
4. Write the record of having handled the message in the **same transaction** as its effect.
   Both, or neither.
5. That single ordinary transaction turns at-least-once delivery into exactly-once
   processing.
6. Ask first whether the handler is naturally idempotent, or can be rewritten to be. That is
   the better answer whenever it is available.
7. The store is a real table with a real retention policy, and the expiry window is chosen
   rather than derived.
8. All the sending side owes you is a stable message id. That one field is the entire
   handover.

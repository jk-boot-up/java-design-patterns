# Session Guide — Event Sourcing Pattern

A one-hour taught session for a small group. It assumes everyone has a JDK 21 and
has cloned the repository; it does not assume anyone has seen event sourcing before.

The session is built around one move that has to land: **the balance is not stored**.
Everything else follows from that, and if it does not land, nothing else will.

## Learning Objectives

By the end, a participant can:

1. State the pattern in one sentence and give the bank-statement analogy unprompted.
2. Point at the line in `CurrentStateLoyaltyAccounts.award` where the order id and
   the date are thrown away.
3. Explain why the repair for the double-award bug touches no events at all.
4. Name the four costs — replay time, snapshot staleness, erasure, and event
   versioning — and say what each one actually breaks.
5. Say in one sentence each how CQRS and event sourcing differ.
6. Decide, for a system they work on, whether it should use this pattern. The
   expected answer for most of them is no, and that is a successful outcome.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and the warning |
| 0:05–0:15 | The problem: the row that cannot answer |
| 0:15–0:25 | The pattern: three moves |
| 0:25–0:38 | Code walkthrough |
| 0:38–0:50 | Exercises |
| 0:50–0:58 | The bill, and CQRS |
| 0:58–1:00 | Wrap-up |

## 0:00–0:05 — Setup, And The Warning

```bash
cd gradle-java/platform-design-patterns/event-sourcing-pattern
./gradlew test    # 31 tests, about a second
```

Then say the warning out loud, before anything else:

> Most of the systems you work on should not use this pattern. It is the most
> over-applied pattern in this course. We are going to spend the first half on why
> it is wonderful and the second half on what it costs, and the second half is the
> half that will save you.

Saying this at the start rather than the end changes how the room listens.

## 0:05–0:15 — The Problem: The Row That Cannot Answer

Run the first two acts.

```bash
./gradlew run
```

**Act 1.** A customer asks why their balance is 140, and the entire available answer
is "the row says 140 points. How it got there was never written down."

Now show them `CurrentStateLoyaltyAccounts.award` and ask the room to read the
signature and then the body:

```java
public void award(String customerId, int amount, String orderId, LocalDate on) {
    this.points.merge(customerId, amount, Integer::sum);
}
```

Wait for someone to notice that `orderId` and `on` are never used. This is the
single most valuable ten seconds in the session. The loss is not a bug; it is the
design, and it happens on that line.

**Act 2.** The double-awarding release. Three customers, three balances, and the
question: which is wrong, and by how much?

```
    C-5120 = 100 points
    C-5122 = 25 points
    C-5121 = 60 points
```

Give the room a minute to try. They cannot do it. A doubled £45 order on top of a
£10 one writes 100, and one honest £100 order writes 100. The bug destroyed the
evidence of itself.

## 0:15–0:25 — The Pattern: Three Moves

On a whiteboard, not in the code.

1. **Make each change a fact with a name**, in the past tense. Not "add 60 to the
   balance" but "sixty points were awarded to C-4417 on 1 March for order ORD-8801".
2. **Append it to a log, and never touch it again.** One operation: add to the end.
3. **Derive the state by folding.** Start at zero, walk the events, add them up.

Then the analogy, and let it run: your bank does not send you the number, it sends
you the statement. The number at the bottom is the only thing you could work out
from the rest. And nobody edits a statement — a wrong payment gets a reversing line,
and both stay on the page forever.

Ask: **why is that the only design under which last month's statement still means
what it said last month?**

## 0:25–0:38 — Code Walkthrough

Four files, in this order, ten minutes.

**`LoyaltyEvent.java`** — three points. Past-tense names (a command can be refused, a
fact cannot). Self-contained (no reference to an `Order` object, because the order
may have changed since). Sealed (the compiler knows the list is complete).

**`LoyaltyEventStore.java`** — show them that `append` is the whole write side, and
then show them what is *not* in the file. No update. No delete. Note that nothing is
validated here either: by the time a fact is in the log it is history, and history
does not get vetoed.

**`EventSourcedLoyaltyAccounts.java`** — ask the room to find the balance field.
Give them long enough to be sure. There isn't one.

**Acts 3, 4 and 5.** The three payoffs, in order:

- *Why is it 140?* Four lines with a running total, including the expiry, which is
  the call support dreads most.
- *What was it on 3 March?* One `continue` on the date. Nobody planned the question;
  the answer was already there.
- *Where did the bug do damage?* `duplicateAwards` was written weeks after the bug
  shipped, and it works, because the data was already lying there.

Then the line to stop on:

```
  no event was edited and none was deleted. The reading code changed,
  and every balance is right again.
```

Ask the room why the log was not wrong. Keep asking until someone says it: the shop
really did award those points twice. That is what happened. What was wrong was the
interpretation.

## 0:38–0:50 — Exercises

### Exercise 1 — Add an event (everyone)

Add `PointsAdjusted` for a support agent correcting a balance by hand, carrying a
reason and the agent's name. Notice what the compiler tells you when the sealed
interface gains a fourth permitted type.

### Exercise 2 — Repair the other way (everyone)

Fix the double-award bug by appending a correcting event instead of changing the
read. Get it working, then discuss: which would you rather explain to an auditor,
and which to a developer joining next year? There is a real answer in the javadoc on
`balanceWithDuplicateAwardsIgnored` and it is not the one the demo uses.

### Exercise 3 — Break the repair (discussion)

Suppose a promotion lets one order legitimately award points twice. What happens to
`balanceWithDuplicateAwardsIgnored`? This is the honest limit of the rule the demo
uses, and spotting it is the exercise.

### Exercise 4 — Stretch

Add `pointsExpiringBefore(customerId, day)` answered from the log alone. Then try to
add it to `CurrentStateLoyaltyAccounts`, and stop when you see why you cannot.

## 0:50–0:58 — The Bill, And CQRS

Run acts 6, 7 and 8 and take them quickly; the numbers do the arguing.

**Replay cost.** 5,000 events read for one balance. A snapshot brings it to one
read for the same answer.

**Snapshot staleness.** But a snapshot is a stored balance, which is the thing the
pattern set out to avoid. It records `computedBy` for a reason: when that code
turns out to have had a bug, the snapshot is wrong forever and nothing throws. The
cure is `discardAll()` and a refold, which is cheap only because the log kept
everything. **The log is the truth; a snapshot is a cache.**

**Erasure.** A customer with a legal right to be forgotten meets a log with no
delete. Show what "just delete their events" does: their history is destroyed beyond
recovery *and* a snapshot taken earlier still reports their balance. Ask the room
what they would do. Then give the two real answers — encrypt the personal fields and
destroy the key, or keep the event's shape and blank the identity out of it — and
point out that both have to be designed in before the first event is written.

**Versioning.** Somebody added the order id field in 2023. The duplicate hunt finds
zero duplicates in a stream that visibly contains two identical awards, and nothing
reports a problem. An event is a schema you version and never migrate.

**CQRS.** Act 9, two sentences: CQRS changes where reads come from. Event sourcing
changes what the writes store. Point at `OrderHistoryReadModel`, which is CQRS with
no event log anywhere in it, and at `EventSourcedLoyaltyAccounts`, which is event
sourcing with no second model at all.

## 0:58–1:00 — Wrap-Up

Ask each participant to name one system they work on and say whether it should use
this pattern. Most answers should be no. The ones that should be yes have a common
shape: **the history is the product** — money, loyalty, orders, anything an auditor
can ask about.

Close on the one sentence: store the facts, derive the total.

## Facilitator Notes

- The moment to protect is the search for the balance field. Do not shorten it, and
  do not answer it for them.
- If someone says "this is just an audit log", the answer is that an audit log is a
  *second* copy, and second copies drift out of step with the first. Here there is
  only one copy, and the balance is derived from it.
- If someone says "this is just Kafka", separate the pattern from the product. The
  log here is an `ArrayList`.
- Watch for the room getting excited and wanting to use it everywhere. That is the
  failure mode this session is designed to prevent, which is why the warning goes at
  0:00 and the bill gets eight full minutes.

## Materials Checklist

- [ ] JDK 21 on every machine, `./gradlew test` green
- [ ] A whiteboard for the three moves and the bank statement
- [ ] `docs/animation.html` open in a browser for the fold
- [ ] `docs/images/class-diagram.png` on screen for the walkthrough

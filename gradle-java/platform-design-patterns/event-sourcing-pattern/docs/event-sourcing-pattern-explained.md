# The Event Sourcing Pattern, Explained

## In One Sentence

**Store the things that happened, in the order they happened, and never change
them — then work out the current state by adding them up.**

The balance is not a thing you keep. It is a thing you calculate.

## Everyday Analogy: The Bank Statement

You have a bank account. Somewhere in the bank there is a number that says how much
money you have. But that is not what the bank sends you at the end of the month —
it sends you a list. Salary in on the twenty-eighth. Rent out on the first. A
refund from a shop you had forgotten about. Line after line, each with a date, an
amount and a description, and a running total down the right-hand side.

Now think about why the statement is the list and not the number.

If the bank only sent you the number, and the number was wrong, you would have no
way to find out where it went wrong. You could not say "that one, on the twelfth, I
did not make that payment". You could only say "this is not the amount I expected",
and neither you nor the bank could do anything with that.

The number at the bottom of the statement is the least interesting thing on the
page. It is also the only thing you could work out from the rest. Every line above
it is a fact somebody was told; the total is arithmetic.

Event sourcing is the decision to build software the way a bank statement is built.
Keep the lines. Add them up when somebody asks.

And one more thing the analogy gives you for free: nobody edits a bank statement.
If a payment was wrong, the bank does not go back and change the line — it adds a
new line that reverses it, and both lines stay on the statement forever. That is
not the bank being awkward. That is the only design under which last month's
statement still means what it said last month.

## The Problem, In The Shop

The shop's loyalty scheme gives one point per pound, lets points be spent on later
orders, and expires anything unused after twelve months. The obvious
implementation, and the one nearly everybody writes, keeps a number per customer:

```java
public void award(String customerId, int points, String orderId, LocalDate on) {
    this.points.merge(customerId, points, Integer::sum);
}
```

That is `CurrentStateLoyaltyAccounts`, and the balance it produces is correct. Read
the method signature and then the body, though. An order id comes in. A date comes
in. Neither is used. The addition happens and the two facts that would have
explained it are gone.

So when a customer asks why their balance is a hundred and forty, the whole answer
the shop can give is the number again:

```
the row says 140 points. How it got there was never written down.
```

And when a release awards points twice for three weeks before anybody notices,
finding the damage is impossible, because a doubled forty-five pound order on top of
a ten pound one writes `100`, and one honest hundred pound order also writes `100`.
The bug erased the evidence of itself.

## The Pattern

Three moves, and the third is the one people miss.

**One: make each change a fact with a name.** Not `points = points + 60`, but "sixty
points were awarded to C-4417 on the first of March for order ORD-8801". A thing
that happened, named in the past tense, carrying everything needed to understand
it.

**Two: append it to a log, and never touch it again.** The log has one operation:
add to the end. There is no update and no delete, and that absence is the design.
The past does not change, so the record of the past must not either.

**Three: derive the state by folding the log.** The balance is not a field anywhere
in the program. When somebody asks for it, start at zero, walk the customer's
events in order, apply each one, and return what you end up with. Ask again a second
later and the same walk happens again.

That third move is the hard one to accept, because it looks wasteful and it looks
slow, and sometimes it is both — the second half of this document is about paying
for it. But look first at what it buys.

## Participants

| Role | In this project | What it decides |
| --- | --- | --- |
| **Event** | `LoyaltyEvent` and the three records that implement it | Nothing. An event is a fact; it has no behaviour and no opinion |
| **Event store** | `LoyaltyEventStore` | Only the order things go in. It has `append` and it has reads, and it has no way to change anything |
| **Aggregate / projection** | `EventSourcedLoyaltyAccounts` | How events turn into a balance. Every read is a fold; this is the only place the meaning of an event lives |
| **Snapshot** | `Snapshot`, `SnapshotStore` | Nothing about correctness. It is a cache, and it says which event it was taken at and which code took it |
| **The caller** | `Checkout` | Whether to append at all. It cannot tell the two implementations apart, because both implement `LoyaltyAccounts` |
| **The contrast** | `CurrentStateLoyaltyAccounts` | Kept deliberately, and kept correct. It is what the pattern is being compared against |

## Code Walkthrough

### The event

```java
public sealed interface LoyaltyEvent
        permits PointsAwarded, PointsRedeemed, PointsExpired {
    String customerId();
    LocalDate on();
    int effectOnBalance();
    String because();
}
```

Three things to notice.

The names are all in the **past tense**. `PointsAwarded`, not `AwardPoints`. This is
not a style preference: `AwardPoints` is a request, which can be refused, and
`PointsAwarded` is a fact, which cannot. Everything in the log is the second kind.
If you find yourself wanting to validate an event on the way in, the name is wrong
and it is really a command.

Each event is **self-contained**. `PointsAwarded` carries the order id and the date
inside it. It does not hold a reference to an `Order` object, because the order it
refers to may have changed since, and the point of the log is that reading it in
2027 gives you what was true in 2025.

The interface is **sealed**, so the compiler knows the three kinds are the only
kinds. Add a fourth event and every `switch` over them stops compiling until it is
handled — which is exactly the reminder you want.

### The store

```java
public void append(LoyaltyEvent event) {
    events.add(event);
}
```

That is the whole write side. There is no `update` and no `delete`, and the absence
is the guarantee. In a real system this is a table with an auto-incrementing id and
no `UPDATE` grant, or a file opened in append mode. The mechanism varies; the
promise does not.

Note also that nothing is validated here. The store does not care whether a
redemption leaves the balance negative — that decision belongs to the code deciding
whether to append, and it is made *before* the event exists. By the time a fact is
in the log it is history, and history does not get vetoed.

### The fold

```java
int running = 0;
for (LoyaltyEvent event : store.eventsFor(customerId)) {
    running += event.effectOnBalance();
}
return running;
```

There is no balance field in `EventSourcedLoyaltyAccounts`. Search the class for
one; it is not there. This loop *is* the balance, and it runs every time somebody
asks.

### And now the three things that come free

**Why is it 140?** Print the same walk instead of just its answer:

```
  2025-03-01  earned 60 points on order ORD-8801                   balance 60
  2025-03-03  spent 25 points on order ORD-8814                    balance 35
  2025-03-08  earned 120 points on order ORD-8907                  balance 155
  2025-03-14  lost 15 points to the twelve-month expiry            balance 140
```

Support can read that to a customer down the phone. Note the last line especially:
the expiry is explained too, and "where did my points go" is the call support dreads
most.

**What was it on the third of March?** Same sum, stopped earlier:

```java
if (event.on().isAfter(day)) { continue; }
```

Nobody planned for that question. Nobody created a history table for it. The answer
was already in the data:

```
  on 1 March:  60 points
  on 3 March:  35 points
  on 8 March:  155 points
  on 20 March: 140 points
```

**Where did the bug do damage?** This is the strongest argument in the project. The
double-awarding release has shipped and been fixed. Now, weeks later, somebody
writes a query that did not exist when the bug was live:

```java
public List<String> duplicateAwards(String customerId) { ... }
```

```
  orders that earned points more than once:
    ORD-9001 awarded 2 times
```

And the repair:

```
  balance with the second award ignored: 55 points
  no event was edited and none was deleted. The reading code changed,
  and every balance is right again.
```

Read that last line twice. The log was never wrong — the shop really did award those
points twice, and that really is what happened. What was wrong was the
interpretation. So the fix lives in the code that interprets, and the log is
untouched. `BugInvestigationTest` asserts exactly this: `store.size()` before the
repair equals `store.size()` after it.

## What this simulation does not show

This project starts nothing. No database, no Kafka, no container, no HTTP port. The
event store is an `ArrayList` in memory and the whole thing runs offline with a JDK.
That buys the pattern's shape, and the shape is real — what an event is, what may go
in the log, where the meaning of an event lives, why the repair is a read. Those do
not change when the list becomes a table.

Several things that matter in production are genuinely absent, and it is worth being
straight about which:

**Durability and ordering are assumed.** An `ArrayList` never loses an append and
never reorders one. A real log has to decide what "appended" means — written to
disk, replicated to two nodes, acknowledged by a quorum — and every answer costs
latency. Nothing here exercises that.

**Concurrency is absent.** Two `append` calls for the same customer at the same
instant is the whole difficulty of a real event store, and the usual answer is an
expected-version check that rejects the second writer. There is one thread here, so
there is nothing to reject.

**The cost numbers are reads, not milliseconds.** Act 6 measures events examined —
5000, then 5001, then 1. Those ratios are honest and the ratio is the lesson. The
wall-clock cost of the same fold against a database over a network is a different
number that this project does not measure.

**There is no subscriber.** Real event logs are read by other services, which is
half of why people adopt them. Nothing subscribes here.

Finish this project and you will know what event sourcing is, could write one, and
will know what it costs you. You will not have operated one.

## Why The Tests Are The Proof

Both implementations produce the same balance, so `EventSourcedLoyaltyAccountsTest`
opens by asserting exactly that — `row.balanceFor(...)` equals
`accounts.balanceFor(...)`. If the pattern's selling point were "a correct balance",
there would be nothing to sell.

`CurrentStateLoyaltyAccountsTest` is the test file worth reading most carefully,
because every test in it **passes**. It is not a list of failures waiting to be
fixed by the pattern. It pins down a boundary: the balance is right, and every
question past the balance has no answer in that design. The sharpest one builds the
same hundred points twice, once by a bug and once honestly, and asserts that the two
are indistinguishable:

```java
assertEquals(honest.explain("C-5120"), doubled.explain("C-5120"));
```

`SnapshotTest` and `ErasureAndEventVersioningTest` are the bill, as assertions
rather than as warnings. The important one is `aStaleSnapshotIsSilentlyWrong`,
because it demonstrates a wrong balance that looks exactly like a right one.

`DemoRunsTest` captures the demo's output and checks the numbers this document
quotes are the numbers the program prints, so a document can never drift from the
code without a test going red.

## What You Gain

**An answer to "why".** Every balance can be explained line by line, to a customer,
an auditor or a developer at two in the morning.

**Questions you did not plan for.** As-of queries, duplicate hunts, "which orders
earned the points that expired" — none of these needed a table designed in advance.
The past was kept, so the past can be interrogated.

**Repairs that do not rewrite history.** A misinterpretation is fixed by changing
the interpreter. The record of what happened stays what happened, and every previous
answer remains explainable.

**A single source of truth.** There is no balance that can drift out of step with
its audit log, because there is no second copy. An audit log bolted onto a
current-state design is a second copy, and second copies disagree.

## What To Watch Out For

**Reads get slower as the log gets longer, and the fix introduces a second truth.**
Five thousand events, one balance, five thousand reads. A snapshot brings it to one.
But a snapshot is a stored balance, which is the thing the pattern set out to avoid
— so it must record which event it was taken at *and which code computed it*, and
when that code turns out to have had a bug the snapshot is wrong forever and nothing
throws. `SnapshotTest` shows it happening. The cure is to throw the cache away and
refold, which is cheap precisely because the log kept everything. Treat this as the
rule: **the log is the truth and a snapshot is a cache.**

**Deleting personal data fights the pattern head-on.** A customer has a legal right
to erasure and the log has no delete. "Just remove their events" is the first answer
everybody reaches for, and Act 7 shows what it does: the customer's history is gone
beyond recovery, *and* a snapshot taken earlier still reports their balance, so the
data you deleted is still in the building. The real answers are harder — encrypt the
personal fields in the event and destroy the key, or keep the event's shape and
blank the identity out of it — and both have to be designed in before the first
event is written, not after the first request arrives.

**An event is a schema you version and never migrate.** Somebody added the order id
field in 2023. Every event written before then does not have it and never will,
because you cannot go back and fill it in from information that was not recorded.
Act 8 shows the consequence: the duplicate hunt reports zero duplicates in a stream
that plainly contains two identical awards, and nothing anywhere reports a problem.
Every reader written from then on has to cope with both shapes, forever. In this
project that is `recordsItsOrder()`. In a ten-year-old system it is four shapes and
a comment nobody trusts.

**Most systems do not need this.** A shopping basket, a settings page, a stock
level — if nobody will ever ask how the number got there, keeping the number is the
right design and this pattern is a large bill for nothing. Reach for it where the
history *is* the product: money, loyalty, orders, anything an auditor may ask about.

## Event Sourcing vs. CQRS

These two get treated as one idea constantly, and it means people argue about the
wrong trade-off. Act 9 and `CqrsDistinctionTest` pull them apart by building each
without the other.

**CQRS with no event sourcing.** `OrderHistoryReadModel` is a second model, shaped
for the screen that displays it, updated by the code that handles writes. Writes go
to a current-state row; reads come from here. That is the whole of Command Query
Responsibility Segregation, and there is not an event log anywhere in it. Its own
cost is drift: if the update to the read model is lost, nothing throws and the
customer sees an empty history beside a non-zero balance.

**Event sourcing with no CQRS.** `EventSourcedLoyaltyAccounts` stores events and
answers reads by folding those same events. One model. Nothing to fall behind.

One sentence each, and worth memorising: **CQRS changes where reads come from. Event
sourcing changes what the writes store.**

They appear together often, because a log is an awkward thing to read from directly
and a projection fixes that. But "often together" is not "the same thing", and a
design can have either, both or neither.

## Where You Have Already Seen It

**Git.** A commit is an event. The working tree is a fold. `git log` is `explain()`,
and `git checkout` of an old commit is an as-of query. You cannot change a commit —
`git commit --amend` makes a new one — and the reason force-pushing a shared branch
is rude is the reason the log has no update.

**Your bank statement**, as above.

**Database write-ahead logs.** Postgres writes what it is about to do before doing
it, and recovery after a crash is a fold over that log. The table is the snapshot.

**Accounting, for about five hundred years.** Double-entry bookkeeping is an
append-only log with a fold, and the reason you post a correcting entry rather than
erasing a mistake is that a ledger you can erase is not evidence of anything.

## Try It Yourself

1. Add a `PointsAdjusted` event for support staff correcting a balance by hand,
   with a reason and the name of whoever did it. Notice that the sealed interface
   makes the compiler tell you every place that needs to know.
2. Now use it to repair the double-award bug the *other* way: append a correcting
   event instead of changing the read. Which repair would you rather explain to an
   auditor, and which to a developer? There is a real answer in the javadoc on
   `balanceWithDuplicateAwardsIgnored`, and it is not the one the demo uses.
3. Make `balanceWithDuplicateAwardsIgnored` wrong on purpose by letting the shop
   award points twice for one order legitimately — a promotion, say. The repair rule
   in this project only works because this shop never does that.
4. Add `pointsExpiringBefore(customerId, day)`, answered from the log alone. Then
   try to add it to `CurrentStateLoyaltyAccounts` and stop when you see why you
   cannot.
5. Take a snapshot, then delete the snapshot store's entry for one customer and
   watch every balance stay correct. That is what "the log is the truth" means in
   practice.

## See Also

- [`problem-statement.md`](problem-statement.md) — the row that cannot answer the question
- [`class-diagram.md`](class-diagram.md) — the types, and the class with no balance field
- [`uml-diagram.md`](uml-diagram.md) — the fold, the as-of query and the repair, as sequences
- [`animation.html`](animation.html) — the log filling up and the fold running, in a browser
- [CQRS](../../micro-services-design-patterns/cqrs-pattern) — the pattern this one is constantly confused with
- [Memento](../../behavioural/memento-pattern) — the other pattern about keeping the past, one object rather than one log

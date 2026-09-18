# Problem Statement

## The Scenario

The shop runs a loyalty scheme. One point for every pound spent, points can be
spent on later orders, and anything unused expires after twelve months. It is the
simplest possible scheme and the shop has had it for years.

The database has a table with one row per customer, and the row has a number in
it.

```
customer_id   points
C-4417        140
```

A customer rings up and asks why they have a hundred and forty points.

## Attempt One: Keep The Balance

```java
public void award(String customerId, int points, String orderId, LocalDate on) {
    this.points.merge(customerId, points, Integer::sum);
}
```

That is `CurrentStateLoyaltyAccounts` in this project, and it is not a straw man.
It is correct. Every test in `CurrentStateLoyaltyAccountsTest` passes, the balance
is right after every operation, and it will still be right in five years. Most
loyalty schemes in the world are written exactly like this, and most of them should
be.

Look closely at that one line, though. It is handed an order id and a date, and it
uses neither. They arrive at the method and go no further. The addition happens and
the two facts that would have explained it are dropped on the floor.

## Why That Hurts

**Support cannot answer the question.** Act 1 of the demo asks it and prints the
entire available answer:

```
  balance: 140
  support asks why, and this is the whole answer:
    the row says 140 points. How it got there was never written down.
```

The four things that happened in March were each added to a number and then
forgotten. There is nobody to ask.

**A bug destroys its own evidence.** A release goes out that awards points twice
for one order. Nobody notices for three weeks. The fix is easy; finding the damage
is not. Act 2:

```
    C-5120 = 100 points
    C-5122 = 25 points
    C-5121 = 60 points
  which of those three is wrong, and by how much?
  100 could be a doubled £45 order on top of £10, or one honest £100 order. Both write 100.
```

A doubled forty-five pound order sitting on top of a ten pound one writes `100`.
One honest hundred pound order writes `100`. The two are the same row. The
information needed to tell them apart was overwritten by the bug itself.

**No question about the past can be answered.** What was the balance on the third
of March? What did the customer see when they complained? Which orders earned the
points that just expired? Each of those needs a table somebody thought to create
before the question was asked. The history table, the audit log, the
`points_transactions` table — every one of them exists because somebody predicted a
question, and every question nobody predicted is unanswerable.

## The Question This Project Answers

**If the shop had stored what happened instead of what the total is, which of those
questions would still be hard?**

Not "how do we add an audit log", because an audit log is a second copy that can
disagree with the first. The stronger move is to notice that the balance was never
a fact the shop was told — it is a number the shop worked out — and to store the
facts it *was* told instead.

## The Goal

Build a loyalty account such that:

1. every change is **appended** as an event that names what happened, and nothing
   is ever updated or deleted;
2. the balance is **derived** from those events on demand, and is stored nowhere;
3. support can be shown **why** the balance is 140, one line per event, with the
   running total;
4. the balance **on any past day** can be answered, without anybody having planned
   for the question;
5. a bug found three weeks late can be investigated with a query **written after
   the bug shipped**, against data that was already there;
6. and the repair for that bug changes the **reading** code, appends nothing,
   edits nothing, and deletes nothing.

Point six is the one that surprises people, and it is the point of the pattern.

## And The Bill

This pattern costs more than the others in this category, and the project spends
three of its nine acts on the costs rather than the benefits.

Folding five thousand events to answer one balance reads five thousand events. The
fix is a snapshot, and a snapshot is a second place a balance lives — so a snapshot
written by buggy code stays wrong forever and nothing detects it. A customer with a
legal right to be erased meets a log that is never deleted from, and "just delete
their events" both destroys the history that explained them *and* leaves their
balance sitting in a snapshot. And an event written in 2023 was written by the code
of 2023: a field added later is missing from it permanently, so Act 3's duplicate
hunt finds nothing in a stream that visibly contains two identical awards.

Those four are in the demo, in the tests, and in the video. A pattern taught
without its bill is a sales pitch.

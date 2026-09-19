# Problem Statement

## The scenario

The catalogue's price is read on every page view — constantly — and
changes only a few times a day. A price is two fields that must agree
with each other: an amount and a currency. Change one without the other,
even for an instant, and a reader can see a price that was never true at
any moment the business actually set.

## The naive version, in two parts

### Part one: no synchronization at all

`UnsynchronizedCatalogue` updates its two fields one after the other, with
nothing stopping a reader from reading exactly between the two writes.

```
ONE. No lock at all — the torn read.
  read mid-update: 54.99 GBP
  never a true price: the new amount with the old currency.
```

Fifty-four ninety-nine, in pounds. That price never existed — the amount
belongs to the new price, the currency to the old one, and this project's
interleaving harness makes that happen on every single run, not
occasionally.

### Part two: one mutual-exclusion lock

The obvious fix is correct: one lock around every read and every write,
and the torn read is gone. The cost this exposes is different — two
readers can never possibly conflict with each other, and this lock
cannot tell them apart from a writer, so they queue behind each other for
no reason at all.

```
TWO. One mutual-exclusion lock — correct, but readers queue too.
  8 readers x 50,000 reads each: 13ms
  every reader queued behind every other reader -- two readers
  can never conflict, and this lock cannot tell them apart.
```

## What the pattern must deliver

A lock that lets many readers proceed together and only makes anyone wait
for a writer. It also has to pay several real, honest costs: a queued
writer can still be barged by a fresh reader arriving after it, upgrading
a held read lock to a write lock deadlocks a thread against itself, and —
the finding this project's own measurements produce, unprompted — for a
critical section this cheap to guard, the lock's own bookkeeping can cost
more than the parallelism it buys.

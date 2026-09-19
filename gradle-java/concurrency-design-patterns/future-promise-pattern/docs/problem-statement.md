# Problem Statement

## The scenario

A product page needs three things before it can render: the price, the
stock count, and a review score. Each one is a genuine catalogue lookup —
this project measures each at two hundred milliseconds — and none of the
three depends on either of the other two. Price does not need to know the
stock count to compute itself; the review score does not care what the
price is.

## The naive version

`SequentialProductPage` calls all three, one after another, waiting each
one out fully before starting the next.

```
ONE. Sequential — price, then stock, then rating.
  price £129.99, stock 7, rating 4.6
  rendered in 619ms — three lookups, none depending on the others,
  paid for one after another anyway.
```

Six hundred milliseconds, for work that a moment's thought shows has no
reason to be serial at all.

## What the pattern must deliver

Each lookup submitted at once, returning a **handle to a result that does
not exist yet** — a Future, from the reader's side. The page then waits
for all three together rather than one at a time, so the total cost is
roughly the slowest single lookup, not the sum of all three.

```
TWO. Concurrent — all three submitted at once.
  price £129.99, stock 7, rating 4.6
  rendered in 208ms — roughly one lookup's cost, not three.
```

This project also has to separate the two halves beginners conflate: the
**Future** is what the reader holds and blocks on; the **Promise** is what
the writer holds and completes. And it has to pay the real bill honestly —
a failing task's exception surfaces later and wrapped, not where it was
thrown; a `get()` with no timeout is a hang, not a wait; and cancellation
asks a running task to stop, it does not make it stop.

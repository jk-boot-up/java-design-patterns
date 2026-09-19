# Problem Statement

## The scenario

Placing an order writes an order row, three line rows and three stock
decrements. The third stock update fails.

## The naive version: each object saves itself

Each object writes as it changes. The failure leaves whatever had been
written.

```
ONE. Each object saves itself — the wreckage.
  orders in the database:      1
  order lines in the database: 2 of 3
  stock now: keyboard 8, mouse 9, monitor 10 (was 10, 10, 10)
  nothing knows it is broken, and nothing can undo it.
```

## The second naive version: wrap it in a transaction

Experienced readers reach for this, and it mostly works. The failure rolls
back to nothing.

```
TWO. Wrap it in a transaction — it mostly works.
  orders: 0, lines: 0, stock: keyboard 10, mouse 10, monitor 10
  the cost: the transaction was open for 22 ticks, including every slow check.
```

Its cost is that the transaction, and the locks it holds, stay open for the
whole computation, including the slow check made for each line.

## What this project must deliver

A way to collect the changes, do the slow work first, and write everything in
one short step that either happens completely or not at all.

# Problem Statement

## The scenario

The order worker writes each order as three lines. The shop is shut down for an upgrade while the worker is in the middle of an order.

## The naive version

Shut everything down at once: close the ledger and stop waiting for the worker.

```
  the shop shuts down and closes the ledger while ORD-1 is half written. lines written: [ORD-1 line 1].
  left with an order half written: true. the order has a line 1 and no line 2 or 3.
```

## What this project must deliver

A worker that writes three lines per order and can be asked to stop; a ledger that notes if it was left with an order half written; the abrupt stop shown to leave one; a stop request that finishes the order in progress; a flag that does not wake a sleeping worker and an interrupt that does; cleanup in a finally block; a worker that ignores the request, with a time limit on phase two; five orders left pending; and a plain verdict.

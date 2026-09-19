# Problem Statement

## The scenario

A partner sends a file of order lines: customer, item and quantity. Each line must be parsed, checked, priced, taxed and turned into a confirmation.

## The naive version

One method loops over the lines and does all five jobs inside the loop.

```
  6 lines in, 3 out: [ada: 2 x MUG-BLUE = £19.20, ben: 1 x ESP-001 = £360.00, fay: 3 x TEA-050 = £28.80].
  5 separate jobs in one loop. the six lines came in, and the three that were dropped left no trace of why.
```

## What this project must deliver

A `Filter` that may pass an item on or drop it with a reason; a `Pipeline` that joins filters and runs items through one at a time; the same import as five small steps; a swapped tax step and an added step; rejected lines reported; streaming against stage-by-stage memory; the shape problem of untyped items; and a plain verdict.

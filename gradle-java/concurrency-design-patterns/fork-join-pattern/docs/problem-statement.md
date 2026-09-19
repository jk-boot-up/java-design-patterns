# Problem Statement

## The scenario

The day's report adds up a hundred thousand order totals, and the machine has several processors that are idle while one loop does the work.

## The naive version

One loop adds every total, on one thread.

```
  adding up 100000 order totals in a loop: 499838000 pence, on one thread.
```

## What this project must deliver

A recursive task that adds a slice directly when it is small and otherwise forks half and joins; the leaves and tasks counted and matched to a shape worked out with no threads; a pool of exactly four workers held at a gate to show four pieces at once; four thresholds compared; the ceiling one large piece puts on the speedup; work that waits shown to gain nothing; and a plain verdict.

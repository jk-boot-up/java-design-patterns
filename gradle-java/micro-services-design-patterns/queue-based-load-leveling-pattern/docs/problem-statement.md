# Problem Statement

## The scenario

When a sale starts, a hundred orders arrive in the same moment. The order service can process ten a tick. The rest of the day it is nearly idle.

## The naive version

Orders go straight to the order service. Whatever it cannot take at that moment is refused.

```
  100 orders arrive at once. the order service handles 10 a tick. processed: 10, refused: 90.
  ninety customers were told to try again, on the busiest moment the shop had.
```

## What this project must deliver

A model in ticks, with exact counts; a burst refused and the same burst queued; the waiting a queue costs; an unbounded queue growing without limit against a bounded one refusing; a faster worker against a slower one; orders lost when an in-memory queue stops; and a plain verdict.

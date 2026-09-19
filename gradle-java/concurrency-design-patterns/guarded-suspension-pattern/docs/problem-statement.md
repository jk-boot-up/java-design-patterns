# Problem Statement

## The scenario

Orders arrive in an inbox at unpredictable times. Pickers take them out, and must wait when there are none.

## The naive version

The picker asks the inbox again and again whether an order has come.

```
  the picker asks whether an order has come, over and over. no order has come, and it has already asked more than a million times: true.
  it took [ORD-1] when it arrived. the whole time it kept a processor busy doing nothing.
```

## What this project must deliver

Five kinds of inbox: one that spins, one that waits with a guard in a loop, one with the guard as an if, one that waits without looking first, and a limited wait; thread states polled to WAITING so every result is exact; the wake-ups counted; and a plain verdict.

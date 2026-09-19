# Problem Statement

## The scenario

When an order is placed, a receipt must be sent. In a hundred ticks, only three orders arrive, and now and then five arrive at once.

## The naive version

Keep a server running all the time, in case an order comes.

```
  100 ticks, 3 orders. the bill: 200. paid for 100 ticks, used for 3 orders.
```

## What this project must deliver

A platform simulation on a counted clock: instances started when a call needs one, kept warm, and dropped after an idle timeout; an always-on server with a price per tick; counts of invocations, cold starts and extra wait; instance memory against an outside store; a busy load that costs more than the server; and a time limit that stops long work.

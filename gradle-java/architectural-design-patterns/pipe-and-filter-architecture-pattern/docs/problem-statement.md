# Problem Statement

## The scenario

Every order is parsed, priced and packed. Parsing takes one tick, pricing three, and packing one. An order arrives every tick.

## The naive version

One worker does all three jobs for one order, and only then starts the next.

```
  parse 1 tick, price 3, pack 1: 5 ticks for each order, one at a time. an order arrives every tick.
  after 30 ticks, orders done: 5.
```

## What this project must deliver

A simulation in whole ticks, with no clock: stages with a cost, workers and a waiting line; one big step; three overlapping stages; queue sizes showing the bottleneck; a widened price stage; waiting lines with a limit, and the refusals at the door; and a crash that loses the orders in flight.

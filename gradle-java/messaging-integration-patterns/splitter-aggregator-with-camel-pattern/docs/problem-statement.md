# Problem Statement

## The scenario

A customer's basket has three lines, and the three products sit in three different warehouses: Leeds, Reading and Glasgow. One worker taking the whole basket walks all three, one line after another, while the other two warehouses stand idle. The basket comes to £283.42 either way; the only question is how long the customer waits for it.

## The naive version

One message for the whole order, one worker, one line at a time.

```
  order ORD-4471 has 3 lines, held in 3 warehouses: Leeds, Reading, Glasgow.
  one picker walks all of them, one line after another: 3 steps of work on 1 thread, and the basket comes to £283.42.
  while that picker walks, the other warehouses stand idle.
```

## What the partner project already did

[Splitter and Aggregator](../../splitter-aggregator-pattern) built the whole mechanism by hand: a splitter that numbers every piece, an aggregator that keys on the order number, duplicates counted once, two orders that never mix, and a partial result at a timeout. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. Its clock was a field the demo could push forward thirty minutes in a single statement, and its completion test was written into the method that accepted a piece. Both of those are decisions a real aggregator makes you take.

## What this project must deliver

The same order, split and gathered by Apache Camel. A completion condition supplied as a separate thing, and an act showing that an aggregator with a count and nothing else holds an unfinished order for ever. A real deadline, with a background checker watching the clock, and an order that is given up on without anybody asking. A warehouse that is genuinely closed, so a message stops on its path and nothing downstream is told. The moment Camel's completion-by-size counts a repeated message as progress and declares an order finished with a line missing. And the memory a thousand unfinished orders hold, which a restart would throw away.

Every figure printed is Camel's own, and two runs back to back print the same thing.

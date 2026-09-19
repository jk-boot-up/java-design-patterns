# Splitter and Aggregator, Explained

## The pattern in one sentence

A splitter breaks one message into several, each carrying an id and its place, and an aggregator collects the pieces by that id and puts them back together as one.

## The six acts

### One Message, One Picker

An order of three lines is picked by one person, one line after another: three steps in a row, while the other pickers stand idle.

```
  an order of 3 lines is picked by one person, one line after another: 3 steps of work, in a row.
  the aisles are far apart, and the other pickers stand idle.
```

### Split It

The order becomes three parts, each with the order's id, its own number, and how many there are in all. That is what lets them be put back.

```
  ORD-1 part 1 of 3: 2 x MUG-BLUE (aisle 3)
  ORD-1 part 2 of 3: 1 x ESP-001 (aisle 9)
  ORD-1 part 3 of 3: 5 x TEA-050 (aisle 1)
  each part carries the order's id, and its place. that is what lets it be put back.
```

### The Parts Finish In Any Order

Suppose the pickers finish in the order three, one, two. Nothing guarantees the parts come back in the order they went.

```
  suppose the three pickers finish in the order: 3 1 2.
  nothing guarantees they come back in the order they went.
```

### Gather Them By The Id

Part three arrives, then part one, and the aggregator waits. Part two arrives, and the order is complete, in its original line order.

```
  part 3 arrives. waiting for the rest.
  part 1 arrives. waiting for the rest.
  part 2 arrives. complete: [2 x MUG-BLUE (aisle 3), 1 x ESP-001 (aisle 9), 5 x TEA-050 (aisle 1)].
  the order came back together, in its original line order, from parts that arrived out of order.
```

### A Part Never Arrives

Parts one and three arrive, and part two's picker has gone home. After twenty nine minutes nothing has expired. After thirty, the aggregator gives up, with two of three lines and part two named as missing.

```
  parts 1 and 3 arrive. part 2's picker has gone home. open orders: 1.
  after 29 minutes: expired 0.
  after 30 minutes the aggregator gives up: 2 of 3 lines, missing part [2], complete: false.
  without a timeout it would wait for ever, and the customer would too.
```

### The Bill

A thousand orders each missing one part means a thousand orders held in memory. A part delivered twice is counted once. And two orders with the same id would be mixed into one, so the id must be unique.

```
  1000 orders each missing one part: 1000 orders held in memory, waiting.
  a part delivered twice: counted once, and 1 duplicate noted. without that, an order could complete with a line twice.
  and two orders with the same id would be mixed into one. the id that ties the parts together has to be unique.
```

## The verdict

Use a splitter and aggregator when one message contains parts that can be worked on separately, and the work is slow enough that doing it in parallel pays. Number every part and carry the id and the total. Aggregate with a timeout, drop duplicates, and decide what to do with a partial result. Watch the number of open aggregations.

## How to recognise this in code you did not write

- A message that carries a `correlationId`, a `sequenceNumber` and a `sequenceSize`.
- Spring Integration's `splitter` and `aggregator`, Camel's `split` and `aggregate`.
- A map keyed by an id, holding what has arrived so far.
- A timeout on collecting the results of a batch.

## Where you have already met this

Batch jobs that fan out over records, map-reduce, and any order system that sends each line to a different picker or supplier.

## When this is too much

If the parts are quick, or depend on each other, splitting is overhead. If order matters between the parts, an aggregator needs more than the parts.

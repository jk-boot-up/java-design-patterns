# Problem Statement

## The scenario

An order has three lines, in aisles far apart. Picking them one after another takes three steps in a row, while other pickers stand idle.

## The naive version

One message for the whole order, picked by one person, one line after another.

```
  an order of 3 lines is picked by one person, one line after another: 3 steps of work, in a row.
  the aisles are far apart, and the other pickers stand idle.
```

## What this project must deliver

A splitter that numbers each part and carries the order id; an aggregator that collects by id, puts parts back in line order, and counts a duplicate once; two interleaved orders that do not mix; an order with a missing part emitted as partial at a timeout on a controlled clock; the memory a thousand incomplete orders hold; and a plain verdict.

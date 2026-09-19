# Problem Statement

## The scenario

Two clerks open the same product. One raises the price. The other counts the stock. Each edits for a while, then saves the whole row.

## The naive version

Each clerk reads the row, changes a field, and writes the whole row back. Whoever saves last wins.

```
  clerk A raises the price to 12.00 and saves. clerk B counts 40 in stock and saves.
  the row now: price £10.00, stock 40. clerk A's price has vanished, and no error was raised.
```

## What this project must deliver

A store with no lock that loses an update silently; a store with a version per row that refuses the stale save; a retry that reloads and reapplies; a conflict on different fields shown honestly; a busy row where nine of ten saves are repeated; a long edit discarded at the end; and a plain verdict.

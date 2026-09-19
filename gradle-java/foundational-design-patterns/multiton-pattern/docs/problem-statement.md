# Problem Statement

## The scenario

The shop has a warehouse in the UK, one in the EU and one in the US. Many parts of the shop reserve stock, and all of them must see the same stock for a region.

## The naive version

Create a new warehouse object whenever a part of the shop needs one.

```
  two callers each made a UK warehouse. same object: false. A has stock 90, B has 100.
  the shop now believes two different things about one warehouse.
```

## What this project must deliver

A warehouse with a private constructor and a map from region to instance; a fixed set of regions; a naive look-then-create that makes two under a race, forced with a barrier; an atomic create-if-absent that makes one under eight threads; and a leak of state from one test to the next.

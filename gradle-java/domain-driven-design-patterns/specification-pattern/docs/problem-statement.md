# Problem Statement

## The scenario

Three features of the online store need the same idea: cheap and available. The search page shows such products, a promotion is offered on them, and they ship free.

## The naive version

Each feature writes the condition where it needs it. Three copies, written at different times by different people.

```
  search page:   [MUG-BLUE, TEA-050]
  promotion:     [MUG-BLUE, MUG-RED, MUG-OLD, TEA-050]
  free shipping: [MUG-BLUE, TEA-050]
  the promotion includes MUG-RED at exactly 10.00 and MUG-OLD, which is discontinued. nobody meant that.
```

## What this project must deliver

A `Specification` that is satisfied or not, describes itself, says which parts a candidate fails, and combines with and, or and not; one named rule used by all three features; the drift of the plain version shown for real; the cost of filtering in memory; and a plain verdict.

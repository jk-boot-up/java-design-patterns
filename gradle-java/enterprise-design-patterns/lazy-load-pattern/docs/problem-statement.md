# Problem Statement

## The scenario

Load one order to show it on a page.

## The naive version: eager loading

Load everything reachable. An order refers to its customer, the customer
to their other orders, those to their lines, the lines to products, and the
products to categories.

```
ONE. Eager loading — one order, everything reachable.
  loaded one order. objects created: 37
  database operations: 26
```

One order asked for, thirty-seven objects created, twenty-six database
operations. There is no cycle in that graph and no obvious mistake.

## What this project must deliver

A way to load the order now and the rest only when it is asked for. And it
must not soften the bill: N+1, a field access that is now I/O, and a load
that fails after its session has gone.

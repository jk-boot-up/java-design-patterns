# Problem Statement

## Read the partner first

This project assumes [Lazy Load](../lazy-load-pattern), which builds four lazy
variants by hand and shows N+1 and a closed session failing at the point of use.
Nothing here is lost by skipping the framework, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's store: five customers, twenty orders, four lines per order, twelve
products, four categories. An order refers to its customer and to its lines. Both
are declared `FetchType.LAZY`.

## The failure this project exists to show

Load an order, close the session, then ask for the customer's name.

```
ONE. Load an order, close the session, use the customer.
  the order loaded fine: order 1
  asking for the customer's name threw LazyInitializationException:
  Could not initialize proxy [...Customer#1] - no session
  the failure is where it was used, not where it was loaded.
```

This is one of the most searched Java errors there is, and it is explained here
from its mechanism, not worked around.

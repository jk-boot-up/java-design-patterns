# Strangler Fig, Explained

## The pattern in one sentence

Replace a system by growing the new one around the old, one capability at a time, behind a router that can send
each capability to either.

## An analogy, and then back to the shop

A strangler fig starts as a seed high in a tree. It sends roots down the trunk, and grows around the host a bit
at a time. For years the tree and the fig are both alive, and the tree is still doing its job. One day the fig
is complete, and the old tree inside it is gone. At no point was there a moment when the forest had no tree.

## How it works

A `Router` sits in front of the legacy checkout. Each of the four capabilities, pricing, stock, payment and
email, has its own switch: `LEGACY`, `NEW`, or `SHADOW`.

```
TWO. The pattern: a router, and one switch per capability.
  every capability starts on the legacy checkout: PRICING=LEGACY STOCK=LEGACY PAYMENT=LEGACY EMAIL=LEGACY
  pricing moves first: PRICING=NEW STOCK=LEGACY PAYMENT=LEGACY EMAIL=LEGACY
```

The customer saw no cutover. The checkout never stopped.

## Shadow reads: move on evidence, not on hope

In `SHADOW` mode a capability is served by legacy, the new implementation is called too, and any difference is
recorded. The customer only ever gets the legacy answer.

```
THREE. Shadow reads: move on evidence, not on hope.
  201 orders served by legacy, and priced by the new code as well, and compared.
  they disagreed on 29. the first three:
    order 7: legacy ... vatPence=1294 ..., new ... vatPence=1293 ...
```

The rewrite was written from the business rules as people described them, and it differs from what the legacy
code has actually charged for years, in two ways: VAT is rounded per line against once, and delivery is free from
fifty pounds against over fifty pounds. Shadow reads found both **before any customer paid a penny differently**.
After the team decides to reproduce legacy exactly, the shadow finds 0 differences in 201, and pricing can move.

## Rollback, one capability at a time

```
FOUR. Rollback: one capability, not the whole checkout.
  payment is on the new code, and misbehaves on a large order. succeeded: false, charge: null.
  one switch flipped: payment alone goes back to legacy. succeeded: true, charge: L-1.
  routes now: PRICING=NEW STOCK=LEGACY PAYMENT=LEGACY EMAIL=LEGACY. pricing stayed on the new code the whole time.
```

## The bill

**Two systems are live for months, and both must be maintained.** Every business rule that changes while both are
live is changed twice.

**Data has to stay consistent across both.**

```
FIVE. The bill: two systems, and two versions of the truth.
  the new service says 395 on hand. the legacy table, which its reports and its invoices still read, says 400.
```

Two tables claim to be the truth. Someone must decide which, and keep them in step until legacy is gone.

**And the failure that actually happens: the migration stalls half-finished.** Budget moves elsewhere, and the
organisation lives with two checkouts forever.

```
SIX. The failure mode that actually happens: the migration stalls.
  quarter   stalled: moved  running  total     finished: moved  running  total
  ...
  six quarters, cumulative: stalled 760, finished 645.
  the stalled state costs 115 a quarter, more than all legacy (100) and more than all new (60).
```

That is a **stated cost model**, not a measurement: all legacy costs 100 a quarter, all new costs 60, and running both
adds a fixed 35. Only the shape matters. Two checkouts, forever, is worse than either endpoint, and it is the most
likely outcome, and nobody warns you.

## The verdict

Use it, but treat the end date and the decommissioning of legacy as part of the migration, not a later job. A
strangler you do not finish is worse than a big bang you should have avoided, and worse than not starting.

## How to recognise this in code you did not write

- A gateway or proxy with routes sending one path to an old service and another to a new one.
- A feature flag per capability, with names like `use-new-pricing`.
- Two implementations of the same interface, and a selector between them, with a ticket to delete one.
- A `Legacy` package that has been "temporary" for years.

## What this simulation does not show

Tier 1 is a model in one JVM. It does not show two real deployments, a real network between the router and the
systems, real data migration (moving rows, not just comparing two maps), or the organisational part, which is
where most strangler migrations actually stall: priorities, budgets and people. The cost figures are assumptions
chosen to show a shape.

## Where you have already met this

Every "we are moving to the new platform, one team at a time" migration, and every `/api/v2` next to a `/api/v1`.

## When this is too much

For a system small enough to rewrite in a few weeks, the seam and the router cost more than they save.

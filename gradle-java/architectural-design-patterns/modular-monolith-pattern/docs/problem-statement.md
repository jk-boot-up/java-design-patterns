# Problem Statement

## The scenario

The online store is one Java program in which checkout, the catalogue and
payments share every table.

## The naive version

`MudCheckout` writes the stock and payment tables directly. The catalogue's
rule that stock never goes below zero is skipped, and one kettle is sold twice.

## What this project must deliver

- The shared-table failure shown: stock -1 after two orders for one kettle.
- Three modules with front doors, where the catalogue's rule holds and a refused order is not charged.
- A boundary check over the real source: 0 violations, and a planted import caught.
- Payments swapped for a remote version with 0 lines changed in orders.
- The costs named: one build, one deployment, one process.
- Every printed result asserted by a test.

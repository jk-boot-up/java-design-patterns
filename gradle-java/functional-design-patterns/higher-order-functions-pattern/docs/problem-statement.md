# Problem Statement

## The scenario

The catalogue answers questions like "under 10", "in stock" and "mugs".

## The naive version

Each question had its own copy of the same loop, differing only in the test.

## What this project must deliver

- Three copied loops.
- One `filter` taking a `Predicate`.
- Functions returning predicates, combined with `and` and `negate`.
- Price rules joined with `andThen`, where order matters.
- Advice on naming.
- Every printed result asserted by a test.

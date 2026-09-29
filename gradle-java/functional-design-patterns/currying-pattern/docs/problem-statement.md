# Problem Statement

## The scenario

The shipping price depends on zone, service and weight, and the EU warehouse
always uses the same zone and service.

## The naive version

Every call repeats the unchanging arguments before the one that changes.

## What this project must deliver

- Repeated arguments in a three-argument function.
- A curried version fixing zone and service.
- Ready-made functions per zone, used with `map`.
- A generic `curry` helper and the argument-order trap.
- A plain lambda as the simpler alternative.
- Every printed result asserted by a test.

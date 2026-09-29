# Problem Statement

## The scenario

Orders are fulfilled in three steps: reserve stock, take payment, ship.
Some steps fail and must be undone or retried elsewhere.

## The naive version

`Chained` passes each order along a line. A declined card stops the line, the
reserved stock is never released, and nobody knows where the order is.

## What this project must deliver

- The chain shown leaking stock on a declined card.
- A process manager taking an order through every step.
- A branch to a partner warehouse.
- A failure path that releases stock and emails the customer.
- The status of every order in one place, and the cost of a central brain.
- Every printed result asserted by a test.

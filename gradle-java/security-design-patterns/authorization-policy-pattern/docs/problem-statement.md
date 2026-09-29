# Problem Statement

## The scenario

The store's view, cancel and refund endpoints each checked access in their
own code.

## The naive version

Scattered checks drift: one forgot ownership and exposed other customers'
orders, another forgot the refund limit.

## What this project must deliver

- Scattered checks with two real holes.
- A role-based policy, and what roles cannot express.
- An attribute-based policy with ownership and limits.
- Deny by default for actions with no rule.
- An audit log of every decision with its reason.
- Every printed result asserted by a test.

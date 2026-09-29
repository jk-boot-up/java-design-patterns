# Problem Statement

## The scenario

The shop's view, refund and export endpoints must allow different things to
customers, support and admins.

## The naive version

Checks written separately in each endpoint drift, and one forgotten check
exposes other customers' orders.

## What this project must deliver

- An endpoint that forgot the owner check.
- A role-only URL rule, and its limit.
- @PreAuthorize rules for ownership and refund limits.
- Deny by default with denyAll().
- Authorization events, and two framework traps.
- Every printed result asserted by a test.

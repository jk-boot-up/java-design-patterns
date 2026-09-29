# Problem Statement

## The scenario

Customers can also become marketplace sellers and affiliates, and can stop
being either.

## The naive version

`SellingCustomer extends Customer`. Becoming a seller means a new object that
loses the order history, and every combination of kinds needs its own class:
seven for three kinds.

## What this project must deliver

- The subclass approach shown losing 12 orders and needing 7 classes.
- One account playing buyer and seller roles, keeping its orders.
- Roles with their own behaviour: listing, commission.
- A role removed while the others and the identity remain.
- Every printed result asserted by a test.

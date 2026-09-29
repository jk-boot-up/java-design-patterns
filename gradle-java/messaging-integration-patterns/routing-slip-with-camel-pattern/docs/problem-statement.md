# Problem Statement

## The scenario

Orders need different sets of steps: validate, age check, customs, charge,
gift wrap and pack.

## The naive version

One fixed pipeline makes every order visit every step, and every step check
whether it applies.

## What this project must deliver

- A fixed pipeline with wasted visits.
- A slip written once per order.
- Camel's `routingSlip()` following it.
- A new step added as one rule.
- The fixed-at-start limit, and `dynamicRouter()` deciding on the way.
- Every printed result asserted by a test.

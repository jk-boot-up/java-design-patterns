# Problem Statement

## The scenario

Checkout sends charge and refund messages to the payment service, and someone
needs to see them to investigate a disputed refund.

## The naive version

Logging typed into the payment service's charge path misses refunds and
records full card numbers.

## What this project must deliver

- Hand-added logging shown missing a message and exposing cards.
- An audit tap copying every message with masked cards.
- A tap detached with no change to the flow.
- A second tap feeding a sales meter.
- A slow tap measured, and fixed with its own thread.
- Every printed result asserted by a test.

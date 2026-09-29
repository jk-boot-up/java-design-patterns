# Problem Statement

## The scenario

Checkout has four steps; the payment library throws on a declined card.

## The naive version

Exceptions that nothing forces the caller to handle become error pages.

## What this project must deliver

- A throwing library.
- An Either chain with flatMap.
- Try moving an exception onto the failure track.
- map for a plain step and orElse for recovery.
- Validation collecting every problem.
- Every printed result asserted by a test.

# Problem Statement

## The scenario

Checkout tests use a stub of the payment service, and the payment team
releases independently.

## The naive version

A hand-written stub keeps the old behaviour after the real service changes,
so tests pass while production fails.

## What this project must deliver

- A hand-written stub drifting from the real service.
- A contract of three interactions.
- A stub generated from the contract.
- The real service verified against the same contract.
- A strict stub refusing unlisted requests.
- Every printed result asserted by a test.

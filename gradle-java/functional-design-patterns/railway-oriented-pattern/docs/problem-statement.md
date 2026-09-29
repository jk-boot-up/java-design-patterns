# Problem Statement

## The scenario

Checkout has four steps, each of which can fail for a business reason.

## The naive version

Each step threw its own exception, and a new exception type slipped past the
controller as a 500 error.

## What this project must deliver

- An uncaught exception turning a declined card into a 500.
- A sealed `Result` type with `flatMap`, `map`, `recover` and `fold`.
- A checkout chain that skips steps after a failure.
- A plain tax step and a back-order recovery.
- The first-failure-only limit.
- Every printed result asserted by a test.

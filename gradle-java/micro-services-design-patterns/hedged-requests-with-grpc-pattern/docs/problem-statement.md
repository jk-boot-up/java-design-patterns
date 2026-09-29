# Problem Statement

## The scenario

The product page calls the price service over gRPC; one call in thirty-three
takes a second.

## The naive version

Waiting on whichever attempt was sent makes the slowest pages take a second.

## What this project must deliver

- The slow tail measured over real gRPC calls.
- A hedging policy in the service config.
- Losing attempts cancelled, seen on the server.
- Hedging at once doubling the load.
- A non-idempotent call hedged by mistake.
- Every printed result asserted by a test.

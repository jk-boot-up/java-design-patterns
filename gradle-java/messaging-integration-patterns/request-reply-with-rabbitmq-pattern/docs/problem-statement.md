# Problem Statement

## The scenario

Checkout and the phone app ask the inventory service to reserve items over a
broker, and replies can come back out of order.

## The naive version

Taking replies in arrival order pairs answers with the wrong questions.

## What this project must deliver

- Mismatched replies without IDs.
- Correlation IDs matching every reply.
- Return addresses, including direct reply-to.
- Twenty requests in flight.
- A timed-out request expiring in the queue.
- Every printed result asserted by a test, skipped without Docker.

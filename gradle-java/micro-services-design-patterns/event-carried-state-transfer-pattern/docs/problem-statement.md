# Problem Statement

## The scenario

Shipping prints labels; the customer service owns the addresses and sends a
thin "customer changed" event.

## The naive version

Shipping calls the customer service for every label, so it stops working
whenever the customer service is down.

## What this project must deliver

- Thin events with a call-back, and their dependency on the owner.
- Events that carry the address, and a local copy in shipping.
- The stale window of eventual consistency.
- Out-of-order events fixed with version numbers.
- The cost of copies named.
- Every printed result asserted by a test.

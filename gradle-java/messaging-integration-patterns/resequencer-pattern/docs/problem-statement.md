# Problem Statement

## The scenario

Order status updates pass through parallel workers and reach the order page
out of order.

## The naive version

The page applies updates as they arrive, showing packed before paid and ending
on shipped for a delivered parcel.

## What this project must deliver

- Wrong statuses shown when applying in arrival order.
- A resequencer releasing updates in sequence.
- A trace of holding and releasing.
- Independent sequences per order.
- A lost update and a limit that skips the gap.
- Every printed result asserted by a test.

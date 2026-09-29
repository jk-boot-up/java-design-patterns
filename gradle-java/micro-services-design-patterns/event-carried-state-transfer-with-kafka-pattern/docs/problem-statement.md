# Problem Statement

## The scenario

Shipping prints labels; the customer service owns the addresses.

## The naive version

Thin events force a call back for every label, and labels stop when the owner
is down.

## What this project must deliver

- Thin events and call-backs failing with the owner down.
- Address events on a compacted, keyed topic, and a local copy.
- A new copy built from the topic, and the lag of an old one.
- Order kept by key within a partition.
- A tombstone deleting a customer from copies.
- Every printed result asserted by a test, skipped without Docker.

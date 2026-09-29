# Problem Statement

## The scenario

Catalog, cart and orders each checked the sign-in token with their own copy
of the code.

## The naive version

Three copies drift apart: the orders service never checked expiry, so an
expired sign-in still worked there.

## What this project must deliver

- Three services checking tokens themselves, one wrongly.
- A gateway that checks sign-in once for all.
- Per-customer rate limiting at the gateway.
- Gzip compression at the gateway.
- The side-door risk shown, and the single point named.
- Every printed result asserted by a test.

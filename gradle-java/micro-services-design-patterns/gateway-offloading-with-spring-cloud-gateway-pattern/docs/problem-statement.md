# Problem Statement

## The scenario

Catalog, cart and orders each checked sign-in tokens with their own code.

## The naive version

Three copies drift apart; the orders copy forgot expiry.

## What this project must deliver

- Three real services checking tokens themselves, one wrongly.
- A Spring Cloud Gateway global filter checking once.
- A per-customer rate limit at the gateway.
- Response compression by server properties.
- A stripped spoof, and the side door.
- Every printed result asserted by a test.

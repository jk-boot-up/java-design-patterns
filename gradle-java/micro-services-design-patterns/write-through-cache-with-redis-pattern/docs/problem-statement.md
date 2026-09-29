# Problem Statement

## The scenario

Product pages read prices from a cache; checkout reads the database.

## The naive version

Writing prices straight into the database leaves the cache showing old prices.

## What this project must deliver

- A write around the cache, and two prices.
- Write-through to PostgreSQL and a shared Redis.
- Reads counted by Redis's own statistics.
- A refused database write, and an unreachable Redis.
- The cost of every write.
- Every printed result asserted by a test, skipped without Docker.

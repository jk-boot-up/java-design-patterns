# Problem Statement

## The scenario

A supplier sends a thousand products a second; the search indexer handles a
hundred.

## The naive version

Buffering everything the indexer has not reached means memory grows by nine
hundred products a second until the service falls over.

## What this project must deliver

- An unbounded buffer growing without limit.
- A bounded buffer that makes the producer wait.
- A pull-based subscriber using `java.util.concurrent.Flow`.
- A conflator that keeps only the latest update.
- The costs named: slower producers and lost data.
- Every printed result asserted by a test.

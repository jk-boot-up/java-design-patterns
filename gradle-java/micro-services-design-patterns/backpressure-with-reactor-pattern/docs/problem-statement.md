# Problem Statement

## The scenario

A supplier feed sends products far faster than the search indexer can index
them.

## The naive version

Pushing regardless of demand piles products up in memory until something
breaks.

## What this project must deliver

- A source ignoring demand, stopped by Reactor.
- A subscriber requesting ten at a time.
- `limitRate` and its top-up requests.
- `onBackpressureLatest` for stock levels.
- The choice every source must make.
- Every printed result asserted by a test.

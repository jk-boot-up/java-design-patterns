# Problem Statement

## The scenario

The product page asks the price service for each price. Most answers take 20
ms, but one call in thirty-three hits a paused replica and takes a second.

## The naive version

Waiting for whichever replica was asked means the slowest one percent of
pages wait a whole second.

## What this project must deliver

- The slow tail measured: median against 99th percentile.
- Hedging after a delay, with its small extra load.
- Hedging at once, with its doubled load.
- A real race between threads, with the loser cancelled.
- The limits named: only repeatable calls, and a cap on hedges.
- Every printed result asserted by a test.

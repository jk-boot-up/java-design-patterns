# Problem Statement

## The scenario

Pickers work through orders ten a minute; same-day orders must reach the van
by 9:05.

## The naive version

A first-in-first-out queue makes same-day orders wait behind every standard
order, and they miss the van.

## What this project must deliver

- Same-day orders missing the van with a FIFO queue.
- A priority queue getting them picked in the first minute.
- The same result with a thousand standard orders queued.
- Starvation shown, and fixed with a reserved share.
- The abuse risk named.
- Every printed result asserted by a test.

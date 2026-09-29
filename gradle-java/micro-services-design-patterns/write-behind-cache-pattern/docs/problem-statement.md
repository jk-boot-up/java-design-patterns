# Problem Statement

## The scenario

Customers change their carts many times a minute, and every change was saved
to the database before the page answered.

## The naive version

`WriteThroughStore` writes every change at once: thirty writes for thirty
clicks, twenty milliseconds of waiting on each, and most of the writes
overwritten a moment later.

## What this project must deliver

- The cost of writing every change: 30 writes, 600 ms of waiting.
- Write-behind with a flush that writes each changed cart once: 0 ms waiting, 3 writes.
- A database outage survived, with carts kept dirty and written when it returns.
- The crash window shown: 3 changes lost.
- The database shown behind the cache, and the rule for what never to write behind.
- Every printed number asserted by a test.

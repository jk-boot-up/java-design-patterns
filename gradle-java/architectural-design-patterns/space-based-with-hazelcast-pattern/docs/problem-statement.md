# Problem Statement

## The scenario

A flash sale sends hundreds of kettle orders a second to a database that
writes one at a time.

## The naive version

Every order waits for the database, and more app servers only queue for it.

## What this project must deliver

- A database bottleneck measured.
- Three real Hazelcast members holding the stock.
- One owner per key instead of copies.
- Write-behind coalescing updates.
- An atomic last-kettle sale and a crash survived.
- Every printed result asserted by a test.

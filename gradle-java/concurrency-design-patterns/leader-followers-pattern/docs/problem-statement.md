# Problem Statement

## The scenario

An order service receives a stream of order messages for a pool of threads to
handle.

## The naive version

`DispatcherWorkers` has a dispatcher thread that passes every message across a
second queue to a worker: twenty hand-offs, and one thread that never handles
an order.

## What this project must deliver

- Hand-offs counted for a dispatcher and workers.
- A leader/followers pool with leadership as a lock.
- Proof that only one thread waits on the source at a time.
- Every order handled by the thread that received it.
- The ordering cost shown with place and cancel.
- Every printed result asserted by a test.

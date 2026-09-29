# Problem Statement

## The scenario

Orders arrive in bursts on an event thread; each needs 100 ms of blocking
work.

## The naive version

`EventThreadOnly` does the blocking work on the event thread, so it cannot
accept the next order until the previous one is finished.

## What this project must deliver

- The acceptance delay shown with blocking work on the event thread.
- An async half that only queues, accepting every order within 0.1 s.
- A sync half of plain worker threads finishing the burst in under 1 s.
- A bounded queue turning orders away when workers stall.
- Every printed result asserted by a test.

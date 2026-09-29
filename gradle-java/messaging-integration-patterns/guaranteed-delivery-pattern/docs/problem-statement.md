# Problem Statement

## The scenario

Order confirmation emails wait in a queue in front of a slow email provider.

## The naive version

`MemoryQueue` holds them in memory, so a restart loses every waiting email.

## What this project must deliver

- Ten emails lost on a restart with an in-memory queue.
- A journal forcing each message to disk before accepting it.
- Acknowledgements so only undelivered messages are replayed.
- A duplicate caused by a crash before the acknowledgement.
- The disk cost counted.
- Every printed result asserted by a test, with real files.

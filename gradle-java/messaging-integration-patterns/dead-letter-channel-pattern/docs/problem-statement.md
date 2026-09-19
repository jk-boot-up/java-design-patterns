# Problem Statement

## The scenario

Orders are processed one at a time from a channel. Order two arrives garbled, and the handler can never read it. Orders three and four are fine.

## The naive version

Retry the failing message until it works. If it never works, keep retrying.

```
  four orders, one garbled. handled: [ORD-1]. still waiting: 3. attempts made: 11.
  the garbled order is at the head of the line and will never succeed. orders 3 and 4 are stuck behind it.
```

## What this project must deliver

A worker that retries a failing message up to a limit and then moves it to a dead letter channel with its attempts and reason; a poison message that blocks the line without one; a transient failure that recovers and is not dead-lettered; a replay after a fix that does not restore order; forty orders half of which are lost quietly; and a plain verdict.

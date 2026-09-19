# Session Guide — Pessimistic Offline Lock Pattern

A 60-minute session built around one question: what does it cost to prevent a clash instead of detecting it?

## Learning Objectives

1. Say how a lock prevents a lost update.
2. Explain why a lock needs an expiry.
3. Explain a deadlock and the fixed-order fix.
4. Say how much to lock.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | The scenario and the naive version |
| 0:10–0:30 | The pattern |
| 0:30–0:45 | The bill |
| 0:45–0:52 | The verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/pessimistic-offline-lock-pattern
./gradlew -q run
```

Act one: who was told who holds the lock? Act two: what did B see after A let go? Act three: how many refusals? Act four: what happened to A's late save? Act five: which order avoided the deadlock? Act six: which lock let both work?

## Exercises

1. Add a renew method and decide how many times it may be used.
2. Add a queue, so B is told when the lock is free.
3. Write a test that finds the deadlock by two threads.

Close with the verdict: lock the smallest thing, always expire, take locks in a fixed order, and refuse late writes.

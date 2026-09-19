# Session Guide — Active Object with Spring Pattern

A 60-minute session built around one question: what makes an @Async bean an active object, and what breaks it?

## Learning Objectives

1. Explain why a one-thread executor removes the need for a lock.
2. Say what the mailbox is, and how to bound it.
3. Explain how a call on `this` loses an update.
4. Explain why reads must be messages too.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:25 | The first acts |
| 0:25–0:40 | The failures of its own |
| 0:40–0:52 | The cost |
| 0:52–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd concurrency-design-patterns/active-object-with-spring-pattern
./gradlew -q run
```

Act one: where is the lock? Act two: which setting bounded the mailbox? Act three: which thread changed the field first? Act four: why did the direct read say 0? Act five: which thread raised the error? Act six: what limits the rate?

## Exercises

1. Give the executor two threads and rerun act one. What happens, and why?
2. Make `peekStock` package-private and see who still calls it.
3. Add a `close` message that flushes the mailbox before shutdown.

Close with the verdict: one owner, every access through the proxy, and a bounded mailbox.

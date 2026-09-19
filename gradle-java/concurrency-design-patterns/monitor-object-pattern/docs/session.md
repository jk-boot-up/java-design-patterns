# Session Guide — Monitor Object Pattern

A 60-minute session built around one question: if a lock protects the
count, why does it still go wrong?

## Learning Objectives

1. Explain why `volatile` does not prevent a lost update.
2. Say why a lock held by the caller is weaker than a lock the object owns.
3. Explain why `await` belongs in a `while` loop.
4. Describe two ways a correct monitor still deadlocks.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the lost update |
| 0:10–0:20 | volatile, and the forgetful caller |
| 0:20–0:32 | The pattern |
| 0:32–0:44 | if versus while |
| 0:44–0:54 | Two deadlocks |
| 0:54–1:00 | Exercises |

## Walkthrough

```bash
cd concurrency-design-patterns/monitor-object-pattern
./gradlew -q run
```

Read acts one to three together. Ask: what exactly is shared, and what
three steps does a sale take? Open `naive/PlainStock.java` and find the
hook.

For act four, open `pattern/StockMonitor.java` and ask: which method can a
caller call without the lock? (None.)

For act five, open `pattern/IfInsteadOfWhile.java`. Ask the room to predict
the final count before running.

For act six, ask what a listener could do that needs the monitor's lock.

## Exercises

1. Replace `if` with `while` in `IfInsteadOfWhile` and confirm the count.
2. Fix `transferOneTo` by always locking the monitor with the lower id first.
3. Replace the count with an `AtomicInteger` and say what is lost.

Close with: an object that owns its lock cannot be used unsafely, but it
can still be used badly.

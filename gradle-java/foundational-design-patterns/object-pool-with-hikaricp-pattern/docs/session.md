# Session Guide — Object Pool with HikariCP Pattern

A 60-minute session built around one question: what does a mature pool solve, and what can it never solve?

## Learning Objectives

1. Say which of the hand-built pool's costs HikariCP solves.
2. Explain what it cannot reset, and why that matters.
3. Read its exhaustion message.
4. Explain why small pools are recommended.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | The pool, and what it opens |
| 0:22–0:36 | The dirty return, and what remains |
| 0:36–0:50 | Exhaustion and sizing |
| 0:50–1:00 | The verdict |

## Walkthrough

```bash
cd foundational-design-patterns/object-pool-with-hikaricp-pattern
./gradlew -q run
```

Act one: why one connection, not two? Act two: which state was reset, and which was not? Act three: read the exhaustion message. Act four: what size would you choose? Act five: why is the borrow so much cheaper? Act six: name a case where you would still write a pool.

## Exercises

1. Set `leakDetectionThreshold` and log to standard output. What appears?
2. Reset the session variable in `connectionInitSql`. Does that fix the leak, and what does it cost?
3. Set `minimumIdle` equal to the maximum and watch the pool fill.

Close with the verdict: use the library, and reset what it cannot see.

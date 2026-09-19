# Session Guide — Object Pool Pattern

A 60-minute session built around one question: when is it worth keeping objects instead of making new ones?

## Learning Objectives

1. Say when an object pool is worth its cost.
2. Explain why pooling a small object is slower than allocating it.
3. Explain how a pooled object can leak one customer's data to another.
4. Explain what happens when an object is leaked, and when a pool is sized wrongly.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the handshake |
| 0:10–0:20 | The pool |
| 0:20–0:36 | The benchmark, and its method |
| 0:36–0:50 | Dirty, leaked and sized |
| 0:50–1:00 | The verdict |

## Walkthrough

```bash
cd foundational-design-patterns/object-pool-pattern
./gradlew -q run
```

Act one: what is the cost, and where is it? Act two: what is saved? Act three: read `SmallObjectBenchmark` and say what each variant measures. Act four: what would you add to make the reset impossible to forget? Act five: what does a timeout not fix? Act six: what size would you choose?

## Exercises

1. Change `Receipt` to hold a 1 MB array. Does the ordering change, and why?
2. Give the pool a `Lease` that returns the connection in `close()`, used in try-with-resources.
3. Make the pool create connections lazily. What new problem appears?

Close with the verdict: pool what is expensive outside the JVM, and nothing else.

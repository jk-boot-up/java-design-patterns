# Session Guide — Double-Checked Locking Pattern

A 60-minute session built around one question: how do you build a shared object once, lazily, without locking for ever?

## Learning Objectives

1. Show the check-then-create race.
2. Show the lock's cost on every call.
3. Explain the second check and the volatile.
4. Choose the holder idiom.

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
cd concurrency-design-patterns/double-checked-locking-pattern
./gradlew -q run
```

Act one: how many were built in the race? Act two: how many lock takings for a thousand calls? Act three: what did the second thread find? Act four: which keyword does a test guard? Act five: what was built before anyone asked? Act six: how many lines for each version?

## Exercises

1. Remove the volatile keyword and explain why no test fails.
2. Change the constructor to take an argument, and choose between the holder and double-checking.
3. Measure the cost of an uncontended lock on your machine.

Close with the verdict: the holder first, double-checked only when it must be, and never without the volatile.

# Session Guide — Guarded Suspension Pattern

A 60-minute session built around one question: how should a thread wait for a condition?

## Learning Objectives

1. Say why asking again and again is wasteful.
2. Show why the guard is a while and not an if.
3. Show a notification that arrived too early.
4. Say why every wait needs a limit.

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
cd concurrency-design-patterns/guarded-suspension-pattern
./gradlew -q run
```

Act one: how many checks with no order? Act two: what state was the thread in? Act three: what did the if version take? Act four: what did the blind picker do? Act five: what did the limit return? Act six: how many threads woke for one order?

## Exercises

1. Change notifyAll to notify, and find the case where a picker is never woken.
2. Replace the inbox with a LinkedBlockingQueue and count the lines saved.
3. Add a shutdown flag, so waiting pickers can be told to stop.

Close with the verdict: use the library, check the guard in a loop, hold the lock you wait on, and give every wait a limit.

# Session Guide — Thread-Local Storage Pattern

A 60-minute session built around one question: how does code deep in a request know who the customer is, without being told?

## Learning Objectives

1. Show a thread-local read with no parameter.
2. Show two threads with their own values.
3. Show a leak through a reused thread.
4. Say why a value does not cross to another thread.

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
cd concurrency-design-patterns/thread-local-storage-pattern
./gradlew -q run
```

Act one: how many methods carried the customer? Act two: what did the log say? Act three: what did the two threads log? Act four: who was request B logged as? Act five: what did the other thread see? Act six: what did a method with none set log?

## Exercises

1. Write a decorator that copies the context to a pool thread for one task, and clears it after.
2. Replace the thread-local with an explicit parameter, and count the signatures that change.
3. Add a large value to the context, and see how long a pool thread keeps it.

Close with the verdict: per-request context only, set and clear in one place, hand it on by hand, and prefer a parameter.

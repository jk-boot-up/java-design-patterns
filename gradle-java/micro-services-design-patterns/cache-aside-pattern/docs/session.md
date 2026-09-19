# Session Guide — Cache-Aside Pattern

A 60-minute session built around one question: what does a cache in front of a database give you, and what does it take away?

## Learning Objectives

1. Say the steps of cache-aside.
2. Show a stale read and how a write fixes it.
3. Explain what an expiry bounds.
4. Explain a stampede and the shared read.

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
cd micro-services-design-patterns/cache-aside-pattern
./gradlew -q run
```

Act one: how many reads with no cache? Act two: how many with one? Act three: which write forgot the cache? Act four: how long was the price stale? Act five: how many reads for fifty callers? Act six: what happens on a cold start?

## Exercises

1. Change the expiry to ten seconds and rerun acts two and four.
2. Add a maximum size to the cache and decide what to throw away.
3. Make the stampede test fail by removing the recheck in the shared read.

Close with the verdict: read-heavy, tolerant of a little staleness, invalidate on writes, expire everything, share the read.

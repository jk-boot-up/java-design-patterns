# Session Guide — Lazy Load Pattern

A 60-minute session built around one question: when should related data be loaded, and what does asking later cost?

## Learning Objectives

1. Explain why eager loading of one order creates so many objects.
2. Name the four lazy variants.
3. Explain N+1 and count it.
4. Explain why a lazy failure happens at the point of use.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the eager graph |
| 0:10–0:24 | Four variants |
| 0:24–0:40 | N+1 |
| 0:40–0:52 | I/O and the closed session |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/lazy-load-pattern
./gradlew -q run
```

Act one: count the objects. Act two: which variant would you choose for a required field, and which for an optional one? Act three: what is the query count, and why? Act four: where does the exception surface? Act five: who was holding the object when the session closed?

## Exercises

1. Change `OrderList.lazy` to fetch each customer once, and count the queries.
2. Make `Session.select` count reads and log the caller.
3. Add a fifth variant that loads a customer's orders lazily.

Close with: lazy loading trades one big query for many small ones, and moves a failure to where the object is used.

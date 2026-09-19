# Session Guide — Lazy Load with Hibernate Pattern

A 60-minute session built around one question: why does a lazy field fail after the session closes, and what are the fixes?

## Learning Objectives

1. Explain what is inside a lazy field.
2. Explain why `LazyInitializationException` happens.
3. Name three usual fixes and one cost of each.
4. Explain why the customer page cost 6 statements and the line page 21.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | The exception |
| 0:22–0:36 | The proxy |
| 0:36–0:52 | The three fixes |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/lazy-load-with-hibernate-pattern
./gradlew -q run
```

Act one: read the exception message closely. Act two: what does the proxy hold? Act three: why 6 and 21? Act four: what does 80 rows mean? Act five: what is lost by a projection?

## Exercises

1. Change `FetchType.LAZY` to `EAGER` on the order's customer and count the statements.
2. Use `Hibernate.initialize(order.customer())` before closing the session. Which fix is that?
3. Add `@BatchSize(size = 10)` to the lines and count the statements.

Close with: a lazy field is a promise that needs a session to keep.

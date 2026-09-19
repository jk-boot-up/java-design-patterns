# Session Guide — Future/Promise with Spring Pattern

A 60-minute session built around one question: what does @Async return, and what does it lose on the way?

## Learning Objectives

1. Explain why the pool decides how concurrent three lookups are.
2. Say where a void method's exception goes.
3. Explain why a thread-local is empty on a pool thread, and the fix.
4. Explain why neither a timeout nor cancel stops the task.

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
cd concurrency-design-patterns/future-promise-with-spring-pattern
./gradlew -q run
```

Act one: what limits concurrency? Act two: which of the two exceptions did the caller see? Act three: what did the TaskDecorator copy? Act four: who was waiting when the task finished? Act five: what did cancel(true) actually do? Act six: where did the fallback go?

## Exercises

1. Make `slowLookup` check `Thread.interrupted()` in a loop and cancel it through an `ExecutorService` future.
2. Use `completeOnTimeout` instead of `orTimeout` and repeat act four.
3. Copy an `MDC` value across the thread boundary with a `TaskDecorator`.

Close with the verdict: return a future, choose the pool, carry the context, and design tasks that can be stopped.

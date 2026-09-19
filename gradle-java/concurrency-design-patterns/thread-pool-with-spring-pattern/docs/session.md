# Session Guide — Thread Pool with Spring Pattern

A 60-minute session built around one question: what pool does @Async use, and what should you change?

## Learning Objectives

1. Say what Spring Boot's default executor is.
2. Say what an unbounded queue does when workers are busy.
3. Read a `TaskRejectedException`.
4. Explain why a call on `this` ignores `@Async`.

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
cd concurrency-design-patterns/thread-pool-with-spring-pattern
./gradlew -q run
```

Act one: read the three numbers. Act three: where does the backlog go? Act four: which setting decided the refusal? Act five: which thread ran the work? Act six: why can the label task never run?

## Exercises

1. Set `spring.threads.virtual.enabled=true` and print `Thread.currentThread().isVirtual()`.
2. Define a `TaskExecutor` bean with a `CallerRunsPolicy` and repeat act four.
3. Move `pack` into another bean and call it from `packThroughThis`. What changes?

Close with the verdict: name the pool, bound the queue, and do not wait on it.

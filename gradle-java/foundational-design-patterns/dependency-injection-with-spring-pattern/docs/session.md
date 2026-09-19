# Session Guide — Dependency Injection with Spring Pattern

A 60-minute session built around one question: what does Spring's container replace, and what does it leave?

## Learning Objectives

1. Say what `@Component` replaced.
2. Read Spring's missing-bean and circular-dependency errors.
3. Say why field injection is discouraged.
4. Explain the cost of the magic.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | The same graph |
| 0:22–0:36 | Start-up failures |
| 0:36–0:50 | Field injection and the cost |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd foundational-design-patterns/dependency-injection-with-spring-pattern
./gradlew -q run
```

Act one: where did the wiring go? Act two: count the annotations. Act three: read the message aloud. Act four: what would you change to remove the cycle? Act five: which form would you refuse in review? Act six: when would you keep the hand wiring?

## Exercises

1. Add `@Primary` to a second `Notifier` and see what Spring does.
2. Delete `@Component` from `RecordingNotifier` and read the new error.
3. Give `CheckoutService` a second constructor. What does Spring now need?

Close with: Spring did not add the idea, it removed the typing.

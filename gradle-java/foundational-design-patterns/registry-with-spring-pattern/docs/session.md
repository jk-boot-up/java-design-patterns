# Session Guide — Registry with Spring Pattern

A 60-minute session built around one question: what does a well-built registry fix, and what does it still leak?

## Learning Objectives

1. Say which of the hand-built registry's costs Spring fixes.
2. Say when `getBean` is a service locator.
3. Explain how a cached context causes order-dependent tests.
4. Explain why a typo in a property name is silent.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | The context as a registry |
| 0:22–0:38 | The shared-state leak |
| 0:38–0:50 | Properties and ambiguity |
| 0:50–1:00 | The verdict |

## Walkthrough

```bash
cd foundational-design-patterns/registry-with-spring-pattern
./gradlew -q run
```

Act one: what replaced `register`? Act two: compare the two checkouts' constructors. Act three: read `SharedContextLeakTest`, and run its second test alone. Act four: which lookup would you rather have in production? Act five: how would you resolve the ambiguity? Act six: where does your code call `getBean`?

## Exercises

1. Run only the second test of `SharedContextLeakTest` and watch it fail.
2. Add `@Primary` to `RecordingNotifier` and rerun act five.
3. Make the gateway request-scoped and see what the leak does.

Close with: the registry done well is one you rarely call.

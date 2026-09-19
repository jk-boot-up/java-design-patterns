# Session Guide — Prototype with Spring Pattern

A 60-minute session built around one question: what does Spring's prototype scope give you, and what does it not?

## Learning Objectives

1. Say that prototype scope builds from the definition, not from a draft.
2. Explain why a prototype injected into a singleton is built once.
3. Explain who cleans up a prototype.

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
cd creational/prototype-with-spring-pattern
./gradlew -q run
```

Act one: is it the same object? Act two: which fields did the edit reach? Act three: which call gave back the edited title? Act four: why did the second caller see the first caller's title? Act five: what changed? Act six: how many were destroyed?

## Exercises

1. Add a `copy()` test that shows a deep copy of the images.
2. Inject `Listing` into a second singleton and predict what its callers see.
3. Make the listing implement `DisposableBean` and see if it is called.

Close with the verdict: prototype scope for fresh objects, a provider inside singletons, and your own copy for drafts.

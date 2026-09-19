# Session Guide — DTO Pattern

A 60-minute session built around one question: what should cross the boundary, and what should stay inside?

## Learning Objectives

1. List what goes wrong when a domain object is serialised.
2. Say what a DTO is and what it is not.
3. Explain the cost of mapping code.
4. Explain why DTOs multiply.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the leaking JSON |
| 0:10–0:22 | The coupled field names |
| 0:22–0:34 | The pattern |
| 0:34–0:48 | The bill |
| 0:48–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/dto-pattern
./gradlew -q run
```

Act one: what is in the JSON that should not be? Act two: why does renaming a private field break a client? Act three: compare the two sizes. Act four: which of the two would enforce a rule? Act five: how many DTOs would your project need for one entity?

## Exercises

1. Add a `phone` field to `Customer`. Which classes must change to expose it, and which to hide it?
2. Write a test that fails if a DTO gains a field the domain object lacks.
3. Make `toDetail` avoid loading the order history.

Close with: a DTO is a contract, and the mapping is what you pay for one.

# Session Guide — Null Object Pattern

A 60-minute session built around one question: what should a caller see when there is nothing there?

## Learning Objectives

1. Explain how null checks spread and how one gets forgotten.
2. Say what a null object is and does.
3. Explain how a null object can hide an error.
4. Choose between a null object, `Optional` and an exception.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the null checks |
| 0:10–0:20 | The forgotten check |
| 0:20–0:32 | The pattern |
| 0:32–0:46 | The bill, and Optional |
| 0:46–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd foundational-design-patterns/null-object-pattern
./gradlew -q run
```

Act one: which method is the odd one out? Act two: how long did it take you to find it? Act three: diff the two checkouts. Act four: how would you notice the full-price order? Act five: which would you choose at a service boundary? Act six: name two null objects in the JDK.

## Exercises

1. Add a `FreeShippingPolicy` with a null object. What is its `apply`?
2. Write a test that would catch `ForgivingDirectory` swallowing an outage.
3. Change `OptionalDirectory` callers to `orElse(NoDiscount.INSTANCE)`. What did you gain and lose?

Close with the verdict: legitimate absence, yes; hidden failure, never.

# Session Guide — Value Object Pattern

A 60-minute session built around one question: what does a value object give you that a bare number does not?

## Learning Objectives

1. Say the four properties of a value object.
2. Show a bug that a bare number allows and a value forbids.
3. Explain why allocation belongs in the type.

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
cd domain-driven-design-patterns/value-object-pattern
./gradlew -q run
```

Act one: which sum is wrong? Act two: which line refuses the mix? Act three: why does the set hold one? Act four: who changed order A's price? Act five: which method forgot to check? Act six: where did the penny go?

## Exercises

1. Write a Quantity type that refuses a negative number.
2. Add a `percent(int)` method to Money and decide how it rounds.
3. Make Money carry a `Currency` object instead of a string.

Close with the verdict: value objects where a raw type hides a meaning, and not everywhere.

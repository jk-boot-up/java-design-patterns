# Session Guide — Type Object Pattern

A 60-minute session built around one question: when should a kind of thing be a class, and when should it be data?

## Learning Objectives

1. Show three classes differing by numbers.
2. Show a kind added with no class.
3. Show a change to a type reaching all its products.
4. Say where data stops being enough.

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
cd foundational-design-patterns/type-object-pattern
./gradlew -q run
```

Act one: how many classes? Act two: what did the laptop total? Act three: how many classes were added? Act four: what was tea's tax afterwards? Act five: where did the ebook's return days come from? Act six: what did the typo do?

## Exercises

1. Add a frozen grocery type that inherits from grocery.
2. Refuse unknown type names when a product is made, with a helpful message.
3. Add a return fee to the type, and use it.

Close with the verdict: data where kinds differ in numbers, code where they differ in steps.

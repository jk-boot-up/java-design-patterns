# Session Guide — Immutable Object Pattern

## Learning Objectives

By the end of the session you can:

- Explain how a change through one reference is seen through another.
- Write an immutable class: no setters, final fields, copied collections.
- Replace an object whole instead of changing it in place.
- Say when immutability costs more than it saves.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Shared, then changed | 7 min |
| 0:17 | Act 2: Changed while being read | 7 min |
| 0:24 | Act 3: Lost in a set | 7 min |
| 0:31 | Act 4: Immutable objects | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read acts one to three before any code: each is a bug
learners have met without knowing its name. Then open `Address.java` (a
record, four lines) and `PriceList.java`, and point out the two lines that make
it safe: `Map.copyOf` in the constructor, and `with...` returning a new list.

## Exercises

1. Add a postcode to `Address`, with a `withPostcode` method.
2. Make `PriceList.withPrice` refuse a negative price. Where should the check go?
3. Add a list of tags to `Address` and make sure the record stays immutable.
4. Find a class in another project in this course that could be a record. Convert it.

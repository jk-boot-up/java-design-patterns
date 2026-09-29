# Session Guide — Marker Interface Pattern

## Learning Objectives

By the end of the session you can:

- Say what a marker interface is and why it has no methods.
- Use a marker in `instanceof` and as a parameter type.
- Explain why the compiler catches what tags cannot.
- Choose between a marker and an annotation.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Free-text tags | 7 min |
| 0:17 | Act 2: A marker interface | 7 min |
| 0:24 | Act 3: The compiler checks | 7 min |
| 0:31 | Act 4: The mark is passed on | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one aloud: a capital letter ships milk warm.
Open `Markers`: two interfaces, no methods. Then show `sendChilled(Perishable)`
and try passing a kettle in the IDE to see the compiler error.

## Exercises

1. Add a `Hazardous` marker for batteries and a packer rule for it.
2. Replace `Perishable` with an annotation `@Chilled(maxC = 5)`. What does the compiler stop checking?
3. Write a test that every class in the dairy package is Perishable.

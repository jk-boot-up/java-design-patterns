# Session Guide — Entity Pattern

## Learning Objectives

By the end of the session you can:

- Tell an entity from a value object.
- Give an entity an identity that never changes.
- Write equals and hashCode over the identity only.
- Explain what equality does not tell you about an entity.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Defined by values | 7 min |
| 0:17 | Act 2: Defined by identity | 7 min |
| 0:24 | Act 3: Look-alikes are different | 7 min |
| 0:31 | Act 4: A life story | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read acts one and two side by side: the same email
change, two outcomes. Open `Customer.equals` and `hashCode`: one field each.
Then ask learners to name three things in a shop that are entities and three
that are values.

## Exercises

1. Make `Order` an entity with an `OrderId`.
2. Add a method that says whether two customer objects hold the same details, separate from equals.
3. Generate IDs with a counter. What goes wrong after the program restarts?

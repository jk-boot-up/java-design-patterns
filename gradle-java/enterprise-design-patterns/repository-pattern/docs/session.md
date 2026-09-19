# Session Guide — Repository Pattern

A 60-minute session built around one question: should the caller know where customers are stored?

## Learning Objectives

1. Explain why the same query in three places drifts.
2. Say what a repository interface looks like to its caller.
3. Show that a store can be swapped without touching the caller.
4. Name two costs of a repository.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and three answers |
| 0:10–0:20 | The schema change |
| 0:20–0:36 | The pattern and the swap |
| 0:36–0:50 | The bill |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/repository-pattern
./gradlew -q run
```

Act one: which service is wrong, and why is that easy to miss? Act two: how would you have found every use of the column? Act three: what does MarketingService import? Act four: read the one-line change. Act five: which is easier to read, the long method name or the specification? Act six: what would you add to the interface to fix seven operations?

## Exercises

1. Add `findByName` to both implementations. How many classes change?
2. Write a specification for customers with no orders.
3. Make the database repository fetch orders in one operation. What must the interface gain?

Close with: a repository lets the caller speak the domain, but every question still needs somewhere to live.

# Session Guide — Query Object Pattern

## Learning Objectives

By the end of the session you can:

- Explain why gluing SQL from strings breaks and is unsafe.
- Build a query from criteria with placeholders.
- Test a query's meaning in memory.
- Extend a saved query without changing it.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: SQL glued from strings | 7 min |
| 0:17 | Act 2: A query object | 7 min |
| 0:24 | Act 3: The same query in memory | 7 min |
| 0:31 | Act 4: Safe and reusable | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one's three lines of SQL aloud. Then open
`Criterion`: each one is a SQL fragment, a list of values, and a Java test.
Show `ProductQuery.toSql` joining them with AND, and `runOn` using the same
criteria over a list.

## Exercises

1. Add `minPrice` and use it with `maxPrice` for a price range.
2. Add sorting: `orderBy("price_pence")`. How do you stop a customer choosing an unknown column?
3. Add an `or(Criterion, Criterion)` criterion.
4. Write a test that runs every criterion in memory and checks its SQL mentions the right column.

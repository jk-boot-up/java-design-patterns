# Session Guide — Single Table Inheritance Pattern

## Learning Objectives

By the end of the session you can:

- Explain how a class hierarchy can be stored in one table.
- Use a type column to build the right class when loading.
- Add a type with a new column.
- Name the costs: empty cells and weaker constraints.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A table per type | 7 min |
| 0:17 | Act 2: One table for all | 7 min |
| 0:24 | Act 3: Each row becomes its own class | 7 min |
| 0:31 | Act 4: A new type | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's three queries with act two's one.
Open `ProductTable.create` to see the single wide table, then `load`, where the
type column picks the class. Finish on act five: ask how the book without an
ISBN could be stopped.

## Exercises

1. Add a CHECK constraint that a BOOK row must have an ISBN. Does H2 enforce it?
2. Store the same products with Class Table Inheritance: a shared table and one per type, joined. Compare the queries.
3. Add a `Clothing` type with a size column.

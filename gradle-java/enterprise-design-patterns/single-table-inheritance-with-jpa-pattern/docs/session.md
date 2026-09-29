# Session Guide — Single Table Inheritance with JPA Pattern

## Learning Objectives

By the end of the session you can:

- Map a class hierarchy with @Inheritance(SINGLE_TABLE).
- Read the SQL Hibernate writes for polymorphic queries.
- Compare single table with table per class.
- Explain why subclass columns cannot be NOT NULL.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A table per class | 7 min |
| 0:17 | Act 2: One table | 7 min |
| 0:24 | Act 3: Each row as its own class | 7 min |
| 0:31 | Act 4: A new type | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `single/Product`: three annotations. Compare act one's
UNION with act two's plain select. End on act five's refused NOT NULL.

## Exercises

1. Switch the products to JOINED and read the SQL for act two.
2. Add Bean Validation's @NotNull to Book.isbn and save a book without one.
3. Add a Clothing subclass with a size column.

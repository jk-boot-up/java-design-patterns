# Session Guide — Table Data Gateway Pattern

## Learning Objectives

By the end of the session you can:

- Explain why SQL spread across callers is fragile.
- Write a gateway with one method per question.
- Return plain records instead of result sets.
- Say when to move on to Repository or Data Mapper.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: SQL in every caller | 7 min |
| 0:17 | Act 2: A table data gateway | 7 min |
| 0:24 | Act 3: A rename, fixed once | 7 min |
| 0:31 | Act 4: Where the SQL lives | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: three failures from one rename. Open
the `scattered` package and find the word "stock" in each file. Then open
`ProductGateway` and show that it is now the only place the column is named.

## Exercises

1. Add `insert(Row)` and `delete(sku)` to the gateway, with tests.
2. Add an `order_line` table and its own gateway.
3. Move the "low on stock" rule into a method. Where should it go?

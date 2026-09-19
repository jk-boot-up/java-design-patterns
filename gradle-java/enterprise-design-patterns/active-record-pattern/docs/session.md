# Session Guide — Active Record Pattern

A 60-minute session built around one question: what does it cost to let an object save itself?

## Learning Objectives

1. Say what an active record is.
2. Show a rule that cannot be tested without the table.
3. Show a schema change breaking a class.
4. Show a hidden query.

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
cd enterprise-design-patterns/active-record-pattern
./gradlew -q run
```

Act one: which lines save and find? Act two: which method finds a customer's orders? Act three: which rules are on the record? Act four: how many table operations did the rule need? Act five: what broke when the column was renamed? Act six: how many queries for five orders?

## Exercises

1. Make the delivery rule take a total, and count the operations again.
2. Add a batch finder that loads the customers once.
3. Rename a field in Order and decide what should change in Table.

Close with the verdict: active record for close-to-the-table work, pure functions for rules that need no table, and a data mapper when the two drift apart.

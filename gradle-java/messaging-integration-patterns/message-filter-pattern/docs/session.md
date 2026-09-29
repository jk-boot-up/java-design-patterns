# Session Guide — Message Filter Pattern

## Learning Objectives

By the end of the session you can:

- Explain why receivers on a shared channel get too much.
- Write a filter that keeps a receiver unaware of it.
- Chain filters.
- Decide what should happen to dropped messages.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Everything to everyone | 7 min |
| 0:17 | Act 2: A filter | 7 min |
| 0:24 | Act 3: Chained filters | 7 min |
| 0:31 | Act 4: A changed rule | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one. Open `MessageFilter`: a rule, a next
step, a counter. Show that `Channel` and the receivers never mention filters.
End on act five: where should the dropped fifteen go?

## Exercises

1. Send dropped messages to a discard channel and print them.
2. Add a filter that only lets through each customer's first order of the day.
3. Replace the two chained filters with one using `and`. What is lost?

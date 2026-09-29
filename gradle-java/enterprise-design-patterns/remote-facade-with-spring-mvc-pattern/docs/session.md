# Session Guide — Remote Facade with Spring MVC Pattern

## Learning Objectives

By the end of the session you can:

- Measure the cost of chatty remote calls.
- Return a screen as one JSON record.
- Make a change all-or-nothing and report refusals as ProblemDetail.
- Keep business rules on the fine-grained objects.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A call for every fact | 7 min |
| 0:17 | Act 2: The whole screen as JSON | 7 min |
| 0:24 | Act 3: All or nothing | 7 min |
| 0:31 | Act 4: Fine-grained inside | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's five round trips with act two's one.
Open `OrderFacade`: two methods and an exception handler. End on act three's
half-changed order and the facade's 422.

## Exercises

1. Add a small `GET /order-slot` for the widget, and discuss where it belongs.
2. Add an ETag to the summary so an unchanged screen costs almost nothing.
3. Give the fine-grained API an exception handler too.

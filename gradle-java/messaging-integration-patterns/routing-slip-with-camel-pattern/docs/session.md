# Session Guide — Routing Slip with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Write a slip into a header and follow it with `routingSlip()`.
- Add a step by changing only the slip writer.
- Explain why a slip cannot change course.
- Use `dynamicRouter()` to decide steps on the way.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One fixed pipeline | 7 min |
| 0:17 | Act 2: The slip | 7 min |
| 0:24 | Act 3: Camel follows the slip | 7 min |
| 0:31 | Act 4: A new step | 7 min |
| 0:38 | Act 5: The bill, and a dynamic router | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's 24 visits with act three's 15. Open
`ShopRoutes`: the routing slip is two lines. End on act five's two routes for
ORD-5.

## Exercises

1. Add a loyalty-points step for registered customers.
2. Make the dynamic router send international orders to customs.
3. Put a typo in one slip entry and read Camel's error.

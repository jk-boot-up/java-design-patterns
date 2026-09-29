# Session Guide — Priority Queue with RabbitMQ Pattern

## Learning Objectives

By the end of the session you can:

- Declare a RabbitMQ priority queue and send prioritised messages.
- Explain why prefetch defeats priority.
- Show starvation under strict priority.
- Build a reserved share with two queues.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: First in, first out | 7 min |
| 0:17 | Act 2: A priority queue | 7 min |
| 0:24 | Act 3: A flood | 7 min |
| 0:31 | Act 4: Only what is still waiting | 7 min |
| 0:38 | Act 5: The bill: starvation | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's 9:11 with act two's
9:01. Open `Warehouse.declare` and `place`: one argument and one property. End
on act four's positions 101 to 105.

## Exercises

1. Try prefetch 10 in act four and find where the same-day orders land.
2. Add a third priority, express, above same-day.
3. Use a single consumer that takes 8 from the priority queue and 2 from the standard queue each minute.

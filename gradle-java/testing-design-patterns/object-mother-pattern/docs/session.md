# Session Guide — Object Mother / Test Data Builder Pattern

## Learning Objectives

By the end of the session you can:

- Spot test setup that hides what a test is about.
- Write an Object Mother of named test objects.
- Write a Test Data Builder with safe defaults.
- Keep every detail a test depends on inside the test.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Built by hand | 7 min |
| 0:17 | Act 2: An Object Mother | 7 min |
| 0:24 | Act 3: The mother multiplies | 7 min |
| 0:31 | Act 4: A Test Data Builder | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's hand-built order with act four's
one-liners. Open `ShippingRulesTest`: each test reads as a sentence. End on
act five's hidden default.

## Exercises

1. Add `withLines(...)` to the builder and test an order of three products.
2. Make `TestOrders` methods return builders, so mothers and builders combine.
3. Add a required `phone` field to `Customer` and count the files you must change.

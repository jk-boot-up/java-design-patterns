# Session Guide — Railway-Oriented Programming Pattern

## Learning Objectives

By the end of the session you can:

- Explain two-track error handling.
- Write a `Result` type with `flatMap` and `map`.
- Chain steps so later ones are skipped after a failure.
- Recover from a chosen failure.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Exceptions nobody caught | 7 min |
| 0:17 | Act 2: The success track | 7 min |
| 0:24 | Act 3: Switching tracks | 7 min |
| 0:31 | Act 4: Plain functions, and a way back | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 500 with act three's 422 at
charge. Open `CheckoutSteps.checkout`: four lines. Then `Result.flatMap`: two
cases. End on act five's single problem.

## Exercises

1. Add a step that applies a coupon and can fail when it has expired.
2. Add a `peek` method that logs the value without changing the track.
3. Rewrite the chain with Vavr's `Either`.

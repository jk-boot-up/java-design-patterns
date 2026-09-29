# Session Guide — Railway-Oriented Programming with Vavr Pattern

## Learning Objectives

By the end of the session you can:

- Chain steps with Vavr's Either and flatMap.
- Wrap throwing code with Try and toEither.
- Recover with orElse.
- Collect all errors with Validation.combine.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A throwing library | 7 min |
| 0:17 | Act 2: Either | 7 min |
| 0:24 | Act 3: Skipping, and Try | 7 min |
| 0:31 | Act 4: map and orElse | 7 min |
| 0:38 | Act 5: Validation | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `CheckoutSteps.checkout`: four flatMaps. Open
`charge`: Try around the library. End on act five's two answers for the same
form.

## Exercises

1. Add a coupon step that can fail, returning Either.
2. Recover only from out-of-stock failures, and let others through.
3. Add a postcode check to the Validation.

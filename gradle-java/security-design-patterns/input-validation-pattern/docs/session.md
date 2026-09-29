# Session Guide — Input Validation Pattern

## Learning Objectives

By the end of the session you can:

- Treat all outside input as untrusted.
- Check fields against allow-list rules and report every problem.
- Use self-checking types so valid data stays valid.
- Tell input validation apart from output encoding.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Trusting the form | 7 min |
| 0:17 | Act 2: Check at the boundary | 7 min |
| 0:24 | Act 3: Types that cannot be wrong | 7 min |
| 0:31 | Act 4: Encode on the way out | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's -49.95 with act two's three
problems. Open `Quantity`: the compact constructor is the whole rule. End on
act five's two name rules.

## Exercises

1. Add a postcode type with a rule for UK postcodes.
2. Rewrite `OrderForm` with Bean Validation annotations and compare.
3. Store reviews in H2 with a `PreparedStatement`, never string concatenation.

# Session Guide — Message Filter with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Put a `filter()` in front of a Camel endpoint.
- Write rules in Camel's Simple language.
- Read a changing setting inside a rule.
- Add a discard channel with `otherwise()`.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Every service gets every order | 7 min |
| 0:17 | Act 2: A filter in front | 7 min |
| 0:24 | Act 3: Two conditions | 7 min |
| 0:31 | Act 4: Change the rule while running | 7 min |
| 0:38 | Act 5: The bill, and a discard channel | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ShopRoutes.configure`: the gift-wrap filter is
three lines. Compare acts three and four: same route, new threshold. End on
act five's discard channel.

## Exercises

1. Add a discard channel to the gift-wrap filter too, and count its rejects.
2. Write the gift rule as a Java predicate instead of a Simple expression, and compare.
3. Make a typo in a Simple expression and read the error Camel gives.

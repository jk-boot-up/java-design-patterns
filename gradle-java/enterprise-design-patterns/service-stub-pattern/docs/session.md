# Session Guide — Service Stub Pattern

## Learning Objectives

By the end of the session you can:

- Put an external service behind a gateway interface.
- Write a stub that answers like the real service.
- Use the stub to test failures on demand.
- Keep the stub honest with a contract check.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The real service in development | 7 min |
| 0:17 | Act 2: A service stub | 7 min |
| 0:24 | Act 3: Awkward cases on demand | 7 min |
| 0:31 | Act 4: The contract check | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: money and time spent on lookups. Open
`AddressGateway` (one method) and `PostcodeStub` (a map and a switch). Finish
on act four: show that `ContractCheck` is the only thing that noticed the
small-letters difference.

## Exercises

1. Fix the stub so it refuses small letters, like the real service.
2. Make checkout turn postcodes into capitals before looking them up. Does the contract check still find a difference?
3. Give the stub a 'slow' mode that takes 3 seconds, and add a timeout to checkout.

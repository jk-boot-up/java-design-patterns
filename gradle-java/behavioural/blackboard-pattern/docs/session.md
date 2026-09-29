# Session Guide — Blackboard Pattern

## Learning Objectives

By the end of the session you can:

- Describe the three parts: the board, the knowledge sources and the controller.
- Write a knowledge source that says when it is ready.
- Explain how the controller saves work by stopping early.
- Add a knowledge source without changing the others.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Every check, every time | 7 min |
| 0:17 | Act 2: The blackboard | 7 min |
| 0:24 | Act 3: Stopping early | 7 min |
| 0:31 | Act 4: A new expert | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one with act three: 902 milliseconds
against 102. Then open `Checks.countryMatch()` and point out that it only says
it needs two facts; nothing says when it runs. Finish in `Controller.decide`,
a short loop that is the whole pattern.

## Exercises

1. Add a check that needs the device result and adds risk for a new device on an old account.
2. Make the controller approve early when every remaining check could not reach 60.
3. Hide the card number from every check except the card country check.
4. Print the log as a numbered story a support agent could read.

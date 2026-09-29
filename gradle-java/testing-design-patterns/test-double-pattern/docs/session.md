# Session Guide — Test Double Pattern

## Learning Objectives

By the end of the session you can:

- Name the five kinds of test double and the question each answers.
- Write a dummy, stub, spy, mock and fake for one interface.
- Explain the difference between checking state (fake) and checking calls (spy, mock).
- Say what a double can never prove, and what to do about it.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The real provider | 5 min |
| 0:15 | Act 2: A dummy and a stub | 5 min |
| 0:20 | Act 3: A spy | 5 min |
| 0:25 | Act 4: A mock | 5 min |
| 0:30 | Act 5: A fake | 5 min |
| 0:35 | Act 6: The bill | 5 min |
| 0:40 | Exercises | 20 min |

## Walkthrough

Start with act one and ask the room what is wrong with a test that passed.
Then open `PaymentGateway.java` and point out that all five doubles implement it:
the interface is what makes doubles possible. Read each double in turn; none is
more than forty lines. End on act six, and ask which double would have caught
the pence bug, and which would not.

## Exercises

1. Rewrite `CheckoutTest` using Mockito. Which of the five doubles does each Mockito call create?
2. Add a stub that throws a timeout, and make checkout report "try again later".
3. Make `FakeGateway` refuse a refund of an already refunded receipt, and test it.
4. Find the one test that should talk to a real provider sandbox, and write it down as a to-do.

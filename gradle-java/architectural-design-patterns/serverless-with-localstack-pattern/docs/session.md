# Session Guide — Serverless with LocalStack Pattern

A 60-minute session built around one question: what does a real function platform do with your function, and what must you plan for?

## Learning Objectives

1. Say what starts for each concurrent call.
2. Explain the cold start.
3. Show what a function forgets.
4. Say what the time limit does.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:25 | The first acts |
| 0:25–0:40 | The failures of its own |
| 0:40–0:52 | The cost |
| 0:52–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd architectural-design-patterns/serverless-with-localstack-pattern
./gradlew -q run
```

Act one: what did the server cost? Act two: how many receipts were sent? Act three: how many copies for five orders? Act four: which call was slower? Act five: what did the new copy remember? Act six: what did the platform say about the long job?

## Exercises

1. Raise the time limit to ten seconds, and rerun the last act.
2. Change the idle time, and rerun act three.
3. Keep the count of calls in a file outside the function.

Close with the verdict: short work, state outside, plan for the cold start, and price it when busy.

# Session Guide — Execute Around Pattern

A 60-minute session built around one question: how do you make sure that clean-up always happens, without every caller remembering?

## Learning Objectives

1. Show a leak on the error path.
2. Show the closing in one place.
3. Show a transaction undone on failure.
4. Show a resource escaping.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | The scenario and the naive version |
| 0:10–0:30 | The pattern |
| 0:30–0:45 | The bill |
| 0:45–0:52 | The verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd foundational-design-patterns/execute-around-pattern
./gradlew -q run
```

Act one: how many connections stayed open? Act two: how many? Act three: what came out? Act four: what was the balance after the failure? Act five: what was measured for the failing job? Act six: what happened to the escaped connection?

## Exercises

1. Add a retry around the work.
2. Add a lock as a third around method.
3. Make the connection refuse use outside the block, with a clear message.

Close with the verdict: clean-up in one place, in a finally block, and never let the resource out.

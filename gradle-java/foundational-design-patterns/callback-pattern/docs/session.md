# Session Guide — Callback Pattern

A 60-minute session built around one question: how do you hear the answer to something slow without standing still?

## Learning Objectives

1. Show the cost of asking again and again.
2. Show a callback with a result.
3. Show a failing callback contained.
4. Show why nesting hurts.

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
cd foundational-design-patterns/callback-pattern
./gradlew -q run
```

Act one: how many looks found nothing? Act two: what ran first? Act three: what did order two's callback decide? Act four: who saw the exception? Act five: what did the shared field say? Act six: how many levels deep?

## Exercises

1. Add a callback for failures only.
2. Give the gateway a timeout callback.
3. Rewrite the three nested steps with CompletableFuture and compare.

Close with the verdict: hand over code, carry your own data, and turn to futures when steps chain.

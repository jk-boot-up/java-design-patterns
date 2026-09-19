# Session Guide — Two-Phase Termination Pattern

A 60-minute session built around one question: how do you stop a thread without damaging what it is doing?

## Learning Objectives

1. Show a half-written order from an abrupt stop.
2. Show a stop that finishes the unit of work.
3. Explain why a sleeping worker needs an interrupt.
4. Explain the time limit on phase two.

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
cd concurrency-design-patterns/two-phase-termination-pattern
./gradlew -q run
```

Act one: how many lines were written? Act two: how many orders finished? Act three: what state was the sleeping worker in? Act four: did cleanup run? Act five: was the stuck worker alive? Act six: how many orders were left?

## Exercises

1. Make the worker finish its queued orders before stopping, and decide how long it may take.
2. Add a second phase that saves the queued orders to a file.
3. Make the worker report how long it took to stop.

Close with the verdict: ask, then wait with a limit, finish the unit, clean up in a finally, and decide about the queue.

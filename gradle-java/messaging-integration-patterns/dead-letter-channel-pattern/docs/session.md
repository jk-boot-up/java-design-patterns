# Session Guide — Dead Letter Channel Pattern

A 60-minute session built around one question: what should a worker do with a message that will never succeed?

## Learning Objectives

1. Say what a poison message does to a line.
2. Say what a dead letter records.
3. Tell a transient failure from a permanent one.
4. Name what a dead letter channel needs around it.

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
cd messaging-integration-patterns/dead-letter-channel-pattern
./gradlew -q run
```

Act one: what was stuck, and how many attempts? Act two: what was handled? Act three: what did the dead letter record? Act four: which order was not dead-lettered? Act five: in what order was order two handled? Act six: how many were lost, and who was told?

## Exercises

1. Add an alert that fires when the dead letter count passes five.
2. Add a delay between attempts that doubles each time.
3. Make replay put the message back in its original place.

Close with the verdict: a limit, a reason kept, an alert, an owner, and consumers safe to replay.

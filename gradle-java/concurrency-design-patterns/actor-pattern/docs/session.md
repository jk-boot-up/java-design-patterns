# Session Guide — Actor Pattern

A 60-minute session built around one question: how do you keep shared state right without locking it?

## Learning Objectives

1. Show an update lost in shared state.
2. Show an actor losing none.
3. Say why replies are messages.
4. Say what a restart does.

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
cd concurrency-design-patterns/actor-pattern
./gradlew -q run
```

Act one: which reservation was lost? Act two: what was left? Act three: what did the refusal say? Act four: how do you learn the stock? Act five: what happened to the stock after the crash? Act six: why did two actors wait for ever?

## Exercises

1. Make the actor keep its stock across a restart, and decide where to keep it.
2. Add a payment actor, and have the order ask inventory and payment without blocking.
3. Give the mailbox a limit, and decide what a sender should do when it is full.

Close with the verdict: one owner, immutable messages, no waiting inside a handler, and a clear rule for restarts.

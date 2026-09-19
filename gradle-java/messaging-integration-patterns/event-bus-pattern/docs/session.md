# Session Guide — Event Bus Pattern

A 60-minute session built around one question: what does one shared bus replace, and what does it hide?

## Learning Objectives

1. Count the references with and without a bus.
2. Subscribe by type and by supertype.
3. Show failure isolation.
4. Show a dead event and a leaked subscription.

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
cd messaging-integration-patterns/event-bus-pattern
./gradlew -q run
```

Act one: how many references? Act two: how many with a bus? Act three: what did the supertype subscriber hear? Act four: who still heard the event? Act five: where did the unheard event go? Act six: how many subscribers were held?

## Exercises

1. Add a subscriber that unsubscribes itself after its first event.
2. Add an ordering guarantee for subscribers, by a priority.
3. Make the bus deliver on another thread, and see what a failing subscriber does then.

Close with the verdict: typed events, cancelled subscriptions, dead events heard, and a map of who reacts to what.

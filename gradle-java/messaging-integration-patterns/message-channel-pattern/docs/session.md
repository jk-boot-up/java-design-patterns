# Session Guide — Message Channel Pattern

A 60-minute session built around one question: what does a channel between two systems buy, and what does it cost?

## Learning Objectives

1. Say what a channel does while the receiver is down.
2. Say what is in an envelope.
3. Explain why a channel has a type and a limit.
4. Name what the sender loses.

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
cd messaging-integration-patterns/message-channel-pattern
./gradlew -q run
```

Act one: how many checkouts failed? Act two: how many messages were waiting? Act three: in what order did the warehouse work? Act four: which headers were readable? Act five: which message was refused? Act six: how many were refused when it filled?

## Exercises

1. Make the channel drop the oldest message when full, and decide what it costs.
2. Add a reply channel, so the warehouse can say it has picked the order.
3. Add a priority header and take express messages first.

Close with the verdict: a typed, bounded channel between systems, routing information in the envelope, and a way for the sender to learn the result.

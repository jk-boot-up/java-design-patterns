# Session Guide — Dead Letter Channel with RabbitMQ Pattern

A 60-minute session built around one question: when a message dies, who decides that it is dead?

This session assumes the hand-built [Dead Letter Channel](../../dead-letter-channel-pattern) session has been taught. It does not re-teach the pattern.

## Learning Objectives

1. Say, in plain words, what a queue, an exchange and a dead letter exchange are.
2. Say the difference between refusing a message and asking for it back, and what each one does to the messages behind it.
3. Name the three reasons RabbitMQ records for a death, and say which of them an application could not have produced.
4. Say what a replay costs: the order, and the broker's note.
5. Name what a parked queue needs around it before it is safe to have one.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The scenario, and asking for it back for ever |
| 0:08–0:22 | The rule on the queue, and who does the moving |
| 0:22–0:34 | The note the broker attaches, and the three reasons |
| 0:34–0:44 | Replay, and what it does not restore |
| 0:44–0:52 | The bill, and what the simulation left out |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd messaging-integration-patterns/dead-letter-channel-with-rabbitmq-pattern
./gradlew -q run
```

Act one: how many of the twelve turns went to the same order, and how many good orders never moved? Act two: how many deliveries in all, and which order failed once and still went through? Act three: what three things does the broker's note say? Act four: which two deaths did no worker choose, and what is the broker's word for each? Act five: where in the line did the replayed order end up, and what happened to the note? Act six: how many orders were parked, and what did the working queue report?

The question to keep coming back to: at each step, is this the application deciding, or the broker?

## Exercises

1. Change the time limit in act four from five hundred milliseconds to five seconds and predict, before running it, whether the demo still finishes and why the wait is safe.
2. Give the parked queue a time limit of its own, so a parked order eventually dies again, and decide where it should go next.
3. Make the replay copy the broker's note onto the republished message, so that an order that dies twice can be told from one that dies once.
4. Change the queue in act five so that instead of pushing the oldest order out when full, it refuses the newest at the point of publishing, and say which behaviour you would want for orders and why.

Close with the verdict: write the rule on the queue, let the broker do the moving, read the note it leaves, and put an alert, an owner and a time limit on the parked queue before you ever need them.

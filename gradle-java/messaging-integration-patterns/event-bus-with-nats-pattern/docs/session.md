# Session Guide — Event Bus with NATS Pattern

A 60-minute session built around one question: what does a bus that keeps nothing give you, and what does it quietly take away?

## Learning Objectives

1. Say what publishing to this bus does, and what it does not do.
2. Explain subject names, and what a star and an arrow match.
3. Show an event being missed, and explain why waiting cannot prove it.
4. Say which of the two real brokers you would pick, and why.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, the container runtime, and the dependency |
| 0:10–0:25 | Acts one to three: the wiring cost, the fan-out, the names |
| 0:25–0:42 | Acts four and five: isolation, and the event nobody hears |
| 0:42–0:52 | Act six: the cost, and the contrast with the durable log |
| 0:52–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd messaging-integration-patterns/event-bus-with-nats-pattern
./gradlew -q run
```

Act one: how many wires do five services need without a bus? Act two: what was checkout told about its listeners? Act three: how many events did the star listener get, and how many did the arrow listener get? Act four: who reacted after the email service threw? Act five: what was the first event the warehouse ever received, and what does that prove? Act six: who was able to say how many listeners there were?

## The one to slow down on

Act five. Ask the room how they would prove that the warehouse missed the first order. Somebody will say "wait a while and check nothing arrived". Take that seriously and then take it apart: how long is a while, and what would you conclude on a slow machine? Then give them the answer the code uses. The warehouse's very first event is the second order. Delivery on one name is ordered, so the first order cannot still be in flight. It was never coming. No waiting, no guessing.

## Exercises

1. Add a loyalty service listening to `store.payments.taken`, and confirm it hears the payment and not the order.
2. Remove the call that waits for the server to confirm a subscription, run it several times, and watch an event go missing.
3. Make a service listen to `store.>` and print everything, then publish a new kind of event and see that nothing had to change.
4. Read the Kafka project beside this one, and write two sentences saying which trade you would take for order events, and why.

Close with the verdict: use this bus for announcements, name subjects for facts in the past tense, confirm the subscription before you publish, and if losing an event would cost a customer money, use a durable log instead.

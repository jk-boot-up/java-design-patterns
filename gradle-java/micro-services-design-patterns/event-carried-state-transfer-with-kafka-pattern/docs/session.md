# Session Guide — Event-Carried State Transfer with Kafka Pattern

## Learning Objectives

By the end of the session you can:

- Publish state events keyed by entity to a compacted topic.
- Build a local copy by reading a topic from the beginning.
- Explain why a key keeps order.
- Delete with a tombstone.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Thin events and call-backs | 7 min |
| 0:17 | Act 2: The address in the event | 7 min |
| 0:24 | Act 3: A new copy from the topic | 7 min |
| 0:31 | Act 4: Order within a partition | 7 min |
| 0:38 | Act 5: Deleting is an event | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's 0 of 100 with act
two's 100 of 100. Open `ShippingCopy.apply`: put, or remove on a tombstone.
End on act four's two results.

## Exercises

1. Keep a consumer running and apply new events as they arrive, instead of re-reading.
2. Rebuild the copy with a Kafka Streams `KTable`.
3. Publish only the city and postcode, and see what shipping can still do.

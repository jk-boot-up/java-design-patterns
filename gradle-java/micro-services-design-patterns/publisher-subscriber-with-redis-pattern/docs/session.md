# Session Guide — Publisher-Subscriber with Redis Pattern

A 60-minute session built around one question: once the topic is a real server that every subscriber reaches over its own connection, what does it keep, what does it tell the publisher, and what does it do with a subscriber that stops reading?

## Learning Objectives

1. Say, in plain words, what publishing, a channel, subscribing, a pattern subscription and the output buffer are.
2. Show one publish reaching a subscriber in a second Java process.
3. Read the number `PUBLISH` hands back, and say what it does not tell you.
4. Explain why a late subscriber sees nothing that was published before it joined.
5. Explain what Redis does with a subscriber that falls too far behind, and why.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The live radio analogy, and the partner project recapped in two minutes |
| 0:08–0:18 | Acts one and two: calling by name, then one publish and a second process |
| 0:18–0:28 | Acts three and four: the late subscriber, and the star |
| 0:28–0:42 | Act five: the pile, the limit and the cut-off |
| 0:42–0:50 | Act six: the bill |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/publisher-subscriber-with-redis-pattern
./gradlew -q run
```

Act one: how many services does the order service know by name? Act two: what did Redis answer, and how many programs were listening? Act three: what did loyalty see, and how many keys did Redis store? Act four: why did the cancelled order reach only one receiver? Act five: how many listeners were cut off, what happened to the count on the next publish, and was the publisher ever told? Act six: what did email get when it came back?

Then open `src/main/java/com/jk/explore/pubsubredis/Subscriber.java` and read `take` aloud. The subscriber that "stops reading" is only a handler that does not return; Redis cannot tell that apart from a service stuck on a slow database call.

## Discussion

Ask the room which store events could be sent this way. A live "3 people are viewing this item" count, perhaps, where a missed update is replaced by the next one. An order that has to be picked, never.

Then ask who should notice a cut-off. The publisher is never told and the subscriber only sees its connection end. The one place it is recorded is Redis's own counter, `client_output_buffer_limit_disconnections`, which somebody has to be watching.

## Exercises

1. Raise the limit in the fifth act to `8mb` and predict whether analytics is still cut off. Then run it.
2. Leave analytics reading in the fifth act and confirm nobody is cut off. What stops the loop?
3. Change the sixth act so email subscribes before the publish, and predict the count Redis answers.
4. Subscribe analytics to `orders.*` and email to both `orders.placed` and `orders.cancelled`, and predict every count in act four.
5. Start the loyalty process twice in act two, and predict what `PUBLISH` answers.

Close with the verdict: subscribe before you need it, keep every listener reading and watch the cut-off counter, and use something that keeps a log if a missed order would matter.

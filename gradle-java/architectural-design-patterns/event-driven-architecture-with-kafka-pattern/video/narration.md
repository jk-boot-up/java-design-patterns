# Event-Driven Architecture with Kafka Pattern — Video Narration Script

## 1. Event-Driven Architecture with Kafka

Hello, and welcome. This video explains the Event-Driven Architecture pattern with Apache Kafka, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Event-Driven Architecture video. That one showed services that write facts to an append only log, and read it at their own pace. It showed a service that is down catching up, a new reader replaying history, briefly wrong stock, and a duplicate delivery absorbed by a check. This one shows the same idea inside Apache Kafka. The plain definition, in short: with Kafka, the log is a topic on a broker, and each service reads it as a consumer group that the broker remembers. By the end you will see an order lost because shipping was down, see the order service send to a real broker, see a service catch up from its remembered offset, see a new reader replay history, see the system briefly inconsistent, and see the bill, which is duplicates and a broker to run.

## 2. The Partner Project

This video assumes the Event-Driven Architecture video. If you have not seen it, start there. It writes facts to a log, and shows readers at their own pace, a reader that was down catching up, and a new reader replaying history. This one uses the same example. It does not teach the pattern again. It shows what Apache Kafka does with it.

## 3. Before The First Line

Before the first line of code, what Apache Kafka is. Kafka is a system that keeps a log of events on a server, called a broker. Producers add events to a topic. Consumers read the topic, and the broker remembers how far each group of consumers has read. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Calling And Waiting

First, calling each other. The order service calls shipping, and waits. Shipping is down. The order is not accepted. A customer lost an order because a service they never see was down.

## 5. Telling The Log

Second, telling the log. The order service sends the event to Kafka, which gives it offset zero, and it finishes. It has no reference to inventory or shipping. Both read the topic, and both see the order.

## 6. A Service That Is Down

Third, a service that is down. Shipping read the first order, and then went down. Three more orders were accepted. Shipping is three events behind, as the broker counts it. Shipping came back and caught up, from where it stopped. It has now planned four orders, and is none behind.

## 7. A New Reader

Fourth, a new reader. Analytics is added after two orders. It reads the topic from the start, and sees both. The order service was not touched. Kafka keeps the events, so a new service can be built from history.

## 8. Not The Same Instant

Fifth, not the same instant. The order is accepted, and stock in the warehouse is still ten. It should be nine. After inventory reads the topic, it is nine. For a moment, the two disagree. The system is eventually consistent, not consistent at every instant.

## 9. The Bill

Last, the bill. The same event is delivered twice, as Kafka may after a missed commit. Without a duplicate check, stock is eight. With one, it is nine, which is right. The flow of an order is now spread over several services, so to see it, you read the topic, not one piece of code. And a broker is another system to run.

## 10. The Verdict

My verdict, plainly. Use a broker when services must not depend on each other being up, and when new services will come. Give each service its own group. Expect readers to be behind, and design for it. Make every reader safe to repeat. And watch the lag.

## 11. How To Recognise It

How do you recognise this in code you did not write? KafkaProducer and KafkaConsumer, or @KafkaListener. A group.id for each service. Lag dashboards, and kafka-consumer-groups.sh.

## 12. Where You Have Met This

You have met this in most large event-driven systems: order pipelines, activity feeds and change data capture.

## 13. What Was Used

For the record. Apache Kafka, 4.3.1. Docker, 24 or later.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real broker in a container, real offsets, and real consumer groups. Each act uses its own one partition topic, so the counts are exact.

## 15. When This Is Too Much

So when is it too much? For a small system where all parts are always up together, a direct call is simpler. A broker is a system to run, and to understand.

## 16. Thanks for Watching

That's Event-Driven Architecture with Kafka. If you take one sentence away, take this one: Kafka keeps the log and each service's place in it, and the price is a broker to run, and readers that may see an event twice. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a third reader for a loyalty service, and read the topic from the start. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.

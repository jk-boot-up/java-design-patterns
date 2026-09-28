# Event-Driven Architecture with Kafka Pattern — Video Narration Script

## 1. Event-Driven Architecture with Kafka

Hello, and welcome. This video explains the Event-Driven Architecture pattern, in Java, using Apache Kafka. This video is presented by Jayasekhar Konduru. First, a simple definition. In an event-driven system, services do not call each other. They write facts, called events, to a shared log, and each service reads that log at its own pace. With Kafka, that log is called a topic, and it lives on a server called a broker. The broker also remembers how far each reading service has got. Think of a library that keeps a bookmark for every reader. You can leave for a week, come back, and carry on from the right page. This is the framework version of the Event-Driven Architecture video. We keep the same online store, and watch a real Kafka broker do the work. We will lose an order the old way, then send events to Kafka, catch up after an outage, replay history, and finally, look at the cost.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Event-Driven Architecture video. That one builds the log itself, in plain Java. It shows readers working at their own pace, a reader catching up, and a new reader replaying history. If you are new to the pattern, watch that one first. Here, we keep the same example. We won't teach the pattern again. Instead, we ask what a real tool, Kafka, does with it.

## 3. Before The First Line

So, what is Apache Kafka? Kafka keeps a log of events on a server, called a broker. Programs that write events are called producers. They add events to a topic. Programs that read events are called consumers. Consumers work in named groups, and the broker remembers how far each group has read. To run the demo, you need Docker running, because the broker runs in a container. Without Docker, the demo tells you so, and stops. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. Calling And Waiting

First, the old way: services calling each other. The order service calls shipping, and waits for an answer. But shipping is down. So the order is not accepted. A customer just lost their order, because of a service they never even see.

## 5. Telling The Log

Second demo: telling the log. The order service sends its event to Kafka. Kafka stores it at position zero, called offset zero. And the order service is finished. It knows nothing about inventory or shipping. Inventory reads the topic, and sees the order. Shipping reads the same topic, and sees it too.

## 6. A Service That Is Down

Third demo: a service that is down. Shipping reads the first order, and then goes down. Three more orders arrive, and all three are accepted. The broker reports that shipping is three events behind. This gap is called lag. Then shipping comes back. The broker remembers exactly where it stopped. So shipping carries on from there, and plans all four orders. Now the lag is zero.

## 7. A New Reader

Fourth demo: a new reader. After two orders have been placed, we add a brand new service: analytics. It reads the topic from the very beginning. So it sees both earlier orders. And the order service was not changed at all. Kafka keeps the events, so a new service can be built from history.

## 8. Not The Same Instant

Fifth demo: things do not happen at the same instant. An order is accepted. But the stock count still says ten. It should say nine. A moment later, inventory reads the event, and the count becomes nine. For that short moment, the two services disagree. This is called eventual consistency. The system becomes correct, but not at every single instant.

## 9. The Bill

Finally, the cost. Kafka can deliver the same event twice, for example when a reader crashes before saving its place. Without a duplicate check, the stock drops twice, to eight. That is wrong. With a duplicate check, it stays at nine, which is right. Second, the journey of one order is now spread across several services. To follow it, you read the topic, not one piece of code. And third, the broker is one more system you have to run.

## 10. The Verdict

So, here is the verdict. Use a broker when services must not depend on each other being up, and when new services will join later. Then follow four rules. One. Give each service its own consumer group. Two. Expect readers to be behind, and design for it. Three. Make every reader safe to run twice on the same event. And four. Watch the lag.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for the Kafka Producer and Kafka Consumer classes. Or a method marked with the at Kafka Listener annotation. Look for a group I D setting for each service. And look for dashboards that show lag, or the Kafka consumer groups command line tool.

## 12. Where You Have Met This

Where have you met this before? In most large event-driven systems. Order pipelines, activity feeds, and systems that copy database changes to other services.

## 13. What Was Used

For the record, here are the versions. Apache Kafka, four point three point one. And Docker, version twenty-four or later.

## 14. What Is Real Here

A quick, honest note about this demo. Everything in it is real. A real broker, running in a container, with real offsets, and real consumer groups. Each demo uses its own topic, with a single partition, so every count you heard is exact.

## 15. When This Is Too Much

So, when is this too much? In a small system where every part is always up together, a direct call is simpler. A broker is another system to run, and another system to understand.

## 16. Thanks for Watching

That's Event-Driven Architecture with Kafka. If you remember one sentence, make it this one. Kafka keeps the log, and each service's place in it, and the price is a broker to run, and readers that may see an event twice. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a third reader, for a loyalty points service. And have it read the topic from the very start. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

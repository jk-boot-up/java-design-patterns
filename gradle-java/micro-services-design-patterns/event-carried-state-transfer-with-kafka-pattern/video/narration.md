# Event-Carried State Transfer with Kafka Pattern — Video Narration Script

## 1. Event-Carried State Transfer with Kafka

Hello, and welcome. This video explains Event-Carried State Transfer, with a real Kafka broker, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When data changes, the new data travels in the event itself. So every service that cares can keep its own copy, and never call the owner back. Kafka is an open-source event platform that keeps events on topics, so a copy can be built from them at any time. Think of a town noticeboard of address changes. A new postman reads the board once, and knows every current address. In this video, the domain is an online shop, whose shipping service prints labels, and whose customer service owns the addresses. By the end, you will hear how a Kafka topic becomes shipping's copy. How keys keep events in order. And how a deletion travels too.

## 2. The Scenario

Here is the scenario. The shipping service prints delivery labels. The customer service owns the addresses. Shipping used to call it for every label. When it was down, no labels were printed.

## 3. Act One — Thin events and call-backs

First demo: thin events on Kafka, and a call back for every label. Each event says only, this customer changed. So shipping still asks the customer service for every address. A hundred labels. A hundred calls. The customer service goes down. Not one label can be printed.

## 4. Act Two — The address in the event

Second demo: the event carries the address. Each event is keyed by the customer, on a topic that keeps the latest per customer. Shipping reads the topic into its own copy. Ten addresses. The customer service is still down. All hundred labels are printed. No calls at all.

## 5. Act Three — A new copy from the topic

Third demo: a new copy, from the topic. A customer moves, from Leeds to York. A brand-new shipping instance starts with nothing. It reads the topic from the beginning. Eleven events, for ten customers. The latest event wins. Its label goes to York. The old copy has not read the new event yet. It still says Leeds.

## 6. Act Four — Order within a partition

Fourth demo: Kafka keeps order only within a partition. A customer moves to Hull, then to Bristol. Sent to two different partitions, and read in the wrong order, the copy ends on Hull. The older address. Keyed by the customer, both events go to the same partition, in order. The copy ends on Bristol. No version numbers needed.

## 7. Act Five — Deleting is an event

Fifth demo: the bill. Customer three closes the account. The customer service sends a special event, with no address at all. Kafka calls it a tombstone. A copy built from the topic now holds nine addresses. Customer three is gone. Every service with a copy must honour it. Or the address lives on. And every copy is more data to store, and protect.

## 8. The Pattern, in Kafka

Let's name the pattern, in Kafka's words. Events carry the address. Keyed by customer, so each customer's events stay in order. On a compacted topic, which keeps the latest per customer. And tombstones, to say a customer is gone.

## 9. Who Does What

Here is who does what. The Kafka class runs a real broker in a container, and sends and reads events. The customer service owns the addresses. And shipping's copy is built only from the events on the topic.

## 10. Where You Have Seen It

You have probably met this already. Compacted Kafka topics, used as a service's own table. Kafka Streams tables, which are exactly this local copy. And change data capture, which publishes every changed database row.

## 11. When To Use It

So, when should you use it? When many services read the same data often, and must keep working when its owner is down. Key events by the entity. Honour tombstones. And copy only the fields you need.

## 12. Thanks for Watching

That's Event-Carried State Transfer, with Kafka. If you remember one sentence, make it this one. Put the data in the event, key it by who it is about, and let every service keep its own copy. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts Kafka for you. Here is one exercise to try. Keep a consumer running, and apply new events as they arrive. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

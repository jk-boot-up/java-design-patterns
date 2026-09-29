# Backpressure Pattern — Video Narration Script

## 1. Backpressure

Hello, and welcome. This video explains the Backpressure pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Backpressure lets a slow consumer tell a fast producer to slow down. So the work waiting in between stays small, instead of filling memory. Think of a busy restaurant. If the waiters take orders faster than the chefs can cook, the ticket rail overflows. A good kitchen tells the front of house to stop seating tables for a while. The pressure travels back, from the kitchen to the door. In this video, the domain is an online shop's search indexer. It reads a supplier's product feed, which is much faster than the indexer. By the end, you will hear how the waiting pile grows without limit. Three ways to push back. And what backpressure costs.

## 2. The Scenario

Here is the scenario. The shop's search indexer reads a supplier's product feed. The supplier sends a thousand products a second. The indexer can handle a hundred. Everything it has not reached yet waits in memory.

## 3. Act One — No backpressure

First demo: no backpressure. The supplier sends a thousand products a second. The indexer handles a hundred. Everything not yet indexed waits in memory. After ten seconds, nine thousand products are waiting. And the pile grows by nine hundred every second. A bigger feed, and the service runs out of memory.

## 4. Act Two — A bounded buffer

Second demo: a bounded buffer. The buffer holds at most five hundred products. When it is full, the supplier waits. Never more than five hundred are waiting. All ten thousand are indexed, in a hundred seconds. The supplier has been slowed to the indexer's pace.

## 5. Act Three — Ask for what you can handle

Third demo: the consumer asks for what it can handle. Java has this built in, in the Flow interfaces. The indexer asks for ten products. It indexes them. Then it asks for ten more. The supplier never sends anything that was not asked for. All ten thousand are indexed. And never more than ten are in flight.

## 6. Act Four — Keep only the latest

Fourth demo: when only the latest value matters, drop the rest. The warehouse sends a thousand stock-level updates, for ten products. The shop only needs the current stock level. So it keeps one pending value per product. A newer one replaces the older one. Only ten updates are delivered. The latest for each product.

## 7. Act Five — The bill

Fifth demo: the bill. Backpressure does not make the work faster. It moves the waiting upstream. The supplier's feed took a hundred seconds, instead of ten. So the supplier must cope with being slowed. And dropping is only safe when the latest value is all that matters. Never for orders, or payments.

## 8. The Pattern

Let's name the pattern. The consumer controls the pace, not the producer. There are three common ways. Bound the buffer, so the producer waits when it is full. Let the consumer ask for a batch at a time. Or, when only the latest value matters, drop the older ones.

## 9. Who Does What

Here is who does what. The publisher is the supplier's feed. It sends only as many products as it has been asked for. The indexer is the subscriber. It asks for ten, indexes them, then asks again. The conflator keeps one pending stock level per product. And the feed simulation compares an unbounded buffer with a bounded one.

## 10. Where You Have Seen It

You have probably met this pattern already. Java's Flow interfaces are the Reactive Streams standard. Reactor, RxJava and Akka Streams are all built on it. A bounded blocking queue makes the producer wait when it is full. And the network itself does it. TCP slows the sender when the receiver cannot keep up.

## 11. When To Use It

So, when should you use it? Whenever a fast source can outrun a slow consumer for long. Bound every buffer. Prefer consumers that ask for work. Drop only data where the latest value is enough. And make sure the producer can cope with being slowed.

## 12. Thanks for Watching

That's the Backpressure pattern. If you remember one sentence, make it this one. Let the slow side set the pace, or memory will set it for you. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Replace the hand-written publisher with the JDK's submission publisher. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

# Backpressure with Project Reactor Pattern — Video Narration Script

## 1. Backpressure with Project Reactor

Hello, and welcome. This video explains the Backpressure pattern, built with Project Reactor, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Backpressure lets a slow consumer tell a fast producer how much it can take. So work does not pile up in between. Project Reactor is an open-source library for streams of data, and every stream in it carries this demand. Think of a kitchen where the chef calls, two more tickets, and the waiter hands over exactly two. A waiter who ignores the chef is stopped before the rail overflows. In this video, the domain is an online shop's search indexer, reading a supplier's product feed. By the end, you will hear what Reactor does with a source that ignores demand. How to ask in batches. And how to keep only the latest update.

## 2. The Scenario

Here is the scenario. A supplier's feed sends ten thousand products, as fast as it can. The search indexer takes a millisecond for each. And stock-level updates arrive by the thousand, though only the current one matters.

## 3. Act One — A source that ignores demand

First demo: a source that ignores demand. The supplier's feed pushes ten thousand products, as fast as it can. It ignores how many the indexer asked for. The indexer's queue holds two hundred and fifty-six. Reactor does not let the pile grow. It stops the stream, with an overflow error. Only part of the feed is indexed. The rest is refused, not quietly piled up.

## 4. Act Two — Produce only what is asked

Second demo: a feed that produces only what is asked for. The indexer asks for ten products. It indexes them. Then it asks for ten more. All ten thousand are indexed. And never more than ten were waiting to be delivered.

## 5. Act Three — limitRate

Third demo: let Reactor do the asking. The limit rate operator asks for ten. Then, each time three-quarters have been used, it asks for eight more. So the next batch is already on its way, and the indexer never waits.

## 6. Act Four — Only the latest

Fourth demo: only the latest matters. A thousand stock-level updates arrive, for one mug. The shop asks for one, and later for one more. It gets the first, a thousand. And the latest, one. Everything in between was dropped. Only the current level matters.

## 7. Act Five — The bill

Fifth demo: the bill. Every source must choose. A source that can wait, like a database cursor, is simplest. A source that cannot wait must buffer, which costs memory. Or drop, or keep only the latest, which loses data. Reactor makes you say which. And a buffer with no limit just hides the pile.

## 8. The Pattern, in Reactor

Let's name the pattern, in Reactor's words. Subscribers request items. Sources send no more than requested. Limit rate asks in batches, for you. And the on backpressure operators say what to do with items produced while nobody is asking.

## 9. Who Does What

Here is who does what. A flux is the feed, a stream of products. A base subscriber is the indexer, asking for ten at a time. Limit rate asks in batches for you. And on backpressure latest keeps only the newest stock level.

## 10. Where You Have Seen It

You have probably met this already. Spring WebFlux is built on Reactor. RxJava, Akka Streams, and Kotlin Flow share the same ideas. And the JDK has the same interfaces, in its Flow class.

## 11. When To Use It

So, when should you use it? Whenever data streams between fast and slow parts of a system. Prefer sources that can wait. And when one cannot, bound it, drop, or keep the latest, on purpose.

## 12. Thanks for Watching

That's Backpressure, with Project Reactor. If you remember one sentence, make it this one. Let the consumer set the pace, and decide on purpose what happens when a source cannot wait. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Use on backpressure drop in the stock demo, and print what is dropped. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

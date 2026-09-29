# Resequencer Pattern — Video Narration Script

## 1. Resequencer

Hello, and welcome. This video explains the Resequencer pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When numbered messages can arrive out of order, a resequencer holds the early ones. It releases each sequence strictly in order. And it has a limit, so a lost message cannot block everything for ever. Think of a long letter sent in five numbered envelopes, delivered in a muddle. You read envelope one, put three aside, and wait for two. And if three is lost for good, at some point you read on without it. In this video, the domain is an online shop. Its order page shows status updates: placed, paid, packed, shipped, and delivered. By the end, you will hear what goes wrong when updates are applied as they arrive. How a resequencer fixes it. How it handles many orders. And what a lost message costs.

## 2. The Scenario

Here is the scenario. Each order goes through five statuses. Placed, paid, packed, shipped, delivered. The updates pass through several workers, running in parallel. So they reach the order page in a muddle. Each update carries a number, one to five.

## 3. Act One — Applied as they arrive

First demo: status updates applied as they arrive. Five updates for Priya's order. Placed, paid, packed, shipped, delivered. They arrive in a muddle: one, three, two, five, four. The page shows each as it comes. Packed before paid. Delivered, then shipped. The page ends on shipped. But the parcel was delivered.

## 4. Act Two — A resequencer

Second demo: a resequencer puts them back in order. It sits in front of the page. It only passes on the next number it expects. The customer now sees: placed, paid, packed, shipped, delivered. The page ends on delivered.

## 5. Act Three — Hold and release

Third demo: early messages wait, and late ones release them. Number one is released at once. Number three arrives early. It is held. Number two arrives. It is released, and so is the three that was waiting. Number five is held, until four arrives. Then both go through.

## 6. Act Four — One sequence per order

Fourth demo: each order has its own sequence. Updates for two orders arrive, all mixed together. Each order's updates are released in that order's own sequence. Neither order waits for the other.

## 7. Act Five — The bill

Fifth demo: the bill. Another order's update number three is lost. Number four arrives, and is held. The page still says paid. Number five arrives. Now two are waiting, the limit. The resequencer gives up on three, and releases four and five. The page says delivered. Packed was never shown. And without a limit, the page would have waited for ever.

## 8. The Pattern

Let's name the pattern. Number each message, per order. Release only the number that is expected next. Hold anything that arrives early. Keep a separate sequence for each order. And set a limit, for gaps that will never fill.

## 9. Who Does What

Here is who does what. A status update carries the order, its number, and the status. The resequencer keeps, for each order, the next number it expects, and the updates it is holding. And the order page shows whatever it is given.

## 10. Where You Have Seen It

You have probably met this pattern already. Apache Camel has a resequence step. The internet's T C P protocol puts packets back in order, using sequence numbers. And Kafka keeps messages in order per key, which is one way to avoid needing a resequencer.

## 11. When To Use It

So, when should you use it? When order matters, and delivery does not keep it. Number messages per key. Put a limit on the buffer. And decide what to do about gaps. And if you can choose a transport that keeps order per key, prefer that.

## 12. Thanks for Watching

That's the Resequencer pattern. If you remember one sentence, make it this one. Hold what comes early, release in order, and never wait for ever. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Give up on a gap after two seconds, instead of after two held messages. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

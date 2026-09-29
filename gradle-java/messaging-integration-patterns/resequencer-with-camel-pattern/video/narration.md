# Resequencer with Apache Camel Pattern — Video Narration Script

## 1. Resequencer with Apache Camel

Hello, and welcome. This video explains the Resequencer pattern, built with Apache Camel, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A resequencer puts messages that arrived out of order back in order. Using a number each message carries. Apache Camel is an open-source library for moving messages, and it has a resequencer built in. Think of a sorting office receiving the numbered pages of a letter, out of order. It can pass pages on as soon as the next one arrives. Or wait for the whole bundle, and sort it. In this video, the domain is an online shop's order-tracking page, and the status updates it shows. By the end, you will hear Camel's two modes, stream and batch. What each makes the customer wait for. And what happens when an update is lost.

## 2. The Scenario

Here is the scenario. The tracking page shows five updates. Placed, paid, packed, shipped, delivered. They travel different paths, and arrive out of order. The page ended on shipped, although the parcel was delivered.

## 3. Act One — Applied as they arrive

First demo: updates applied as they arrive. They arrive in the order one, three, two, five, four. The customer sees placed, packed, paid, delivered, shipped. The page ends on shipped. But the parcel was delivered.

## 4. Act Two — Stream mode

Second demo: Camel's resequencer, in stream mode. Each update is released as soon as all the earlier ones have been seen. The page shows placed, paid, packed, shipped, delivered. In order. One surprise. The very first update waited about a third of a second. Camel cannot know that number one is the first. So it waits one timeout.

## 5. Act Three — Batch mode

Third demo: batch mode. Camel collects a group of five, sorts it, and releases it together. After four updates, the page shows nothing at all. The fifth arrives. All five appear at once, in order. Never out of order. But the customer waits for the whole group.

## 6. Act Four — Two orders at once

Fourth demo: two orders at once. Updates for two orders arrive mixed together. Camel's stream mode keeps one sequence for everything. It cannot keep two orders apart. Batch mode sorts by order, then by number. Order two's updates come out in order. Then order three's.

## 7. Act Five — The bill

Fifth demo: the bill. Update three is lost. Updates four and five arrive. They wait. The page stays on paid. After about half a second, Camel gives up on number three. The page says delivered. A short timeout gives up on late messages quickly. A long one leaves the customer on an old status for longer.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. The resequence step, given each message's number. Stream mode releases each message as soon as the ones before it have gone. Batch mode collects a group, sorts it, and releases it together.

## 9. Who Does What

Here is who does what. Shop routes holds three routes. Straight through, stream, and batch. The resequence step holds messages, and releases them in order. And the order page is what the customer sees.

## 10. Where You Have Seen It

You have probably met this already. Camel's resequence step, and Spring Integration's resequencer. The network does it too. TCP puts packets back in order before your program sees them. And Kafka keeps order within a partition.

## 11. When To Use It

So, when should you use it? When updates travel different paths, and their order matters. Use stream mode to show updates soon. Batch mode when nothing may ever appear out of order. And choose the timeout on purpose.

## 12. Thanks for Watching

That's the Resequencer, with Apache Camel. If you remember one sentence, make it this one. Put messages back in order, and decide how long to wait for a missing one. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Set the timeout to two seconds, and time how long the page stays on paid. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

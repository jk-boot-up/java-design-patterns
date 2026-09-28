# Splitter and Aggregator Pattern — Video Narration Script

## 1. Splitter and Aggregator

Hello, and welcome. This video explains the Splitter and Aggregator pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A splitter breaks one message into several smaller ones. Each piece carries an I D, and its place, like part two of three. An aggregator collects the pieces by that I D, and puts them back together as one. Think of a group shopping trip. One list is torn into three, and each friend fetches their part. At the till, everything is put back together into one basket. In our online store, one order has lines in aisles far apart, and several people pick it at once. In this video, we split an order, let the parts finish out of order, and put it back together. We will handle a missing part with a timeout. And then hear the cost.

## 2. The Scenario

Here is the scenario. An order has three lines, in aisles far apart. One picker does them one after another. Meanwhile, other pickers stand idle. So here is the question. Can we split the order between pickers, and put it back together afterwards?

## 3. One Message, One Picker

First, the simple way: one message, one picker. An order of three lines is picked by one person, one line after another. Three steps in a row, in aisles far apart. While the other pickers stand idle.

## 4. The Pattern

Now, the pattern. A splitter breaks the order into one message for each line. Each message carries the order's I D, and its own place: for example, part two of three. Then an aggregator collects them by the I D. And puts them back together.

## 5. Split It

Second demo: split it. The order becomes three parts. Part one of three. Part two of three. Part three of three. Each part carries the order's I D, and its own place. That is what makes it possible to put them back together.

## 6. The Parts Finish In Any Order

Third demo: the parts can finish in any order. Suppose the three pickers finish in the order three, then one, then two. Nothing guarantees the parts come back in the order they went out.

## 7. Gather Them By The Id

Fourth demo: gather them by the I D. Part three arrives, and the aggregator waits. Part one arrives, and it waits. Part two arrives, and the order is complete. The three lines are back in their original order. Even though they arrived out of order.

## 8. A Part Never Arrives

Fifth demo: a part never arrives. Parts one and three arrive. But part two's picker has gone home. After twenty-nine minutes, the aggregator is still waiting. After thirty, it gives up. It has two of the three lines. Part two is named as missing. And the result says clearly that it is not complete. Without a timeout, it would wait forever. And so would the customer.

## 9. The Bill

Finally, the cost. A thousand orders, each missing one part, means a thousand orders held in memory, waiting. A part delivered twice must be counted only once. Here, it is, and the duplicate is noted. And two orders sharing the same I D would get mixed into one. So the I D that ties the parts together must be unique.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for messages that carry a correlation I D, a sequence number, and a total count. Look for Spring Integration's splitter and aggregator, or Apache Camel's split and aggregate. Look for a map, keyed by an I D, holding what has arrived so far. And look for a timeout on collecting the results of a batch.

## 11. The Verdict

So, here is the verdict. Use a splitter and aggregator when one message contains parts that can be worked on separately. And when the work is slow enough that doing it in parallel pays off. Number every part, and carry the I D and the total. Collect with a timeout. Ignore duplicates. And decide what to do with a partial result. Also, keep an eye on how many orders are waiting to be completed.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Time is simulated, not read from the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If the parts are quick, or depend on each other, splitting is just overhead. And if the order between the parts matters, the aggregator needs more than just the parts.

## 14. Thanks for Watching

That's the Splitter and Aggregator pattern. If you remember one sentence, make it this one. A splitter and aggregator share work by carrying an I D and a place, and the price is state to hold, and a timeout to choose. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the aggregator reject any part whose total count disagrees with the first part it saw. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

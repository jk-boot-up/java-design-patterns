# Splitter and Aggregator Pattern — Video Narration Script

## 1. Splitter and Aggregator

Hello, and welcome. This video explains the Splitter and Aggregator pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a splitter breaks one message into several, each carrying an id and its place. An aggregator collects the pieces by that id, and puts them back together as one. This is the third project in the messaging and integration category, whose subject is how separate systems exchange messages safely. In our online store, the order with several lines, in aisles far apart, is picked by several people at once. By the end you will see an order picked by one person, see it split into parts that carry their place, see the parts finish out of order and come back together, see a missing part handled by a timeout, and see the bill, which is memory for every open order and the care duplicates need.

## 2. The Scenario

Here is the scenario. An order has three lines, in aisles far apart. One picker does them one after another, and other pickers stand idle. The question: can we split the order between pickers, and put it back together afterwards?

## 3. One Message, One Picker

First, one message, one picker. An order of three lines is picked by one person, one line after another. Three steps of work in a row, in aisles that are far apart, while the other pickers stand idle.

## 4. The Pattern

The pattern. A splitter breaks the order into one message for each line. Each carries the order's id, and its own place: part two of three. An aggregator collects them by the id, and puts them back together.

## 5. Split It

Second, split it. The order becomes three parts. Part one of three, part two of three, part three of three. Each carries the order's id, and its own place. That is what lets them be put back together.

## 6. The Parts Finish In Any Order

Third, the parts finish in any order. Suppose the three pickers finish in the order three, one, two. Nothing guarantees that the parts come back in the order they went.

## 7. Gather Them By The Id

Fourth, gather them by the id. Part three arrives, and the aggregator waits. Part one arrives, and it waits. Part two arrives, and the order is complete: the three lines, back in their original order, from parts that arrived out of order.

## 8. A Part Never Arrives

Fifth, a part never arrives. Parts one and three arrive. Part two's picker has gone home. After twenty nine minutes, nothing has expired. After thirty, the aggregator gives up. It has two of three lines, part two is named as missing, and the result says it is not complete. Without a timeout, it would wait forever, and so would the customer.

## 9. The Bill

Last, the bill. A thousand orders, each missing one part, means a thousand orders held in memory, waiting. A part delivered twice is counted once, and noted. And two orders with the same id would be mixed into one, so the id that ties the parts together has to be unique.

## 10. How To Recognise It

How do you recognise this in code you did not write? A message that carries a correlationId, a sequenceNumber and a sequenceSize. Spring Integration's splitter and aggregator, Camel's split and aggregate. A map keyed by an id, holding what has arrived so far. A timeout on collecting the results of a batch.

## 11. The Verdict

Here is my verdict, plainly. Use a splitter and aggregator when one message contains parts that can be worked on separately, and the work is slow enough that doing it in parallel pays. Number every part and carry the id and the total. Aggregate with a timeout, drop duplicates, and decide what to do with a partial result. Watch the number of open aggregations.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If the parts are quick, or depend on each other, splitting is overhead. If order matters between the parts, an aggregator needs more than the parts.

## 14. Thanks for Watching

That's Splitter and Aggregator. If you take one sentence away, take this one: a splitter and aggregator share work by carrying an id and a place, and the price is state to hold and a timeout to choose. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make the aggregator reject a part whose total disagrees with the first part it saw. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.

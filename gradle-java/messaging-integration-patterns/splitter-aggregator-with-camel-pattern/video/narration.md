# Splitter and Aggregator with Camel Pattern — Video Narration Script

## 1. Splitter and Aggregator with Camel

Hello, and welcome. This video explains the Splitter and Aggregator pattern, in Java, using Apache Camel. This video is presented by Jayasekhar Konduru. First, a simple definition. A splitter takes one message and turns it into several. Each piece carries two things: which whole it came from, and its own place in that whole. An aggregator does the opposite. It holds pieces that belong together. And sends out one message, when a rule says they are ready. In our online store, a basket has three items, in three different warehouses: Leeds, Reading, and Glasgow. The order is split into one shipment per warehouse. Each warehouse prices its own line. And the answers are gathered back into one price: two hundred and eighty-three pounds forty-two. By the end, you will hear an aggregator that waits forever, because nobody gave it a deadline. A real deadline ending that wait. And the moment Camel declares an order finished, when it is not.

## 2. The Scenario

Here is the scenario. One basket has three items. And the three products sit in three different warehouses: Leeds, Reading, and Glasgow. One worker takes the whole basket, and walks all three, one after another. While the other two warehouses do nothing. So here is the question. Can we split the order between the three warehouses, and put the answers back together?

## 3. One Picker, One Order

First, one picker, and one order. Order four four seven one has three lines, in three warehouses. One worker handles every line, one after another. Three steps of work, on one thread. And the basket comes to two hundred and eighty-three pounds forty-two. While that worker walks, the other two warehouses stand idle.

## 4. Camel's Three Words

Camel brings three words with it, and each is simpler than it sounds. A route is the path a message takes, written down. Where it starts, what happens to it, and where it goes. A correlation is the rule for reading which order a message belongs to. Here, that is the order number. And a completion condition is the rule that decides when the gathering is finished. That third word is the heart of this video. You must supply it yourself. And if you supply the wrong one, nothing ever comes out.

## 5. Camel Splits The Order

Second demo: Camel splits the order. The split step sends out one message for each line. Shipment one of three, to Leeds. Shipment two of three, to Reading. Shipment three of three, to Glasgow. Camel numbers the pieces itself. And it copies the order number onto every one of them. That number is the only thing that will put the order back together.

## 6. They Come Back In Any Order

Third demo: the answers come back in any order. The warehouses answer third, then first, then second. The aggregator does not mind. It files each answer under the place that answer says it belongs. So the result comes out in the customer's own order, totalling two hundred and eighty-three pounds forty-two. And Camel records why it finished: size. Three messages had arrived, and three were expected.

## 7. The Completion Condition

Fourth demo, and this is what the hand-built version never faced. The Glasgow warehouse is closed. Its message reaches the warehouse, and stops there. Two shipments come back, to an aggregator whose only rule is a count of three. Two is not three. No answer comes out. One order sits open. And nothing will ever change that. An aggregator with only a count is a queue of orders that will never come out.

## 8. A Deadline

Fifth demo: a deadline. The same thing happens to a second aggregator. But this one has a second rule: a deadline of six hundred milliseconds, checked every hundred. A background checker watches the clock the whole time. When the deadline passes, it ends the wait, by itself. Camel records the reason as timeout, not size. The answer carries two of three shipments. It names Glasgow as the one that never came. And it comes to two hundred and sixty-five pounds ninety-seven: the basket, without the Glasgow item.

## 9. The Whole Difference

The difference between waiting forever, and giving up, is two lines. Both aggregators gather by the order number. And both finish when the expected number of messages has arrived. The second one also names a deadline in milliseconds, and how often to check the clock. Whichever rule is met first ends the wait. So never write the count, without the deadline.

## 10. The Bill

Finally, the costs. A thousand orders, each missing one shipment, means a thousand orders held in memory. And memory is where Camel keeps them, unless told otherwise. So a restart throws every one of them away. Then the surprise. Completing by size counts messages, not different pieces. Deliver the Reading shipment twice, and three messages have arrived. So Camel declares the order finished, with only two of its three lines. The duplicate check is yours to write. With it, the customer pays two hundred and sixty-five pounds ninety-seven. Without it, they pay five hundred and fifteen pounds ninety-six.

## 11. What The Simulation Left Out

The hand-built partner video got the whole shape right. Split, stamp each piece, gather by the stamp, count a repeat once, and give up after waiting too long. All of that is true of Camel too. But it left out three things. The completion rule is something you must supply, and can forget. The deadline needs something actually watching a clock, while the rest of the program carries on. And a piece that never comes back is a real event, not a line the demo chose to skip.

## 12. How To Recognise It

How can you spot this in code someone else wrote? Look for a split step in one place, and an aggregate step in another, joined only by an I D on the messages. Look for a completion size, with no timeout beside it. That is a queue of orders that may never come out. And look for unfinished groups kept only in memory, which a restart will empty.

## 13. The Verdict

So, here is the verdict. Split when the pieces can be worked on separately, and the work is slow enough to make parallel work worthwhile. Stamp every piece with what it came from, and its place. Then, on the aggregator, state two things clearly. When it is done. And when it has waited long enough. Never set only the first. And write the duplicate check yourself. Because the framework counts messages, and you care about pieces.

## 14. What Is Real Here

A quick, honest note about this demo. This is Apache Camel, version four point twenty, running inside the demo's own program. There is no container, no broker, and no network call. So it runs offline, with nothing installed except a Java development kit. Every number you heard comes from the program's own output. And two runs, one after the other, print the same results.

## 15. When This Is Too Much

So, when is this too much? If the pieces are quick, or each one needs the answer from the one before, splitting costs more than it saves. If nothing can ever go missing, the hand-built version is smaller, and clearer. And a framework must be learned before a route can be trusted. A route is easy to read, but hard to guess.

## 16. Thanks for Watching

That's Splitter and Aggregator, with Camel. If you remember one sentence, make it this one. An aggregator with only a count will wait forever, so the deadline is not a nice extra, it is the other half of the pattern. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the deadline from the second aggregator, and run it again. Then listen as the deadline demo stops producing any answer at all. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

# Competing Consumers with RabbitMQ Pattern — Video Narration Script

## 1. Competing Consumers with RabbitMQ

Hello, and welcome. This video explains the Competing Consumers pattern in Java, using a real message broker called RabbitMQ. This video is presented by Jayasekhar Konduru. First, a simple definition. Competing consumers are several workers reading from one shared queue of jobs. Each job goes to exactly one of them. So adding a worker adds capacity, and nothing else has to change. In our online store, every order becomes a pick order for the warehouse. On a busy day, one picker cannot keep up. So several pickers take orders from the same queue, and the broker decides who gets which. By the end, you will hear one picker handed the whole queue, while another stands idle. A picker crash while holding five orders, and hand back three. And three orders lost for good.

## 2. The Scenario

Here is the scenario. On a busy day, orders arrive faster than one warehouse picker can pick them. And the queue grows. The warehouse wants to add pickers, without rewriting anything. No order should be picked twice. And none should be lost when a picker's handheld crashes halfway down an aisle. The plain Java version kept its queue as a list inside one program. Each worker reached in, and took a job when it was free. This time, the queue lives in a real broker. And the broker does not wait to be asked. It hands work out. That changes two things.

## 3. One Picker, Then Three

First demo: one picker, then three. Twelve orders are waiting, and one picker takes them one at a time. One is being picked, and eleven wait. Put three pickers on the same queue. Now three are being picked, and nine wait. The pickers never talk to each other. They only talk to the broker. Then three pickers share three hundred orders. All three hundred are picked, and they are three hundred different orders. None twice, and none missed. How many each picker got is the broker's choice. And it changes from run to run. So the demo only says what always holds. Every picker did some, and none did more than half.

## 4. The Broker's Words

A real broker brings a few words with it. Think of a restaurant kitchen, with one ticket rail and several cooks. Order tickets go up on the rail. And a cook who is free takes the next one. The rail is what RabbitMQ calls a queue. A named place where messages wait, in the order they arrived. Each cook is what RabbitMQ calls a consumer. In our store, each consumer is a warehouse picker. When a picker finishes an order, it tells the broker it is done. So the broker may forget it. RabbitMQ calls that an acknowledgement. Until it arrives, the broker keeps its own copy of the order.

## 5. No Limit: One Takes Everything

Second demo, and this is the surprise at the heart of this video. Back in the kitchen. How many tickets may one cook take down at once? RabbitMQ calls that number the prefetch. It is how many orders the broker will hand one picker, before hearing done for any of them. If nobody sets it, there is no limit. That is the default. Twelve orders are waiting. A slow picker starts first, with no limit set. The broker hands it all twelve at once. And nothing is left waiting. A fast picker joins a moment later. And it is handed nothing at all. It stands idle, while the slow picker works through all twelve, one by one. Competing consumers that do not compete.

## 6. Prefetch: How Many To Hold

Third demo: the same slow and fast pickers, now with a limit. Twenty orders, and a prefetch of ten. The broker hands each picker ten. The fast one picks its ten, and then stands idle, with the queue empty. Meanwhile, the slow one is still holding ten that nobody else can reach. Now, a prefetch of one. The slow picker holds just one. And the fast one picks the other nineteen. So prefetch is a trade, not a fix. A prefetch of one shares the work fairly. But every order costs a trip to the broker and back. A high prefetch keeps a fast picker busy. But it lets a slow picker sit on work.

## 7. Where An Order Can Be

Here is the whole picture, in words. An order is always in one of three places. It is waiting in the queue. Or it has been handed to a picker, who has not yet said done. Or it is gone, because a picker said done. The prefetch decides how many orders each picker can hold in that middle place. And here is the rule that holds the rest of this video together. The broker only forgets an order when a picker says it is done.

## 8. A Picker Dies Mid-Work

Fourth demo: a picker crashes halfway through its work. Picker A may hold five orders, and is handed five. It picks order one, and says done. It picks order two, and says done. It starts order three by reserving the stock. Then it crashes, before saying done. The broker notices the connection has gone. It does not know which orders picker A had started. It only knows which ones it never heard done for. So it puts all three back. Picker B is handed orders three, four, and five. All three are marked as seen before. But only order three had really been started. Eight deliveries, for five orders. And the stock for order three was reserved twice. The mark means this might be a repeat. It never means this is one.

## 9. No Saying Done

Fifth demo: the same crash, with one setting changed. This time, picker A tells the broker not to wait for done at all. Every order counts as finished the moment it is handed over. RabbitMQ calls this automatic acknowledgement. Picker A is handed five orders. And the broker has already forgotten all five. Picker A picks two, and crashes on order three. Nothing goes back. Nothing is waiting. Three orders are lost. And nobody will ever be handed them again.

## 10. Two Settings, Two Lines

In the code, both settings are small enough to miss. Before a picker starts listening, one call sets its prefetch: how many orders it may hold. Leave that call out, and there is no limit. Then, when it starts listening, a yes or no says whether the broker should count orders as done when they are handed over. Say no, and the picker must say done itself. After the work, never before.

## 11. The Bill

Finally, the bill. Order thirteen is a poison order. Something in it crashes every picker that takes it. Three pickers take it, one after another. And each one crashes. It was delivered three times, and picked none. And it is waiting again. The broker cannot tell a poison order from a slow one. On an ordinary queue, it will hand it out forever, unless somebody sets a limit. Two more costs. Every picker must be safe to run twice, because the fourth demo made eight deliveries for five orders. And prefetch is a number somebody has to choose. Left unset, one picker took all twelve orders, while another stood idle.

## 12. What The Simulation Left Out

The plain Java version got the shape right. One queue. Workers that never talk to each other. Each order handled once. And a failed order given back, and taken over. All of that is true on RabbitMQ. But it left out four things. First, a real broker pushes work out. And by default, it pushes everything to whoever is listening first. Second, handed over is not the same as started. So a crash hands back more than the one order that failed. Third, saying done is a choice. And the other choice loses orders. Fourth, the plain version counted attempts. But an ordinary RabbitMQ queue only marks an order as seen before: yes or no.

## 13. The Verdict

So, here is the verdict. Share one queue between several pickers when one cannot keep up, and the order of the work does not matter. Then settle three things, because the broker will not assume any of them. One. Set a prefetch. One for fairness, higher for speed, but never the default of no limit. Two. Say done after the work is finished. And make every picker safe to see the same order twice. Three. Limit how often one order may be handed out. Or a poison order goes round forever.

## 14. What Is Real Here

A quick, honest note about this demo. The broker is RabbitMQ, version four point three point six, the newest release. It runs in a container that the demo starts and stops by itself. Nothing is installed, and nothing is left running. You just need Docker switched on first. Every exact number you heard comes from the program's own output. The one thing that changes between runs is how the broker splits orders between equal pickers. So that is described in words, and the tests check it as a range.

## 15. When This Is Too Much

So, when is this too much? If one picker keeps up, one picker is simpler, and keeps orders in order. If the order of the work matters, competing pickers are the wrong shape, until the queue is split by key. If losing an order in a crash is acceptable, counting done on handover is faster. But that should be a decision somebody wrote down, not a default nobody noticed. And a broker is one more system to run, secure, update, and watch.

## 16. Thanks for Watching

That's Competing Consumers, with RabbitMQ. If you remember one sentence, make it this one. The broker only forgets an order when a picker says done, and a picker that crashes hands back everything it was holding, not just what it had started. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give the slow picker in the second demo a prefetch of one. Guess how many orders each picker will get, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!

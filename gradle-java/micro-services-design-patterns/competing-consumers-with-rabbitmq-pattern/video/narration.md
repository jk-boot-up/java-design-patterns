# Competing Consumers with RabbitMQ Pattern — Video Narration Script

## 1. Competing Consumers with RabbitMQ

Hello, and welcome. This video explains the Competing Consumers pattern in Java, using a real message broker called RabbitMQ. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. Competing consumers are several workers reading from one shared queue of jobs. Each job goes to exactly one of them, so adding a worker adds capacity, and nobody else has to change. Now the same thing in our online store. Every order the shop takes becomes a pick order for the warehouse. On a busy day one picker cannot keep up, so several pickers take orders from the same queue, and the broker decides who gets which. By the end you will have seen one picker handed the whole queue while another stands idle, a picker die holding five orders and hand back three, and three orders lost for good.

## 2. The Scenario

Here is the scenario. On a busy day, orders arrive faster than one warehouse picker can pick them, and the queue grows. The warehouse wants to add pickers without rewriting anything. No order should be picked twice, and none should be lost when a picker's handheld crashes half way down an aisle. The plain-Java version of this pattern, earlier in the course, kept its queue as a list inside one program, and each worker reached in and took one job when it was free. This time the queue lives in a real broker, and the broker does not wait to be asked. It hands work out. That changes two things.

## 3. One Picker, Then Three

First, the reason for the pattern. Twelve orders are waiting, and one picker takes them one at a time. One is being picked, and eleven wait. Put three pickers on the same queue, and three are being picked, nine wait. The pickers never talk to each other. They only talk to the broker. Then three pickers share three hundred orders. All three hundred are picked, and they are three hundred different orders, so none twice and none missed. Notice what the demo does not print: how many each picker got. That is the broker's own choice, and it changes from run to run. So the demo says what always holds, in words. Every picker did some, and none did more than half.

## 4. The Broker's Words

A real broker brings a few words with it. Think of a restaurant kitchen with one ticket rail and several cooks. Tickets go up on the rail, and a cook who is free takes the next one. The rail is what RabbitMQ calls a queue: a named place where messages wait, in the order they arrived. Each cook is what RabbitMQ calls a consumer. In our store, each consumer is a warehouse picker, with its own connection to the broker. And when a picker has finished an order, it tells the broker it is done, so the broker may forget it. RabbitMQ calls that an acknowledgement. Until it arrives, the broker keeps its own copy of the order.

## 5. No Limit: One Takes Everything

Second, and this is the surprise at the heart of this video. Back in the kitchen. How many tickets may one cook pull down at once? RabbitMQ calls that number the prefetch: how many orders the broker will hand one picker before hearing done for any of them. If nobody sets it, there is no limit. That is the default. Twelve orders are waiting. A slow picker starts first, with no limit set. The broker hands it all twelve at once, and nothing is left waiting. A fast picker joins a moment later, and is handed nothing at all. It stands idle while the slow picker works through all twelve, one by one. Twelve for the slow picker, none for the fast one. Competing consumers that do not compete.

## 6. Prefetch: How Many To Hold

Third, the same slow and fast pickers, now with a limit. With a prefetch of ten and twenty orders, the broker hands each of them ten. The fast one picks its ten, and then stands idle with the queue empty, while the slow one is still holding ten that nobody else can reach. With a prefetch of one, the slow picker holds just one, and the fast one picks the other nineteen. So prefetch is a trade, not a fix. A prefetch of one shares the work fairly, but every order costs a trip to the broker and back. A high prefetch keeps a fast picker busy, and lets a slow one sit on work.

## 7. Where An Order Can Be

Here is the whole picture in words. An order is always in one of three places. It is waiting in the queue. Or it has been handed to one picker, and that picker has not yet said done. Or it is gone, because a picker said done. The prefetch decides how many orders can sit in the middle place for each picker. And here is the rule that holds the rest of this video together. The broker forgets an order only when a picker says it is done.

## 8. A Picker Dies Mid-Work

Fourth, a picker dies half way through its work. Picker A may hold five orders, and is handed five. It picks order one and says done. It picks order two and says done. It starts order three by reserving the stock, and then it crashes, before saying done. The broker notices the connection has gone. It does not know which orders picker A had started. It only knows which ones it handed over and never heard done for. So it puts back all three. Picker B is handed orders three, four and five. All three carry a mark that says seen before, which RabbitMQ calls redelivered. But only order three had really been started. Eight deliveries for five orders, and order three's stock reserved twice. The mark means this might be a repeat. It never means this is one.

## 9. No Saying Done

Fifth, the same crash, with one setting changed. This time picker A tells the broker not to wait for done at all, and to count every order as finished the moment it is handed over. RabbitMQ calls that automatic acknowledgement. Picker A is handed five, and the queue is already empty, because the broker has already forgotten all five. Picker A picks two, and crashes on order three. Nothing goes back. Nothing is waiting. Three orders are lost, and nobody will ever be handed them again.

## 10. Two Settings, Two Lines

In the code, both settings are small enough to miss. Before a picker starts listening, one call sets its prefetch: how many orders it may hold. Leave that call out, and there is no limit. Then, when it starts listening, one yes or no says whether the broker should count orders done on handover. Say no, and the picker must say done itself, after the work, never before.

## 11. The Bill

Last, the bill. Order thirteen is a poison order. Something in it crashes every picker that takes it. Three pickers take it, one after another, and each one crashes. It was delivered three times, marked seen before on two of them, picked none, and it is waiting again. The broker cannot tell a poison order from a slow one. On an ordinary queue it will hand it out for ever, unless somebody gives it a limit. Two more costs. Every picker must be safe to run twice, because act four made eight deliveries for five orders. And prefetch is a number somebody has to choose, because left unset, one picker took twelve of twelve while another stood idle.

## 12. What The Simulation Left Out

The plain-Java version got the shape right. One queue. Workers that never talk to each other. Each order handled once. A failed order given back and taken over. All of that is true on RabbitMQ. It left out four things. First, a real broker pushes work out, and by default it pushes everything to whoever is listening first. Second, handed over is not the same as started, so a crash hands back more than the one order that failed. Third, saying done is a choice, and the other choice loses orders. And fourth, the simulation counted attempts, but an ordinary RabbitMQ queue only marks an order seen before, yes or no.

## 13. The Verdict

Here is my verdict, plainly. Share one queue between several pickers when one cannot keep up, and the order of the work does not matter. Then say three things out loud, because the broker will not assume any of them. One. Set a prefetch. One for fairness, higher for speed, but never the default of no limit. Two. Say done after the work is finished, and make every picker safe to see the same order twice. Three. Put a limit on how often one order may be handed out, or a poison order goes round for ever.

## 14. What Is Real Here

What is real here? The broker is RabbitMQ, version four point three point six, the newest release, running in a container that the demo starts at the beginning and stops at the end, on a free port picked at random. Nothing is installed and nothing is left running. The one thing you need is a container runtime, such as Docker Desktop, switched on before you start. Every exact number in this video comes from the program's own output, and two runs print the same thing. The one thing that changes between runs, how the broker splits orders between equal pickers, is described in words, and the tests check it as a range.

## 15. When This Is Too Much

So when is this too much? If one picker keeps up, one picker is simpler, and keeps the orders in order. If the order of the work matters, several competing pickers are the wrong shape until the queue is split by key. If losing an order on a crash is acceptable, counting done on handover is faster, but it should be a decision somebody wrote down, not a default nobody noticed. And a broker is a separate system to run, secure, upgrade and watch.

## 16. Thanks for Watching

That's Competing Consumers with RabbitMQ. If you take one sentence away, take this one: the broker forgets an order only when a picker says done, and a picker that dies hands back everything it was allowed to hold, not just what it had started. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, give the slow picker in act two a prefetch of one, guess both numbers, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.

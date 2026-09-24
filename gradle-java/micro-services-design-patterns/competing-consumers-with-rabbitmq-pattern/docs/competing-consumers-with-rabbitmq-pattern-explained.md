# Competing Consumers with RabbitMQ, Explained

## The pattern in one sentence

Competing consumers are several workers reading from one shared queue, each message going to exactly one of them, so that adding a worker adds capacity without anybody changing anything else.

## The analogy, before any of the broker's words

Think of a restaurant kitchen with one ticket rail and several cooks. Tickets go up on the rail. A cook who is free takes the next ticket. The cooks never talk about who does what; the rail decides.

Now two questions a real kitchen has to answer, which the plain-Java project in this course never had to. First, how many tickets may one cook pull down at once? If a cook grabs every ticket on the rail the moment the shift starts, the other cooks stand around with nothing to do, even if the first cook is the slowest in the kitchen. Second, when does a ticket count as done? If a cook walks out half-way through, the tickets in their pocket must go back on the rail, or those meals are never made. And the kitchen cannot know which of those tickets the cook had already started; it only knows which ones they took. Those two questions are the whole of this project.

## What RabbitMQ calls these things

A **broker** is the rail and the person who hands out the tickets: a separate program whose job is to hold messages and give them to workers. RabbitMQ is the broker here, running in a container the demo starts and stops.

A **queue** is the rail: a named place where messages wait, in the order they arrived. Here it holds pick orders for the warehouse.

A **consumer** is a cook. Here it is a warehouse picker, each with its own connection to the broker. Several consumers on one queue are the pattern.

An **acknowledgement** is the cook saying "done": the picker telling the broker it has finished an order, so the broker may forget it. Until then the broker keeps its own copy.

**Automatic acknowledgement** is a picker telling the broker not to wait for "done" at all, and to count each order as finished the moment it is handed over.

**Prefetch** is how many orders the broker will hand one picker before hearing "done" for any of them: how many tickets one cook may be holding. It is set per picker. **Setting none means no limit**, and that is RabbitMQ's default.

**Redelivered** is the broker's mark on an order it has handed out before: in this project's words, seen before. It is a yes or no, not a count, and it means "this might be a repeat", not "this is one".

## The six acts

### One Picker, Then Three

Twelve orders are waiting and one picker takes them one at a time: one being picked, eleven waiting. Put three pickers on the same queue and three are being picked, nine waiting. Then three pickers share 300 orders: all 300 picked, 300 different orders, so none twice and none missed.

How many each picker got is the broker's choice, and the exact split changes from run to run. So the demo prints what always holds, in words: every picker did some, and none did more than half.

```
  12 orders, one picker taking one at a time. being picked: 1. waiting: 11.
  the same 12, three pickers on the same queue. being picked: 3. waiting: 9.
  300 orders, three pickers: 300 picked, 300 different orders. every picker did some, and none did more than half.
  who got which order is the broker's choice, and it changes from run to run.
```

### No Limit: The First Picker Takes Everything

This is the headline find, and the plain-Java version could not stage it. Twelve orders are waiting. A slow picker starts first, with no prefetch set. The broker hands it all twelve at once, and nothing is left waiting. A fast picker joins a moment later and is handed nothing. It stands idle while the slow picker works through all twelve, one by one.

```
  12 orders waiting. a slow picker starts first, with no limit set. handed to it: 12. waiting: 0.
  a fast picker joins a moment later. handed to it: 0. it stands idle while the slow one holds 12.
  picked by the slow picker: 12. by the fast one: 0. RabbitMQ's default is no limit.
```

### Prefetch: How Many A Picker May Hold

The same slow and fast pickers, now with a limit. With prefetch 10 and 20 orders, each picker is handed 10. The fast one picks its 10 and then stands idle with the queue empty, while the slow one still holds 10. With prefetch 1, the slow picker holds 1 and the fast one picks the other 19.

A low prefetch spreads work fairly, and costs a trip to the broker between every order. A high one keeps a fast picker busy, and lets a slow one sit on work nobody else can reach.

```
  20 orders, prefetch 10. handed to the slow picker: 10. to the fast one: 10.
  the fast one picks its 10 and stands idle. waiting: 0. still held by the slow one: 10.
  the same 20, prefetch 1. the slow picker holds 1. the fast one picks the other 19.
```

### A Picker Dies Mid-Work

Picker A has prefetch 5 and is handed 5 orders. It picks ORD-1 and ORD-2 and says done for each. It starts ORD-3 by reserving the stock, and then it crashes, before saying done. The broker notices the connection has gone. It knows only which orders it handed over and was never told were done, so it puts back all 3. Picker B is handed ORD-3, ORD-4 and ORD-5, and all 3 are marked as seen before, although only ORD-3 had been started. ORD-3's stock has now been reserved twice. That makes 8 deliveries for 5 orders.

```
  prefetch 5. picker A is handed 5, picks ORD-1 and ORD-2, reserves the stock for ORD-3, and crashes before saying it is done.
  the broker puts back every order it handed to A and was not told was done. waiting again: 3.
  picker B is handed [ORD-3, ORD-4, ORD-5], marked as seen before: 3 of 3. only ORD-3 had been started.
  deliveries: 8 for 5 orders. stock reserved for ORD-3: 2 times. for ORD-4: 1.
```

### No Saying Done

The same crash again, but picker A has told the broker to count each order as done on handover. The broker forgets all 5 the moment it hands them over, so the queue is already empty before the crash. Picker A picks 2 and crashes on ORD-3. Nothing goes back. 3 orders are lost, and nobody will ever be handed ORD-3, ORD-4 or ORD-5 again.

```
  picker A tells the broker to count each order as done on handover. handed: 5. waiting: 0.
  the same crash on ORD-3. picked: 2. waiting again: 0. lost: 3. nobody will be handed ORD-3, ORD-4 or ORD-5 again.
```

### The Bill

ORD-13 is a poison order: it crashes every picker that takes it. Three pickers take it one after another and each one crashes. It was delivered 3 times, marked seen before on 2 of them, and picked 0 times, and it is waiting again. The broker cannot tell a poison order from a slow one, and a classic queue will hand it out for ever unless it is given a limit.

Two more costs follow. Every picker must be safe to run twice, because act four made 8 deliveries for 5 orders. And prefetch is a number somebody has to choose, because left unset, one picker took 12 of 12 while another stood idle.

```
  ORD-13 crashes every picker that takes it. 3 pickers, delivered 3 times, marked seen before on 2, picked 0 times. waiting again: 1.
  the broker cannot tell a poison order from a slow one. it will hand it out for ever unless told a limit.
  and every picker must be safe to run twice: act four made 8 deliveries for 5 orders, and reserved the stock for ORD-3 2 times.
  and prefetch is a number somebody has to choose. left unset, one picker took 12 of 12 while another stood idle.
```

## The verdict

Put several pickers on one queue when one picker cannot keep up and the order of the work does not matter. On a real broker, say three things out loud, because the broker will not assume any of them. Set a prefetch: one for fairness, higher for speed, never the default of no limit. Say done after the work, not on handover, and make every picker safe to see an order twice. And put a limit on how often one order may be handed out, or a poison order will go round for ever.

## How to recognise this in code you did not write

- A `basicConsume` with no `basicQos` before it. That picker has no prefetch limit and will take the whole queue.
- A `basicQos` with a large number on a picker whose work is slow. That picker will sit on work others could do.
- A `basicConsume` with automatic acknowledgement turned on (`autoAck` set to `true`). A crash loses everything handed over.
- A handler that reads `isRedeliver()` and skips the order. The mark only says "might be a repeat"; skipping loses orders that were never started.
- A classic queue with no dead-letter or delivery limit, fed by consumers that can crash on bad input.

## Where you have already met this

Order fulfilment workers, email senders, thumbnail makers, settlement jobs: any service scaled to several copies reading one queue. Spring AMQP sets a prefetch of 250 by default; the plain Java client sets none. Amazon SQS, Azure Service Bus and Kafka consumer groups each answer the same two questions in their own words.

## When this is too much

If one picker keeps up, one picker is simpler and keeps the order. If order matters, several competing pickers are wrong until the queue is split by key. And a broker is a separate system to run, secure and watch.

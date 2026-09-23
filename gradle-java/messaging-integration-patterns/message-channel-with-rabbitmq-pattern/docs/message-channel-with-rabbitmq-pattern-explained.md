# Message Channel with RabbitMQ, Explained

## The pattern in one sentence

A message channel is a named place that one system puts messages into and another takes them out of, so that neither has to be running, or waiting, at the same moment as the other.

## The analogy, before any of the broker's words

Think of a post office. You hand a parcel over the counter and walk away. You do not wait for the person it is addressed to; they may be on holiday, and that is fine, because the post office keeps the parcel on a shelf until they come for it.

Now three questions a post office has to answer, and the partner project never had to. What if the person collecting the parcel drops it on the way out and never gets it home? A good post office hands it over only when it is signed for, so an unsigned parcel is still the post office's parcel. What if the post office itself closes for the night? The parcels on the shelf are still there in the morning, but a note written on the whiteboard is not. And what if the shelf is full? Somebody has to decide whether to turn the next parcel away or throw out the oldest one. Those three questions are the whole of this project.

## What RabbitMQ calls these things

A **broker** is the post office: a separate program whose job is to hold messages for other programs. RabbitMQ is the broker here, running in a container the demo starts and stops.

A **queue** is the shelf: a named place where messages wait, in the order they arrived. In this pattern's words, the queue is the channel.

An **exchange** is the counter: the part of the broker that decides which queue a message goes on. This project only uses the default one, which puts a message on the queue whose name it is addressed to, so it never has a real decision to make.

An **acknowledgement** is the signature: the receiver telling the broker it has finished with a message, so the broker may forget it. Until then the broker keeps its own copy.

**Durable** is the broker's word for a queue it writes down, so the queue itself survives a restart. **Persistent** is its word for a message it writes down. They are two separate settings, and the fifth act is about the difference.

A **publisher confirm** is a receipt: the broker telling the sender that it took a message, or turned it away.

**Prefetch** is how many messages the broker will hand one receiver before that receiver has said done with any of them. It only matters when several receivers share a queue, which never happens here: every act has at most one receiver at a time, so this project leaves it unset. Where two receivers do share a queue, how the broker spreads messages between them depends on its own scheduling, and is honestly described as a range rather than a fixed number.

One warning about words. The RabbitMQ Java client also has a type called `Channel`, and it means something unrelated: a lightweight conversation over one network connection. This project gives the name `Channel` to the pattern, and keeps the client's conversation in a field called `amqp`.

## The six acts

### Checkout Calls The Warehouse

The warehouse system is down for maintenance. Checkout calls it directly, three times, and all three checkouts fail. The shop cannot sell while another system is away, even though selling does not need the warehouse to answer yet.

```
  the warehouse system is down for maintenance. orders placed: 3. checkouts that failed: 3.
  the shop cannot sell while another system is away, though selling does not need it to answer yet.
```

### A Real Channel Between Them

A RabbitMQ broker is now running in a container. Checkout sends three pick orders to a queue and carries on without waiting. The warehouse is listening, and is handed each order once. When it has finished, nothing is left waiting.

```
  a RabbitMQ broker is running in a container. checkout sends 3 pick orders and carries on.
  the warehouse is listening and takes them, each once: [ORD-1, ORD-2, ORD-3]. left waiting: 0.
```

### Nobody Is Listening Yet

This is the act the partner project could not stage. The warehouse is not running at all, so no receiver exists anywhere. Checkout sends three orders and none of them fail, because checkout is only talking to the broker. The broker holds all three. When the warehouse starts up afterwards it is handed the backlog, in the order it went in.

```
  the warehouse is not running, so no receiver exists. checkout sends 3, and none fail. the broker is holding: 3.
  the warehouse starts up afterwards and works through them, in order: [ORD-1, ORD-2, ORD-3].
```

### Saying Done

A picker takes order ORD-1 but does not say it is done. Then it crashes: its connection is cut with no goodbye. The broker had kept its own copy, so the moment it notices the connection has gone it puts the order back, and one order is waiting again. A second picker is handed the same ORD-1, and the broker marks it as seen before, so the picker can tell it may be a repeat. This picker says done, and only now does the broker forget the order. Two deliveries, one order picked, none waiting.

The price of never losing an order this way is that a receiver can see the same order twice, and has to be written to cope.

```
  a picker takes ORD-1 and crashes before saying it is done. the broker puts it back. waiting again: 1.
  a second picker is handed the same ORD-1, marked as seen before: true, and says done. deliveries: 2, orders picked: 1, waiting: 0.
```

### Written To Disk, Or Only Held In Memory

Two queues, both durable, each given the same three orders. The only difference is the flag on the messages: one queue's are persistent, marked to be written to disk; the other's are held in memory only. The broker program is stopped and started again inside its container. Both queues come back. The first still holds three orders. The second holds none.

That is the headline find of this project. Keeping a message safe is two settings, not one, and a queue that came back empty after a restart looks, from outside, exactly like a quiet day.

```
  two channels hold 3 orders each. the broker is asked to write one channel's messages to disk and to hold the other's in memory only.
  the broker program is stopped and started again. written to disk: 3 orders still waiting. held in memory only: 0.
  a channel that outlives the sender, the receiver and the broker itself is the whole reason to pay for a broker.
```

### The Bill

A RabbitMQ queue has no limit unless you give it one, and when you give it one, its default is to make room by silently throwing away the oldest message. So this queue is given room for five and told to refuse new messages instead, and checkout asks for a receipt on every send. Eight are sent: five accepted, three refused, and checkout hears about every refusal. Without the receipts, the three refused orders would simply have vanished.

Then two costs that do not go away. Checkout no longer learns whether the warehouse picked an order; it learns only that the broker took the message. And the broker is a third system to run, secure, upgrade and watch: one container, for one shop and one warehouse.

```
  the warehouse stays down and a channel with room for 5 is given 8: 5 accepted, 3 refused. a channel must have a limit, and somebody must decide what to do at it.
  and the sender no longer learns whether the warehouse picked the order. it learns only that the broker took the message.
  and a broker is a third system to run, secure, upgrade and watch: this demo needed 1 container for 1 shop and 1 warehouse.
```

## The verdict

Put a channel between two systems when they live on different schedules. On a real broker, then say three things out loud, because the broker will not assume any of them: write the queue down and write each message down, if a restart must not lose orders; say done only after the work is finished, and make the receiver safe against seeing a message twice; and give the queue a limit, choose what happens at it, and ask for receipts so the sender hears the answer.

## How to recognise this in code you did not write

- A `queueDeclare` with `durable` set, and a `basicPublish` beside it with or without `PERSISTENT_TEXT_PLAIN`. The two have to agree.
- A `basicConsume` with automatic acknowledgement turned on, which means the broker forgets a message the moment it hands it over, and a crash loses it.
- A `basicAck` called before the work instead of after it, which is the same mistake written by hand.
- `x-max-length` with no `x-overflow`, which quietly drops the oldest message when the queue is full.
- A `confirmSelect` and `waitForConfirms`, which is a sender that wants to know.

## Where you have already met this

An order handed to a warehouse. An email handed to a sending service. A payment handed to a settlement job that runs overnight. RabbitMQ, Amazon SQS, Azure Service Bus and ActiveMQ are all this pattern as a product, and each makes you decide, in its own words, what is written to disk and when a message counts as handled.

## When this is too much

If both systems are always up together and the caller needs the answer now, a direct call is simpler and tells you more. If losing a waiting message on a restart is acceptable, a queue inside the program, like the partner project's, costs nothing to run. A broker earns its keep only when the sender and the receiver genuinely live on different schedules.

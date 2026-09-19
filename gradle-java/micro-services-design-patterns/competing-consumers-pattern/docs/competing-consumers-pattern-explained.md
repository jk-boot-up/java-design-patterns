# Competing Consumers, Explained

## The pattern in one sentence

Competing consumers means several workers take messages from the same queue, so each message is handled by one of them, and the work is shared without any of them coordinating.

## The six acts

### One Consumer, Then Three

Six slow jobs: with one consumer, one is in progress and five wait. With three consumers, three are in progress and three wait. The consumers do not talk to each other.

```
  six slow jobs, one consumer: 1 in progress, 5 waiting.
  six slow jobs, three consumers: 3 in progress, 3 waiting.
  the consumers do not talk to each other. they take from the same queue.
```

### Each Message Is Handled Once

A thousand orders and four consumers: handled a thousand times, and a thousand different orders. None twice, none missed.

```
  1000 orders, 4 consumers: handled 1000 times in all, 1000 different orders.
  none twice, none missed. which consumer got which order is not defined, and does not matter.
```

### The Order Is Not Kept

Orders one, two and three are published in that order, but one's consumer is slow, so they finish as two, three, one. If order two depends on order one, that is a bug.

```
  orders 1, 2 and 3 published in that order. order 1's consumer is slow. they finished: [2, 3, 1].
  if order 2 depends on order 1, this is a bug. competing consumers give up ordering.
```

### A Consumer Fails, Another Takes Over

A consumer fails on the first attempt. The message is given back, and another attempt succeeds. It was not lost.

```
  [attempt 1 fails, attempt 2 succeeds].
  the message was given back and handled again. it was not lost.
```

### At Least Once, So A Duplicate

A consumer charges the card and crashes before saying it finished, so the message returns and the card is charged again: two charges. A consumer that remembers what it has done charges once.

```
  a consumer charges the card and then crashes before it can say it finished. charges made: 2.
  the same crash, with a consumer that remembers what it has done: charges made: 1.
```

### The Bill: The Same Downstream

Six consumers share a database that lets two in at a time. Two are inside, and four are waiting for a place, so four of six are doing nothing useful.

```
  6 consumers share a database that lets 2 in at a time. inside it: 2. waiting for a place: 4.
  four of the six are doing nothing useful. adding consumers only helps while the shared thing has room.
```

## The verdict

Use competing consumers to scale work that can be done in any order, where each item is independent. Acknowledge only when finished, make every consumer safe to run twice on the same message, and size the pool for the slowest thing they share. Do not use it where order matters, unless the queue is partitioned by the key that carries the order.

## How to recognise this in code you did not write

- Several instances of a service reading the same queue or topic partition group.
- Kafka consumer groups, SQS with several pollers, RabbitMQ work queues.
- An acknowledge or delete call after the work is done.
- A thread pool whose tasks come from one shared queue.

## Where you have already met this

Every scaled-out worker service, and every Java `ExecutorService` fed by one queue.

## When this is too much

When one consumer keeps up, extra consumers are cost and risk. When order matters, competing consumers are wrong until the queue is partitioned.

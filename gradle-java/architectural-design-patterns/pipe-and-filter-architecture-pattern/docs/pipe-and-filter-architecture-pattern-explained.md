# Pipe and Filter Architecture, Explained

## The pattern in one sentence

Pipe and filter architecture splits work into stages that run at the same time, joined by waiting lines, so that each stage can be sized and limited on its own.

## The six acts

### One Big Step

One worker does all three jobs, five ticks for each order. An order arrives every tick. After thirty ticks, five orders are done.

```
  parse 1 tick, price 3, pack 1: 5 ticks for each order, one at a time. an order arrives every tick.
  after 30 ticks, orders done: 5.
```

### Stages With Waiting Lines

The same work in three stages, each working while the others do. After thirty ticks, eight orders are done. Parse takes a new order while price is still on the last one.

```
  the same work in three stages, each working while the others do. after 30 ticks, orders done: 8.
  the parse stage takes a new order while price is still on the last one.
```

### The Slowest Stage Sets The Pace

Waiting in front of each stage: parse one, price nineteen, pack none. Price takes three ticks, so one order leaves every three ticks, however fast parse and pack are. Orders pile up in front of it.

```
  waiting in front of each stage: parse 1, price 19, pack 0.
  price takes 3 ticks, so one order leaves every 3 ticks however fast parse and pack are. orders pile up in front of it.
```

### Widen Only The Slow Stage

Three price workers. After thirty ticks, twenty two orders are done, and the lines are short. Parse and pack were not touched. Now they take one order a tick, and that is the new limit.

```
  three price workers. after 30 ticks, orders done: 22. waiting: parse 1, price 1, pack 1.
  parse and pack were not touched. now they take one order a tick, and that is the new limit.
```

### A Limit On Each Line

With no limit, nineteen orders wait in one line. With a limit of three, no more than three wait, and fourteen orders are refused at the door. Orders done is eight, the same as without a limit. A full line makes the stage before it hold its order, and so on back to the door. That push-back is called backpressure.

```
  no limit: most orders waiting in one line 19, refused at the door 0.
  limit of 3: most orders waiting in one line 3, refused at the door 14. orders done: 8, the same as without a limit.
  a full line makes the stage before it hold its order, and so on back to the door. that push-back is called backpressure.
```

### The Bill

The price stage crashes. Twenty orders were in it, waiting or being worked on. They were accepted from customers, and are gone, unless the lines are kept somewhere that survives. And an order now passes through three stages and two waiting lines, so a single order takes longer than its five ticks of work, whenever it has to wait.

```
  the price stage crashes. orders it was holding, waiting or working on: 20. they were accepted from customers and are gone, unless the lines are kept somewhere that survives.
  and an order now passes through 3 stages and 2 waiting lines, so a single order takes longer than the 5 ticks of work, whenever it has to wait.
```

## The verdict

Use stages when the work has parts of different speed and you want throughput. Find the slowest stage, and widen only that one. Put a limit on each waiting line so that trouble pushes back to the door. Keep the lines somewhere that survives a crash if the orders matter.

## How to recognise this in code you did not write

- Stages joined by queues, as in a log-processing or ETL system.
- Worker pools with a bounded queue in front, such as `ThreadPoolExecutor`.
- `BlockingQueue` between producer and consumer threads.
- Reactive streams and their request-n backpressure.

## Where you have already met this

Unix pipelines, video and image processing chains, ETL systems, and build systems that run stages in parallel.

## When this is too much

If the work is short, or the stages are about equally fast, a single step is simpler, and the queues only add delay. Stages pay off when parts differ in speed, or need separate scaling.

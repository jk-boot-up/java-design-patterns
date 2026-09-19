# Queue-Based Load Leveling, Explained

## The pattern in one sentence

Queue-based load leveling puts a queue between a source of bursty work and the service that does it, so the service works at its own steady pace and the burst waits its turn.

## The six acts

### A Burst, Straight To The Worker

A hundred orders arrive at once and the service takes ten. Ninety are refused, on the busiest moment of the shop's day.

```
  100 orders arrive at once. the order service handles 10 a tick. processed: 10, refused: 90.
  ninety customers were told to try again, on the busiest moment the shop had.
```

### A Queue In Between

The same hundred orders, through a queue: all hundred are processed, none refused, and the worker never did more than ten a tick.

```
  the same 100 orders. processed: 100, refused: 0. the deepest the queue got: 100.
  the worker never did more than 10 a tick. the burst was spread over 10 ticks.
```

### What The Queue Costs: Waiting

The first order waited nothing. The last waited nine ticks. On average an order waited four and a half.

```
  the first order waited 0 ticks. the last waited 9. on average: 4.5.
  no order was lost, and none was fast except the first ten.
```

### A Queue With No End, And One With A Limit

Fifteen arrive a tick and the worker does ten. An unbounded queue reaches five hundred waiting and keeps growing. A queue limited to fifty refuses four hundred and sixty, and no wait is longer than four ticks.

```
  orders arrive at 15 a tick and the worker does 10, for 100 ticks. an unbounded queue: 500 orders waiting, and still growing.
  a queue limited to 50: 40 waiting, 460 refused, longest wait 4 ticks.
  a queue does not fix a worker that is too slow. it hides it, until the limit says so.
```

### Size The Worker For The Average

A worker of ten clears the burst with a longest wait of nine. A worker of twenty halves it to four. Serving the peak with no queue would need a worker of a hundred, idle almost all day.

```
  a worker of 10 a tick clears the burst with a longest wait of 9. a worker of 20 clears it with a longest wait of 4.
  to serve a peak of 100 at once with no queue you would need a worker of 100, idle almost all day.
```

### The Bill: An In-Memory Queue Forgets

The process holding an in-memory queue stops at tick three. Thirty orders were processed and seventy were waiting, and are lost, though the customers were told they were accepted.

```
  the process holding the queue stops at tick 3, with the queue in memory. processed: 30, lost: 70.
  70 customers were told their order was accepted, and it never happened.
  a queue that must not lose orders has to be kept somewhere that survives.
```

## The verdict

Use a queue to level load when work arrives in bursts, the caller does not need the answer straight away, and a short wait is acceptable. Bound the queue, watch its depth, and size the worker for the average. Keep the queue somewhere durable if orders must not be lost. Do not use it where the caller needs an immediate result.

## How to recognise this in code you did not write

- A message broker or a queue between a web tier and a worker tier.
- A `BlockingQueue` between threads, sized on purpose.
- A chart of queue depth on a dashboard, with an alert.
- Amazon SQS, RabbitMQ, Kafka, or Azure Service Bus in an architecture diagram.

## Where you have already met this

Every checkout that says 'we have received your order' and then emails you later.

## When this is too much

If load is steady and the service copes, a queue is one more thing to run. If the caller needs the answer now, a queue is the wrong shape.

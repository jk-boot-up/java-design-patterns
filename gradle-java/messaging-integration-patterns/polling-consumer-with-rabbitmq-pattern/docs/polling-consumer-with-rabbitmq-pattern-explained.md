# Polling Consumer with RabbitMQ, Explained

## The pattern in one sentence

With RabbitMQ, a polling consumer asks for messages with `basicGet` when it is
ready; push with a prefetch limit gives the same protection with less waste.

## The 5 acts

### 1. Push with no limit

The printer subscribes with no prefetch limit. A burst of fifty orders
arrives, and RabbitMQ pushes all fifty into the printer's memory at once,
although its buffer holds ten. When the printer crashes, all fifty,
unacknowledged, go back on the queue to be sent again.

### 2. A polling consumer

Now the printer polls: each tick, it asks the broker for up to five orders
with `basicGet`, prints them and acknowledges each. Fifty orders are printed
in ten ticks, and it never holds more than five.

### 3. Pausing is not polling

Twenty more orders arrive. After one tick the paper runs out, so the printer
stops polling: five are printed and fifteen wait safely on the queue. When
paper is loaded and polling resumes, all twenty are printed and none is lost.

### 4. When nothing is happening

In a quiet minute, polling every tenth of a second makes six hundred requests
to the broker, all empty. RabbitMQ's middle way is push with a prefetch limit:
with a limit of five, the printer holds five of the twenty orders waiting, and
the broker sends more only as it acknowledges. A quiet queue then costs no
requests at all.

### 5. The bill

With polling, an order that arrives just after a poll waits a whole interval,
and every empty poll is a request to the broker. RabbitMQ's own advice is to
consume with a prefetch limit, keeping `basicGet` for the cases where the
receiver must control exactly when it takes work.

## The verdict

Poll when the receiver must decide exactly when to take work. Otherwise
consume with a prefetch limit, sized to what the receiver can hold.

## How to recognise this in code you did not write

- `channel.basicGet(queue, false)` in a loop.
- `channel.basicQos(n)` before `basicConsume`.
- Scheduled jobs that drain a queue.

## Where you have already met this

- RabbitMQ `basicGet` and `basicQos` prefetch.
- Amazon SQS `ReceiveMessage` with long polling.
- Kafka consumers, which always poll, with `max.poll.records`.

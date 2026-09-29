# Polling Consumer, Explained

## The pattern in one sentence

A polling consumer takes messages from a queue when it is ready, as many as it
can handle, so it sets its own pace and can pause without losing anything.

## The 5 acts

### 1. Pushed at the printer

Each order is pushed at `LabelPrinter` the moment it arrives. The printer's
buffer holds ten jobs. A burst of fifty arrives at once: ten are accepted,
forty are refused with "printer busy".

### 2. A polling consumer

Orders now go into a queue. `PollingConsumer.tick` asks the queue for up to
five orders, as many as the printer can print in one tick. All fifty are
printed in ten ticks, one second, and none is refused: the queue holds the
rest until the printer asks.

### 3. Pausing

After one tick the paper runs out, so the consumer is paused: it simply stops
polling for three seconds. Five labels are printed and fifteen orders wait
safely in the queue. When paper is loaded and polling resumes, all twenty are
printed and none is lost.

### 4. How often to poll

In a quiet minute with no orders, polling every tenth of a second makes 600
requests, all of them empty. Long polling, where each request waits up to 20
seconds for something to arrive, covers the same minute with three.

### 5. The bill

A message that arrives just after a poll waits until the next one: up to a
whole interval. Polling often wastes requests, polling rarely adds waiting.
Long polling is the usual middle way.

## The verdict

Use polling consumers when a consumer must control its own pace, handle
bursts or pause safely. Take only what you can handle, use long polling to
avoid empty requests, and accept a small wait for the next poll.

## How to recognise this in code you did not write

- Loops that call `poll()`, `receive()` or `ReceiveMessage` with a batch size.
- Settings for polling interval, max messages and wait time.
- Consumers that pause by simply not polling.

## Where you have already met this

- Kafka consumers calling `poll()` in a loop.
- Amazon SQS `ReceiveMessage` with long polling.
- Spring Integration's polling channel adapters.
- Checking email with IMAP rather than push notifications.

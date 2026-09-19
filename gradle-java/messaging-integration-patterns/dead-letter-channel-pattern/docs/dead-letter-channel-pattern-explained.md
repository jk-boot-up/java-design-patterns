# Dead Letter Channel, Explained

## The pattern in one sentence

A dead letter channel is where a message goes when it cannot be handled after a fixed number of tries, so that it stops blocking the messages behind it and can be looked at later.

## The six acts

### A Message That Can Never Succeed

Four orders, one garbled. Only the first is handled. The garbled one is tried ten times and never succeeds, and orders three and four are stuck behind it.

```
  four orders, one garbled. handled: [ORD-1]. still waiting: 3. attempts made: 11.
  the garbled order is at the head of the line and will never succeed. orders 3 and 4 are stuck behind it.
```

### A Dead Letter Channel

After three attempts the garbled order is moved aside. Orders one, three and four are handled, nothing is waiting, and there is one dead letter.

```
  after 3 attempts the garbled order is moved aside. handled: [ORD-1, ORD-3, ORD-4]. waiting: 0. dead letters: 1.
  orders 3 and 4 went through.
```

### It Says Why

The dead letter records the order, three attempts, the last error, and the channel it came from. The original message is kept exactly.

```
  ORD-2: 3 attempts, last error 'cannot read the body of ORD-2', from channel orders.
  the original message is kept exactly, so it can be looked at, and put back.
```

### A Slow Day Is Not A Dead Letter

Order three fails once on a timeout and succeeds on the second try, so it is not dead-lettered. Only order two, which fails every time, is.

```
  ORD-3 failed once, on a timeout, and succeeded on the second attempt. handled: [ORD-1, ORD-3, ORD-4].
  only ORD-2, which fails every time, is a dead letter: [ORD-2].
  retrying is for the first kind of failure, and the dead letter channel is for the second.
```

### Fix It, And Replay

The parser is fixed and the dead letter is replayed. Order two is now handled, after three and four, and the dead letters are empty. Replay does not restore the original order.

```
  before the fix: handled [ORD-1, ORD-3, ORD-4], dead 1.
  the parser is fixed and 1 dead letter is replayed. handled: [ORD-1, ORD-3, ORD-4, ORD-2], dead 0.
  note the order: ORD-2 was handled after ORD-3 and ORD-4. replay does not restore the order.
```

### The Bill: Nobody Is Looking

Forty orders, half garbled: twenty dead letters, each an order a customer was told was accepted. The main channel looks healthy, with nothing waiting, and nothing tells anyone to look.

```
  40 orders, half of them garbled: 20 dead letters, and every one of those orders was accepted from a customer.
  the main channel looks perfectly healthy: 0 waiting. the dead letter channel is where the loss is, and nothing tells anyone to look.
  a dead letter channel needs an alert on its depth, an owner, and a limit on how long a message may stay. each keeps a copy of customer data.
```

## The verdict

Use a dead letter channel on every channel where a message can fail for ever. Retry a few times for transient failures, then move the message aside with its attempts and its reason. Alert on the depth of the dead letter channel, give it an owner, and decide how long messages stay. Make consumers safe to replay.

## How to recognise this in code you did not write

- A queue named `something-dlq` or `dead-letter`.
- A `maxReceiveCount` on an SQS queue, or `x-dead-letter-exchange` in RabbitMQ.
- Spring's `DefaultErrorHandler` with a `DeadLetterPublishingRecoverer`.
- A dashboard with a count of messages in the dead letter queue.

## Where you have already met this

Every managed queue service has one, and every operations team has a story about one that filled up unnoticed.

## When this is too much

For a channel where failure is impossible, or where losing a message is fine, a dead letter channel is more to run. Where a message can be poison, its absence is the outage.

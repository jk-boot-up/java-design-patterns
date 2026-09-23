# Dead Letter Channel with RabbitMQ, Explained

## The pattern in one sentence

A dead letter channel is somewhere for a message to go when it cannot be handled, so that it stops blocking the messages behind it and a person can look at it later.

## The same sentence, with a real broker in it

The shop writes a rule on the queue saying where a dead order should be sent. After that the broker does the moving, and writes down which rule it applied. The application has no code that puts an order in the dead letter queue.

Three words are worth saying in plain language before RabbitMQ's names for them appear.

- A **queue** is the line orders wait in.
- An **exchange** is the broker's sorting desk. You hand a message to a desk with a label on it, and the desk decides which queues get a copy. The desk that parked orders are handed to is what RabbitMQ calls a **dead letter exchange**.
- **Refusing an order** is the worker telling the broker it will not finish this one. The worker can refuse it and ask for it back, which puts it at the head of the queue again, or refuse it for good, which hands it to the desk.

## The six acts

### An Order That Can Never Succeed

Four orders go on a queue with no rule written on it. The second has an address nothing can read. The worker takes each order in turn, and when one fails it refuses it and asks for it back. The broker puts it back at the head of the line, so it is the next thing the worker gets. Over twelve turns, eleven of them are the same unreadable order. The two good orders behind it never move.

```
  four orders, one with an address nothing can read. handled: [ORD-1001]. still waiting: 3. deliveries of ORD-1002: 11.
  the worker refuses it and asks for it back, so the broker returns it to the head of the queue. ORD-1003 and ORD-1004 never get their turn.
```

### A Dead Letter Channel, Made Of A Real Exchange And A Real Queue

The same four orders, on a queue declared with a rule: a dead order goes to the parked exchange under the key `rejected`, and a queue called `orders.parked.rejected` is tied to that key. The worker gives each order three deliveries. On the third failure it refuses the unreadable order for good, and the broker takes it out of the queue and hands it to the desk. The two good orders behind it go through. One of them had failed once on a payment gateway timeout, and succeeded the next time it was delivered.

```
  the worker gives each order three deliveries. after the third it refuses ORD-1002 for good, and the broker takes it out of the queue.
  handled: [ORD-1001, ORD-1003, ORD-1004]. still waiting: 0. parked: 1. deliveries in all: 7.
  ORD-1003 failed once on a payment gateway timeout and went through on its second delivery. a slow day is not a dead order.
```

Seven deliveries: one for the first order, three for the unreadable one, two for the one that timed out, one for the last.

### The Broker Writes Down Why

Reading the parked queue gives back the order with a note attached. The note names the queue it died in, `orders.work`, counts the deaths, one, and gives the reason in one word: `rejected`. The body of the order is byte for byte what the shop sent.

```
  ORD-1002: reason rejected, from queue orders.work, died 1 time.
  the order itself is exactly as the shop sent it: ORD-1002 ship to ??? ?? ?????, card ending 9930
  the application wrote none of that. the broker did, and it will be there tomorrow morning.
```

### Not Every Death Is A Refusal

Two more orders die, and no worker touches either one.

The first goes on a queue declared with a time limit of five hundred milliseconds. Nobody reads it in time, and the broker parks it with the reason `expired`.

The second goes on a queue declared to hold two orders. Three are sent. To take the third, the broker pushes the oldest out, and parks it with the reason `maxlen`. Two orders are left waiting there.

```
  ORD-1005 sat in a queue with a time limit of 500 milliseconds and nobody read it: reason expired, from queue orders.slow.
  a queue that holds two orders was sent three. the broker pushed the oldest out: ORD-1006, reason maxlen. still waiting there: 2.
  no worker refused either order. the broker decided both times, and named the rule it applied.
```

This is the act the hand-built version cannot have. In plain Java, nothing but the worker can act, so the only way a message can die is for the worker to decide it has died.

### Fix It, And Put It Back

The unreadable order is parked. An operator finds the cause — the address parser — and fixes it. The parked order is published back onto the working queue, and this time it goes through. It is handled last, after the two orders that were behind it, because a replay puts a message at the back of the line.

```
  before the fix: handled [ORD-1001, ORD-1003, ORD-1004], parked 1.
  the address parser is fixed and 1 parked order is published back onto the working queue. handled: [ORD-1001, ORD-1003, ORD-1004, ORD-1002]. parked: 0.
  note the order: ORD-1002 was handled after ORD-1003 and ORD-1004. a replay does not restore the order things were sent in.
  and it goes back as a new message, so the broker's note is gone unless the operator copies it across first.
```

### The Bill: Nobody Is Looking

Forty orders, every second one unreadable. The worker refuses each bad one for good on its first delivery, and the broker parks it. Twenty orders are shipped and twenty are parked. Every one of the forty was paid for by a customer who was told the order went through. The working queue reports nothing waiting, so every dashboard shows the shop healthy.

```
  40 orders, half of them unreadable: 20 parked, 20 shipped, and every one of those 40 was paid for by a customer.
  the working queue reports 0 waiting, so every dashboard shows the shop healthy. the loss is in the parked queue, and nothing tells anyone to look at it.
  a parked queue needs an owner, an alert on its depth, and a limit on how long an order may stay, because each parked order is a copy of a customer's address.
  and a broker is another thing to run: this demo declared 11 queues and 1 exchange in 1 RabbitMQ container, and took the container away at the end.
```

## The three reasons, in one place

| The broker's word | What happened | Who decided |
| --- | --- | --- |
| `rejected` | A worker refused the message and did not ask for it back | The worker started it, the broker carried it out |
| `expired` | The message sat in the queue past its time limit | The broker alone |
| `maxlen` | The queue was full, and this was the oldest message in it | The broker alone |

## The verdict

Write the rule on every queue where a message can fail for ever. Let the worker try a few times, for the failures that pass, and then refuse for good, for the ones that do not. Let the broker do the moving, because it will do it when your process has crashed as well as when it has not. Read the note it attaches, because it is the only account of the death you will have at three in the morning. Then put an alert on the depth of the parked queue, give the queue an owner, and decide how long an order may stay in it.

## How to recognise this in code you did not write

- A queue declared with `x-dead-letter-exchange` in its arguments.
- A queue whose name ends in `.dlq`, `.parked` or `-dead-letter`.
- A consumer calling `basicReject` or `basicNack` with `requeue` set to false.
- An `x-death` header read out of a message's headers, or `x-first-death-reason`.
- In Spring AMQP, a `RepublishMessageRecoverer`, or a retry policy ending in a rejection.
- In Amazon SQS, a redrive policy with a `maxReceiveCount`.

## Where you have already met this

Every managed queue service has one, under a different name, with the same three parts: a rule on the queue, somewhere for the dead message to go, and a note saying why.

## When this is too much

For a queue where failure is impossible, or where losing a message costs nothing, this is more to run than it is worth. Where a message can be poison, its absence is the outage.

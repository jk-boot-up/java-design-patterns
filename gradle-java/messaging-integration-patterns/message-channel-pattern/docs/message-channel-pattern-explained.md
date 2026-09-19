# Message Channel, Explained

## The pattern in one sentence

A message channel is a named queue that carries messages from a sender to a receiver, so the two systems can talk without being up at the same time.

## The six acts

### Checkout Calls The Warehouse

With the warehouse down, three orders are placed and all three checkouts fail. The shop cannot sell while another system is away.

```
  the warehouse system is down for maintenance. orders placed: 3. checkouts that failed: 3.
  the shop cannot sell while another system is away, though selling does not need it to answer yet.
```

### A Channel Between Them

Checkout sends three messages and carries on. The warehouse then takes them, each once, in order.

```
  checkout sends 3 messages and carries on. waiting in the channel: 3.
  the warehouse takes them, each once: [ORD-1, ORD-2, ORD-3].
```

### The Receiver Is Away

The warehouse is down, and checkout sends three messages, and none fail. When the warehouse comes back, it works through them in order.

```
  the warehouse is down. checkout sends 3, and none fail. waiting: 3.
  the warehouse comes back and works through them, in order: [ORD-1, ORD-2, ORD-3].
```

### An Envelope

A message has headers, such as priority and correlation, that can be read without opening the body. A router or receiver can decide from the envelope alone.

```
  headers, readable without opening the body: {correlation=ORD-1, priority=express}. type: PickOrder.
  body: 2 x MUG-BLUE.
  a router or a receiver can decide what to do from the envelope alone.
```

### One Channel, One Kind Of Message

The pick orders channel refuses a refund request. A receiver never has to ask what kind of message it was given.

```
  channel pick-orders carries PickOrder but was given RefundRequest.
  a receiver of pick orders never has to ask what it was given.
```

### The Bill

If the warehouse stays down, a channel of five fills, and three more are refused. The sender no longer learns whether the order was picked, only that the message was accepted. Sent five, received none.

```
  the warehouse stays down and a channel of 5 fills: 5 accepted, 3 refused. a channel must have a limit, and somebody must decide what to do at it.
  and the sender no longer learns whether the warehouse picked the order. it learns only that the message was accepted.
  sent 5, received 0: the difference is work nobody has done yet.
```

## The verdict

Use a channel between systems that are not always up together, or that work at different speeds. Give it a type, a limit and a name. Put the routing information in the envelope. Decide what happens when it is full, and how the sender finds out the result, since it will not hear it from the call.

## How to recognise this in code you did not write

- A queue name in a configuration file, such as `pick-orders`.
- A `send` call that returns at once, and a separate `receive` loop.
- JMS destinations, SQS queues, RabbitMQ queues, Kafka topics.
- A message class with headers and a payload.

## Where you have already met this

Every message queue product, and Java's own `BlockingQueue`, which is the same idea inside one process.

## When this is too much

If both systems are always up and the caller needs the answer now, a direct call is simpler. A channel is for decoupling in time.

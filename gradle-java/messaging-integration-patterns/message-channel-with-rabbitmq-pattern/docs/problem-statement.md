# Problem Statement

## The scenario

The shop takes orders. The warehouse picks them off the shelf. They are two separate systems, run by two separate teams, and they are not always up at the same time: the warehouse system goes down for maintenance, gets restarted after a deploy, and sometimes crashes half-way through an order. The shop should not stop selling because of any of that. Selling does not need the warehouse to answer yet; it only needs the pick order to reach the warehouse eventually, exactly once as far as the customer can tell.

## The naive version

Checkout calls the warehouse directly and waits for an answer.

```
  the warehouse system is down for maintenance. orders placed: 3. checkouts that failed: 3.
  the shop cannot sell while another system is away, though selling does not need it to answer yet.
```

## What the partner project already did

[Message Channel](../../message-channel-pattern) put a channel between the two: a named, bounded queue that checkout puts pick orders into and the warehouse takes them out of. The warehouse could be away and the orders simply waited. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. The channel was a list inside the same Java program as the shop and the warehouse. "The warehouse is away" was a flag on an object, taking a message out of the list removed it for good, and there was nowhere for a message to be except in that program's memory. So it could not show a receiver that did not exist yet, a receiver that died holding a message, or a channel that was itself restarted.

## What this project must deliver

The same shop and the same warehouse, with the channel moved into a real RabbitMQ broker that the demo starts in a container and stops at the end. Three orders sent to a queue with no receiver at all, held by the broker, and worked through by a warehouse started afterwards. A picker that takes an order and crashes before saying it is done, and the broker handing the same order to the next picker, marked as seen before. Two pickers, one slow and one fast, sharing one queue, first with no limit on how many unfinished orders the broker hands each, then with a limit of one. Two queues holding the same three orders, the broker program stopped and started again, and a count of what each one still holds. A channel with room for five given eight, refusing the rest out loud rather than quietly dropping the oldest. And an honest bill: the sender now learns only that the broker took the message, and the broker is a third system to run.

Every figure printed is the broker's own, and two runs back to back print the same thing.

# Problem Statement

## The scenario

An online store puts every order on a queue. A worker takes one order at a time and ships it. One order in four arrives with an address nothing can read, and no amount of trying will ever make it readable. The orders behind it are perfectly good.

## The naive version

Refuse the bad order and ask the broker for it back. RabbitMQ returns it to the head of the queue, so it comes round again, and again, and the good orders behind it never get their turn.

```
  four orders, one with an address nothing can read. handled: [ORD-1001]. still waiting: 3. deliveries of ORD-1002: 11.
  the worker refuses it and asks for it back, so the broker returns it to the head of the queue. ORD-1003 and ORD-1004 never get their turn.
```

## What is new here, against the hand-built version

The partner project, [Dead Letter Channel](../../dead-letter-channel-pattern), has the whole idea in plain Java: try a few times, then put the message aside with its reason. What it cannot show is the line this project is about.

In a real broker the application does not move the dead order. The shop writes a rule on the queue when it declares it, saying where a dead order should be sent. From then on the broker acts: when a worker refuses an order for good, when an order sits past a time limit, and when a queue is full and the oldest order has to be pushed out. Each time, the broker attaches its own note to the order saying which queue it died in, how many times it has died, and a one-word reason for the death.

## What this project must deliver

An order that can never be read and blocks the queue when the worker keeps asking for it back; a rule on the queue that sends a refused order to a queue of its own without a line of application code doing the moving; the broker's note read back and shown, with the reason `rejected`; two more deaths nobody chose, with the reasons `expired` and `maxlen`; a replay after the cause is fixed, which does not restore the original order; forty orders of which twenty are quietly parked while every dashboard reports the shop healthy; and a plain verdict.

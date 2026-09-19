# Problem Statement

## The scenario

The payment gateway takes some time to answer a card charge. Meanwhile, the shop has other work to do, and other orders to charge.

## The naive version

Ask the gateway again and again, until the answer is ready.

```
  the answer arrived on the 5th look. looks made: 5, 4 of them found nothing.
  and the caller could do nothing else in that time.
```

## What this project must deliver

A gateway that only records a request, and delivers the answer when told to, so order is chosen and nothing is timed; a polling handle that counts looks; callbacks that carry a result; a callback that throws, recorded by the gateway; answers delivered out of order, with a shared field that mixes orders up; and three nested callbacks whose lines run out of written order.

# Problem Statement

## The scenario

When an order is placed, inventory must reserve stock and shipping must plan a delivery. Either of them may be down at the moment.

## The naive version

The order service calls inventory and shipping directly, and waits for each.

```
  the order service calls shipping and waits. shipping is down. order accepted: false. orders placed: 0.
  a customer lost an order because a service they never see was down.
```

## What this project must deliver

A direct version that loses an order when shipping is down; an append-only event log; an order service that only appends; readers with their own position and a lag; a down reader that catches up; a reader added later that reads from the start; a warehouse whose stock is briefly wrong; and a duplicate delivery that a check absorbs.

# Problem Statement

## The scenario

When an order is placed, stock is reserved, a confirmation email is sent, and the sales funnel is counted.

## The naive version

The order code calls stock, email and analytics itself, one after another. It works until one of them is down.

```
  the mail server is down. the caller gets: mail server timed out.
  order saved: true. what happened: [stock: reserved for ORD-1].
  saved and reserved, the customer told they failed, analytics never counted it.
```

## What this project must deliver

An `Order` that records `OrderPlaced` and `OrderCancelled` events and calls nobody; a repository that keeps the events with the order and a relay that delivers them; a failing handler that neither undoes the order nor stops the others and is retried alone; events as records that carry data; the gap between saving and telling, and how keeping the events with the order closes it; and a plain verdict.

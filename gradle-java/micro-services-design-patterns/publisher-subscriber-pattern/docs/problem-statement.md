# Problem Statement

## The scenario

When an order is placed, inventory must reserve stock, email must send a confirmation, and analytics must count it. Next month, loyalty points want to know as well.

## The naive version

The order service calls inventory, email and analytics itself, by name, one after another.

```
  inventory [ORD-1], email [ORD-1], analytics [ORD-1].
  the order service knows 3 services by name. a fourth, loyalty points, means editing it.
```

## What this project must deliver

A topic that is an append-only log with a reader position for each subscriber; a publisher that only appends; a fourth subscriber added without touching the publisher; a slow subscriber with its own backlog; filters by kind; a live and a replaying subscriber; a subscriber that is down and catches up; and a plain verdict.

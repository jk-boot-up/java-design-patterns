# Problem Statement

## The scenario

Inside the shop's program, inventory, email, analytics, loyalty and the audit log all react to orders being placed or cancelled.

## The naive version

Each component holds references to the others and calls them when an order changes.

```
  5 components that each tell each other about orders: 20 references between them.
  add a sixth and it needs 10 more.
```

## What this project must deliver

An in-process bus with typed subscriptions, subtype subscriptions, failure isolation and dead events; the reference counts with and without it; a failing subscriber that does not stop the others; an event nobody hears caught as a dead event; a subscriber asked for by type; a leak from subscriptions never cancelled; and a plain verdict.

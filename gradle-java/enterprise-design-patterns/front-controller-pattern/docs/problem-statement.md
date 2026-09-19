# Problem Statement

## The scenario

The store's web application has pages for products, orders and the customer's account. Every request needs to be logged, and every private page needs the visitor to be signed in.

## The naive version

Each handler looks after its own logging and its own sign-in check. It works while every handler's author remembers both.

```
  /orders with no sign-in: 200 ada's orders: ORD-1, ORD-2
  /account with no sign-in: 401 please sign in
  requests logged: 0 of 2. the orders handler has no login check and no log line, and the account handler logs only what it accepts.
```

## What this project must deliver

A `FrontController` with filters and a routing table; a sign-in check that no handler can forget; uniform answers for unknown pages and wrong methods; a log that includes refused requests; a failure answered without its detail; the outage a buggy filter causes; and a plain verdict.

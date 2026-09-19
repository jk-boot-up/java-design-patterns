# Problem Statement

## The scenario

When a customer places an order, the store checks the quantity and the stock, takes the stock, prices the order with a bulk discount, charges the card, and saves it.

## The naive version

There is no naive version here. The script is the simplest thing that works, and the project asks how long it stays that way.

```
  ORD-1 for £16.00. stock of MUG-BLUE: 8.
  the whole business action is one method, read from the top to the bottom.
```

## What this project must deliver

A `PlaceOrderScript` that does the whole action in one method and one transaction that rolls back; a second script that copies the pricing and drifts; a shared helper; the growth of decisions and paths in a script over a year; and a plain verdict with the place where a script is best.

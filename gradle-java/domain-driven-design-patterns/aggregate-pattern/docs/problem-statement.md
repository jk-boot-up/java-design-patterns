# Problem Statement

## The scenario

An order has lines. It has rules that span the lines: a line holds between one and ten of an item, an item appears on one line only, the total may not pass a thousand pounds, and a placed order cannot change.

## The naive version

The order is a list with public fields. Every caller checks the rules it remembers. It works while every caller is careful.

```
  a line of -3 mugs: in. the same machine on two lines: in. total: £5988.50, past the £1000 limit: in.
  a line added to an order already placed: in.
  every rule is true in the head of the person who wrote the caller.
```

## What this project must deliver

An `Order` root that is the only way to change the lines and enforces every rule; lines that cannot be built outside it; a reference to the customer by id; whole-aggregate saves with a version check; a boundary drawn too big, for the bill; and a plain verdict.

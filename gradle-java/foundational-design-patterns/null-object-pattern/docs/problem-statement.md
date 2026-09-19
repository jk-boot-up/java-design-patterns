# Problem Statement

## The scenario

Most customers have no discount. Some have a loyalty discount, a few a staff
discount. Something has to price an order after whatever discount there is.

## The naive version: return null

`find` returns `null` for no discount, and every caller checks. This is not a
silly design. It is what most code does, and it works when everyone remembers.

```
ONE. find() returns null, and every caller checks.
  customer 1 (loyalty), 10000 pence: total 9000, invoice 9000
  customer 2 (no discount):          total 10000, invoice 10000
```

There are eight places that price an order. Seven remember the check. The eighth
was added last, in a hurry.

```
  the eighth place to price an order, taxBase, for customer 2:
  NullPointerException at checkout.
```

And the cost is quieter than the crash: the check appears seven times, so a
reader stops seeing it, and the missing one hides in plain sight.

## What this project must deliver

A discount that is never null, and a plain answer to when that is a good idea.

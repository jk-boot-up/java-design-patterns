# Problem Statement

## The scenario

The store keeps orders in a table. Each order has a customer, a total and a status. Orders are created, changed while they are drafts, placed, and looked up by customer.

## The naive version

There is no naive version. Active Record is the simplest way to get data in and out, and the project asks what it costs.

```
  saved order 1 for customer 1, 1600 pence, DRAFT.
  three lines: new, save, find. no repository, no mapper.
```

## What this project must deliver

An `Order` and a `Customer` that are rows and know how to find and save themselves; finders on the class; rules on the record; the three bills shown for real, with table operations counted; and a plain verdict.

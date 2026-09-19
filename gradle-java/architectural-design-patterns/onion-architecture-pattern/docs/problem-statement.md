# Problem Statement

## The scenario

An order is placed, priced and saved. The pricing rule gives ten percent off orders of one hundred pounds or more. Storage may change from memory to a file to a database.

## The naive version

Let the order class run its own SQL statement to save itself.

```
  the order saved itself with a SQL statement. statements run: 1.
  to change the storage, the order class, at the centre, must be edited.
```

## What this project must deliver

A naive order that calls a database; four rings: the order and a repository idea at the centre, pricing rules, a use case, and storage and a console outside; a dependency checker that reads the classes with reflection; a naive class caught by it; two storages behind one repository idea; the rules run with no storage; and a count of conversions.

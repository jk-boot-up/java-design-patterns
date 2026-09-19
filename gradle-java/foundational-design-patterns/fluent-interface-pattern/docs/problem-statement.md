# Problem Statement

## The scenario

The catalog search takes a category, a price limit, whether to show only what is in stock, whether to sort by price, and how many to show.

## The naive version

One method with five positional arguments, two of them true or false.

```
  find("mugs", 2500, true, true, 10): [Blue Mug, Big Mug].
  find("mugs", 2500, false, true, 10) has the two booleans the other way round: [Blue Mug, Gift Mug, Big Mug].
  both compile. which is in stock, and which is the sort? you must count the arguments to know.
```

## What this project must deliver

A catalog of six products; a positional find with five arguments; an immutable fluent query; a mutable one that returns itself; a guided version whose steps offer only what may come next, shown by reflection; a bad value accepted and found late; and a count of the methods.

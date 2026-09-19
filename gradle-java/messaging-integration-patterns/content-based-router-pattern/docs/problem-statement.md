# Problem Statement

## The scenario

Orders arrive together: physical goods, gift cards, subscriptions, and some of very high value. Physical goods go to the warehouse, gift cards to digital delivery, and very high value orders to fraud review.

## The naive version

Everything goes to the warehouse's channel, and the warehouse sorts out what it can do.

```
  all 6 orders arrive on the warehouse's channel. 2 are gift cards, which nothing physical can be done for, and 1 is neither.
  the warehouse now has an if for each kind, and every new kind means changing the warehouse.
```

## What this project must deliver

A router with ordered rules, a fallback and a count of dropped messages; six orders routed by their content; two rule orders giving two answers for the same order; a message with no route both caught and lost; a rule added with no other change; a renamed value that makes a rule miss; and a plain verdict.

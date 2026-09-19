# Problem Statement

## The scenario

Sales, Shipping and Support all talk about the customer. Sales means a buyer with a credit limit. Shipping means a delivery address. Support means a person with tickets. Everyone says the same word.

## The naive version

One `Customer` class for the whole company. Every department added the fields it needed.

```
  fields in the company-wide Customer class: 12.
  each context uses a handful of them, and every one depends on the whole class, so one context's change is every context's change.
```

## What this project must deliver

Three models, one per context, that each mean what their department means; a shared id and nothing else; contexts linked by events with each context translating for itself; a boundary that a test can check; the bill of duplication and eventual consistency; and a plain verdict.

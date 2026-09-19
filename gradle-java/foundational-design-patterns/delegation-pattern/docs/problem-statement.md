# Problem Statement

## The scenario

An order can be priced with a premium discount, with gift wrap, with both, or with neither. A customer may become premium in the middle of shopping.

## The naive version

Write a subclass of Order for each way of pricing, and one more for each combination.

```
  premium, gift wrap, and both: 4 classes for 2 features. a third feature would need 8.
  premium and gift order: 9600. and an order cannot change its class once it exists.
```

## What this project must deliver

An inheritance version with four classes; an Order that holds a PricingRule and hands its total to it; rules for none, premium, gift wrap and both in order; a swap of the rule on a live order; a rule that reads the order it was called for; and the costs of a count of extra calls and of forwarding methods.

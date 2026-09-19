# Problem Statement

## The scenario

Books have no tax and cost three pounds to ship. Laptops carry twenty percent tax and ship free. Groceries have five percent tax. Next month, the shop will sell gift cards.

## The naive version

Write a subclass for each kind of product, with the numbers in overridden methods.

```
  3 kinds, 3 classes, and they differ only in three numbers. a novel: 1300.
  a gift card is a fourth kind. that is a fourth class, a new build and a release.
```

## What this project must deliver

A naive set of three subclasses; a Product class and a ProductType with tax, return days and shipping; a registry of types; a gift card type added while running; a tax change that reaches every grocery product; a derived type that inherits what it does not state; and the costs of late typos and of fields for every difference.

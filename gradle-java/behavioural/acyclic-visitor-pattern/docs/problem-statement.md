# Problem Statement

## The scenario

The catalogue has books, food and electronics, and operations such as VAT and
customs forms that visit each product.

## The naive version

The classic `ClassicVisitor` has a method per product type. Every visitor
must write every method, even empty ones, and a new type (gift cards) forces a
change to the interface and to every visitor.

## What this project must deliver

- The classic visitor shown: three methods, two empty ones in customs, and no way to accept a gift card.
- An empty root interface and one small interface per product type.
- A new product type added with no change to existing visitors.
- A visitor that handles exactly one type.
- The cost shown: a forgotten interface that compiles and silently skips.
- Every printed result asserted by a test.

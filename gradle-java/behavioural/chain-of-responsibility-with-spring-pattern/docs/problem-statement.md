# Problem Statement

## Read the partner first

This project assumes [Chain of Responsibility](../chain-of-responsibility-pattern), which passed a checkout request along address, stock, fraud and payment checks, stopping at the first that answered, and reported which links never ran. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: the screening an online shop runs before it accepts an order.

## What is new

Spring **assembles the chain for you**. Ask for a `List<Check>` and it hands over every check bean, already sorted by its `@Order`.

```
  order: [address, stock, fraud, payment-limit].
  the order comes from @Order numbers on four different classes.
```

## The failure this project exists to show

The order is spread over four classes as numbers, so nothing in one place shows it. A link that throws takes the chain with it unless the walker catches it. And a property can quietly remove a link.

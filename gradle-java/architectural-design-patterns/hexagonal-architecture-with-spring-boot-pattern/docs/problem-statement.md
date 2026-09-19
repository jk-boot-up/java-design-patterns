# Problem Statement

## Read the partner first

This project assumes [Hexagonal Architecture](../hexagonal-architecture-pattern), which put the order use case in a core that knows only ports, with adapters outside it, so storage and notification could change without the core changing. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: placing an order through a core with ports, and adapters around it.

## What is new

**Spring Boot** does the wiring. Adapters are components chosen by a property, and one configuration class hands the plain core its adapters.

```
  the use case the container hands out is a PlaceOrderService, not a proxy, in package core.
  classes in the core that mention Spring or an adapter: 0.
```

## The failure this project exists to show

Nothing stops a use case reaching for Spring, so the core needs a rule. And a missing adapter is found at startup, not at compile time.

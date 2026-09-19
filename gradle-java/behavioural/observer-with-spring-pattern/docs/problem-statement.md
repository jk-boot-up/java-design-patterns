# Problem Statement

## Read the partner first

This project assumes [Observer](../observer-pattern), which let an order announce every status change to inventory, email, analytics and the warehouse feed, without knowing any of them, and reported a failing listener by name. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: an order that changes status, and four reactions that must not know about each other.

## What is new

Spring has **events built in**. The subject holds an `ApplicationEventPublisher`. Any bean method marked `@EventListener` becomes an observer, found by the type of its argument.

```
  inventory: released stock for ORD-000001 on main
  email: told the customer about ORD-000001
  analytics: counted ORD-000001 as SHIPPED
  warehouse feed: pick line for ORD-000001
```

## The failure this project exists to show

The container wires observers by scanning, so nothing in the code says who is listening. Delivery is synchronous by default, so one failing listener stops the rest and reaches the caller. And an event nobody listens to is dropped without a sound.

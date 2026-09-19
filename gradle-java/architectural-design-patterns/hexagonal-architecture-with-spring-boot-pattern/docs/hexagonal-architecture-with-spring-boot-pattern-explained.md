# Hexagonal Architecture with Spring Boot, Explained

## The pattern in one sentence

In Spring Boot, the adapters are beans chosen by configuration, and the core stays a plain class handed to the container.

## What is new here

The pattern is [Hexagonal Architecture](../hexagonal-architecture-pattern). This page is only what Spring Boot adds.

### The Core Is Plain Java

The container hands out the use case as a plain class from the core package, and no class in the core mentions Spring.

```
  the use case the container hands out is a PlaceOrderService, not a proxy, in package core.
  classes in the core that mention Spring or an adapter: 0.
```

### Two Storage Adapters

A property chooses memory or a database. The same order gives the same receipt, and the stock drops the same way.

```
  orders.store=memory: ORD-000001 for 30000 pence, kept by InMemoryOrderStore, stock now 4.
  orders.store=jdbc: ORD-000001 for 30000 pence, kept by JdbcOrderStore, stock now 4.
```

### Two Doors Into One Room

A console adapter and a batch adapter both call the same port. One refuses an order for too many machines, and the batch refuses one line in three.

```
  console: ORD-000001 for £300.00
  console: refused: not enough ESP-001 in stock
  batch of three lines: [ORD-000002, refused, ORD-000003]
  neither adapter knows how the other works. both call the same port.
```

### The Core Without A Container

Ten thousand orders go through the real use case with adapters made by hand and no container. The payment port is a one-line lambda.

```
  10000 orders through the real use case, with adapters made by hand and no Spring context: 10000 stored.
  the payment port was a one-line lambda. that is what a port is for.
```

### A Use Case That Reaches For Spring

A use case with a transaction annotation and a database client breaks the rule ten times. The real core breaks it never.

```
  the rule 'the inside knows no framework', run over every class: 10 violations.
  every one is in SpringyPlaceOrder: true. the real core has none.
```

### A Port With No Adapter

A property value with no adapter behind it stops the application at startup, naming the missing port.

```
  orders.store=nothing: the application does not start. no bean of type OrderStore.
  hand wiring would not have compiled. the container finds out at startup.
```

## The verdict

Keep the core free of annotations, wire it in one configuration class, choose adapters by configuration, test the core without a container, and check the inside rule in the build.

## How to recognise this in code you did not write

- A `@Configuration` class that calls `new` on a use case.
- `@ConditionalOnProperty` on adapters.
- Ports as interfaces in a `core` package.

## Where you have already met this

Spring applications whose business code has no annotations.

## When this is too much

For a small service with one storage, a port with one adapter is ceremony.

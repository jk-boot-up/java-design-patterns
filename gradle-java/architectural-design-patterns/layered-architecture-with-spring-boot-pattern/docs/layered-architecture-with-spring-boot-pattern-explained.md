# Layered Architecture with Spring Boot, Explained

## The pattern in one sentence

In a Spring Boot application, the layers are controllers, services and repositories, and the layering rule is yours to enforce.

## What is new here

The pattern is [Layered Architecture](../layered-architecture-pattern). This page is only what Spring Boot adds.

### Four Layers, One Real Request

A real request creates an order and takes one machine from stock.

```
  POST /orders -> 201 {"orderId":"ORD-000001","totalPence":30000,"status":"PAID"}
  stock of ESP-001 afterwards: 4.
  controller, service, repository and record: each is one layer, marked by a Spring stereotype.
```

### One Transaction

The card is declined after the stock was reserved. The service's transaction undoes the reservation.

```
  the card is declined after the stock was reserved: 402 the card was declined
  stock of ESP-001 afterwards: 4. the reservation was rolled back.
```

### Failures Become Statuses In One Place

Too many machines is refused with a 422. The domain names the reason, and one class turns it into a number.

```
  ten machines when four are left: 422 not enough ESP-001 in stock
  the domain named the reason. only the presentation layer knows what number it becomes.
```

### The Shortcut Runs

A controller that reads the repository directly starts, and answers. Spring wires by type, and does not mind.

```
  GET /raw-orders/ORD-000001 -> 200 {"id":"ORD-000001","customer":"ada","sku":"ESP-001","quantity":1,"totalPence":30000,"costPence":21000,"status":"PAID"}
  a controller that reads the repository directly. Spring did not object.
```

### It Also Leaks

The shortcut returns the record as it is, including the cost price. The layered answer returns a response object that has none.

```
  the shortcut's answer contains the shop's cost price: true.
  the layered answer contains it: false.
```

### A Rule The Container Does Not Have

An ArchUnit rule says which layer may depend on which. Run over the project, it finds three violations, all in the shortcut.

```
  the layering rule, run over every class in the project: 3 violations.
  every one is in ShortcutController: true. the real four layers have none.
  Spring wires by type. Only a test can say a layer is not allowed to be there.
```

## The verdict

Keep the layers as packages, put the transaction in the service, map failures in one place, return response objects and not entities, and run a layering test in the build.

## How to recognise this in code you did not write

- `@RestController`, `@Service` and `@Repository` in separate packages.
- `@Transactional` on a service method.
- An ArchUnit `layeredArchitecture()` test.

## Where you have already met this

Most Spring Boot applications you will ever open.

## When this is too much

For a small script with one table, four layers are more ceremony than help.

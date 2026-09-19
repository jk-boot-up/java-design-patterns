# Problem Statement

## Read the partner first

This project assumes [Layered Architecture](../layered-architecture-pattern), which arranged placing an order into presentation, application, domain and infrastructure layers, with one rule about who may depend on whom, and counted the bill for a forced change. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: placing an order for a coffee machine, through four layers.

## What is new

**Spring Boot** gives each layer a real job and a real annotation: a controller, a service with a transaction, a repository on a database, and HTTP in front.

```
  POST /orders -> 201 {"orderId":"ORD-000001","totalPence":30000,"status":"PAID"}
  stock of ESP-001 afterwards: 4.
  controller, service, repository and record: each is one layer, marked by a Spring stereotype.
```

## The failure this project exists to show

Spring wires by type, so it accepts a controller that reads a repository directly. The layering rule is not enforced by the container, and a shortcut can leak fields the layers were hiding.

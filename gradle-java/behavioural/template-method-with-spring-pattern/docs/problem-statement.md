# Problem Statement

## Read the partner first

This project assumes [Template Method](../template-method-pattern), which fixed the order of an order's fulfilment steps in one final method, and let three routes fill in the holes. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

Order data in an online shop, read and written through a database, with the fixed steps of every database call owned by the framework.

## What is new

Spring's **`JdbcTemplate`** and **`TransactionTemplate`** are Template Method by composition. The framework owns the fixed steps and calls a lambda you pass in for the step that differs.

```
  a good query returns [ORD-000001, ORD-000002, ORD-000003]. connections in use afterwards: 0.
  a query with a typo throws JdbcSQLSyntaxErrorException. connections in use afterwards: 1.
  the pool has two connections, so a second typo leaves one, and a third waits for a connection that never comes back.
```

## The failure this project exists to show

The template makes decisions for you: what counts as a missing row, how an error is translated, when a transaction rolls back. None of them shows in your code.

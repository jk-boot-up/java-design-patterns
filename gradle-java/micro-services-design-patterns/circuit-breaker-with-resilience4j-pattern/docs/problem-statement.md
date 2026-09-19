# Problem Statement

## Read the partner first

This project assumes [Circuit Breaker](../circuit-breaker-pattern), which built a breaker with three states by hand, so a product page stopped waiting three seconds on a recommendations service that had gone quiet. Nothing here is lost by skipping Resilience4j, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: the product page calls a recommendations service, and the service stops answering.

## What is new

**Resilience4j** is a library that already contains the breaker. You put an annotation on the method and set its numbers in `application.properties`.

```
  page shows: [Blue Mug Set, Tea Towel]. breaker: CLOSED. backend calls: 1.
```

## The failure this project exists to show

The breaker is a proxy, so a call on `this` skips it. The fallback hides failures from the caller, so the state is the only alarm. And what counts as a failure is a setting that is easy to get wrong.

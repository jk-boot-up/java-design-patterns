# Problem Statement

## Read the partner first

This project assumes [Consumer-Driven Contract](../consumer-driven-contract-pattern), which let each consumer write its contract as data, and let the provider check its real answer against every contract, naming the consumer and the field, and showed that a contract cannot see a change of meaning. Nothing here is lost by skipping Pact, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a catalog price service that renames a field that checkout reads.

## What is new

**Pact**, the standard contract testing library: a consumer DSL that writes a pact file, and a provider verifier that replays it over real HTTP.

```
  the catalog renamed priceCents to price and released. checkout, 2 mugs: total -1, meaning the order failed.
  it was found in production, by a customer.
```

## The failure this project exists to show

A pact still checks the shape and not the meaning. Every consumer must keep its pact up to date. And the provider's build now depends on the consumers' files.

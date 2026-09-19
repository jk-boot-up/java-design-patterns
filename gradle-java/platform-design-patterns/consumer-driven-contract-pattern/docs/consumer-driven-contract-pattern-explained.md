# Consumer-Driven Contract, Explained

## The pattern in one sentence

A consumer-driven contract lets each consumer of a service write down exactly what it needs, and lets the provider check every release against those contracts before it goes out.

## The six acts

### Nobody Told The Consumer

The catalog renamed price cents to price, and released. Checkout, two mugs: the order failed. It was found in production, by a customer.

```
  the catalog renamed priceCents to price and released. checkout, 2 mugs: total -1, meaning the order failed.
  it was found in production, by a customer.
```

### The Consumer Writes It Down

Checkout's contract: price cents, an integer, and sku, a string. Reports' contract: sku, a string. Each lists only the fields it reads, and their types.

```
  checkout's contract: {priceCents=INTEGER, sku=STRING}.
  reports' contract: {sku=STRING}.
  each lists only the fields it reads, and their types.
```

### The Provider Checks Itself

The catalog's real answer is checked against both contracts. No problems. Safe to release.

```
  the catalog's real answer against both contracts. problems: []. safe to release.
```

### The Rename Is Caught

The same check on the renamed release reports: checkout expects price cents, an integer, and it is missing. The build fails, and it names the consumer and the field.

```
  problems: [checkout expects priceCents (integer): missing].
  the build fails, and it names the consumer and the field.
```

### Adding Is Safe

A release that adds a stock field: no problems. And the rename again, per consumer: checkout, one problem; reports, none. Reports never used that field.

```
  a release that adds a stock field. problems: [].
  the rename again, per consumer: checkout 1 problem, reports 0 problems. reports never used that field.
```

### The Bill

A release that now sends pounds, not pence, in the same field: no problems. It passes. Checkout, two mugs: total thirty two, where it should be thirty two hundred. A contract checks the shape, and not the meaning. And every consumer must keep its contract up to date, or the check protects nobody.

```
  a release that now sends pounds, not pence, in the same field. problems: []. it passes.
  checkout, 2 mugs: total 32, where it should be 3200.
  a contract checks the shape, and not the meaning. and every consumer must keep its contract up to date, or the check protects nobody.
```

## The verdict

Let consumers state what they use, and let providers check against it before every release. Keep contracts small: only the fields read. Share them where the provider's build can find them. Add tests for meaning where shape is not enough.

## How to recognise this in code you did not write

- Pact files, or Spring Cloud Contract stubs.
- A provider build that fails with a consumer's name in the message.
- A consumer test that runs against a stub generated from its own contract.
- A broker or folder of contracts that the provider's pipeline reads.

## Where you have already met this

Pact in many microservice teams, Spring Cloud Contract, and Google's and Netflix's approaches to safe change across services.

## When this is too much

If provider and consumer are one team with one release, an ordinary test is enough. Contracts pay off across teams that release apart.

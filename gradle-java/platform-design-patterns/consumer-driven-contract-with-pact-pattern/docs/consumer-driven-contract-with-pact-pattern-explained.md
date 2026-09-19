# Consumer-Driven Contract with Pact, Explained

## The pattern in one sentence

With Pact, a consumer's test writes a pact file, and the provider's build replays that file against the real service, and fails on any difference.

## What is new here

The pattern is [Consumer-Driven Contract](../consumer-driven-contract-pattern). This page is only what Pact adds.

### Nobody Told The Consumer

The catalog renamed price cents to price, and released. Checkout, two mugs: the order failed. It was found in production, by a customer.

```
  the catalog renamed priceCents to price and released. checkout, 2 mugs: total -1, meaning the order failed.
  it was found in production, by a customer.
```

### The Consumer Writes A Pact

Each consumer's own client is run against Pact's mock of the catalog, and agrees. Two pact files are written. Checkout's pact: price cents, an integer, and sku, a string. Reports' pact: sku, a string.

```
  each consumer's own client was run against Pact's mock of the catalog, and agreed: true. two pact files were written.
  checkout's pact: {priceCents=integer, sku=string}.
  reports' pact: {sku=string}.
```

### The Provider Replays The Pacts

Pact replays each pact against the real catalog, over HTTP. Two interactions checked, no problems. Safe to release.

```
  Pact replays each pact against the real catalog over HTTP. interactions checked: 2, problems: []. safe to release.
```

### The Rename Is Caught

On the renamed release: two interactions checked, one failed. Checkout: the actual map is missing the following keys: price cents. The build fails, and Pact names the consumer and the field. Reports' pact still passes.

```
  interactions checked: 2, failed: 1.
  checkout - body: Actual map is missing the following keys: priceCents
  the build fails, and Pact names the consumer and the field. reports' pact still passes.
```

### Adding Is Safe

A release that adds a stock field: two interactions checked, no problems. Adding a field breaks nobody.

```
  a release that adds a stock field. interactions checked: 2, problems: [].
```

### The Bill

A release that now sends pounds, not pence, in the same field: no problems. It passes. Checkout, two mugs: total thirty two, where it should be thirty two hundred. A pact checks the shape, and not the meaning. And every consumer must keep its pact up to date, or the check protects nobody.

```
  a release that now sends pounds, not pence, in the same field. problems: []. it passes.
  checkout, 2 mugs: total 32, where it should be 3200.
  a pact checks the shape, and not the meaning. and every consumer must keep its pact up to date, or the check protects nobody.
```

## The verdict

Let each consumer write a pact for what it reads, and only that. Run the provider's verification in its build, against the real service. Keep pact files where the provider's build can find them, or in a broker. And add tests for meaning, since a pact checks only shape.

## How to recognise this in code you did not write

- A `@Pact` method or `ConsumerPactBuilder` in a consumer's tests.
- `@Provider` and `@PactFolder` or `@PactBroker` in a provider's tests.
- A `pacts` folder of JSON files.
- `can-i-deploy` in a pipeline.

## Where you have already met this

Many microservice teams, and Pact Broker or PactFlow in their pipelines.

## When this is too much

If provider and consumer are one team with one release, an ordinary test is enough. Pact pays off across teams that release apart.

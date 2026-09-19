# Retry with Resilience4j, Explained

## The pattern in one sentence

In Resilience4j, a retry is an annotation on a method, and the attempts and waits are configuration.

## What is new here

The pattern is [Retry with Backoff](../retry-pattern). This page is only what Resilience4j adds.

### A Flaky Call, Retried

The gateway times out twice, and the third attempt works. The caller never sees the failures.

```
  the gateway times out twice. the caller gets: R-1. gateway calls: 3.
```

### Backoff

The wait before the first retry is one millisecond, and before the second, two. Each wait doubles.

```
  waits before each retry, in milliseconds: [1, 2].
  each wait is twice the one before, so a struggling gateway is given room.
```

### Giving Up

When the gateway never answers, the retry stops after three attempts and the caller gets the exception.

```
  the gateway never answers. after 3 attempts the caller gets: GatewayTimeout.
```

### Not Everything Is Worth Retrying

A declined card will decline again. The exception list retries only timeouts, so it makes one attempt. Retrying everything makes three.

```
  a declined card, retried only on timeouts: 1 attempt.
  the same card, retrying everything: 3 attempts against a card that will decline again.
```

### A Retry Can Charge Twice

The charge went through, but the answer was lost, so the retry charged again. With an idempotency key, the gateway recognises the repeat and charges once.

```
  the charge went through but the answer was lost. no idempotency key. charges made: [4999, 4999].
  the same failure, with an idempotency key. charges made: [4999].
```

### Retries Multiply

Checkout retries three times, and each of those retries the gateway three times. One dead gateway and one customer make nine calls.

```
  checkout retries three times, and each of those retries the gateway three times.
  one dead gateway, one customer: 9 calls.
```

## The verdict

Retry only temporary failures. Send an idempotency key with every call that changes something. Retry in one layer, not two. Keep the attempts and the waits small.

## How to recognise this in code you did not write

- `@Retry(name = ...)`.
- `resilience4j.retry.instances.*` in configuration.
- `retry-exceptions` and `ignore-exceptions` lists.

## Where you have already met this

Any Spring service that calls a payment, email or shipping provider over the network.

## When this is too much

For a call that fails for a reason that will not go away, a retry only delays the error.

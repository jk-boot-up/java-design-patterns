# Problem Statement

## Read the partner first

This project assumes [Retry with Backoff](../retry-pattern), which retried a flaky payment gateway with a growing wait between attempts, and showed why a retry is safe only when the failure is temporary and the operation cannot happen twice. Nothing here is lost by skipping Resilience4j, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a payment gateway that fails one call in five, and a checkout that must not lose a sale or charge twice.

## What is new

**Resilience4j** has the retry built in. You put an annotation on the method, and set the attempts, the waits and the exceptions in `application.properties`.

```
  the gateway times out twice. the caller gets: R-1. gateway calls: 3.
```

## The failure this project exists to show

Retries stack: two annotated layers multiply their attempts. An exception list that is too wide retries a card that will decline again. And the library cannot tell you whether doing the call twice is safe.

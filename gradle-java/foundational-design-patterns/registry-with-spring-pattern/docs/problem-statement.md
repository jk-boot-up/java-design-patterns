# Problem Statement

## Read the partner first

This project assumes [Registry](../registry-pattern), which builds a static registry and
shows its costs. Nothing here is lost by skipping Spring, and [`dependencies.md`](dependencies.md)
says so plainly.

## The scenario

The partner's: a checkout needing a discount policy, a payment gateway and a notifier.

## What is new

`Registry.get(PaymentGateway.class)` is `context.getBean(PaymentGateway.class)`.

```
ONE. The ApplicationContext is the registry.
  registered by declaration: @Component on a class. beans of type PaymentGateway: [recordingGateway]
  no static map, no register() calls scattered through the code, and a missing bean fails at start-up.
```

## The failure of its own

Spring's test support **caches** the context and reuses it, so a singleton's state leaks
from one test to the next. The hand-built registry's order-dependent failure returns.

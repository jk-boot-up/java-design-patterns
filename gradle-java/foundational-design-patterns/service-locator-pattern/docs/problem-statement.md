# Problem Statement

## The scenario

The same as Registry's: a checkout needs a discount policy, a payment gateway and a
notifier, and the registry's problems are now felt.

## What Service Locator adds to a registry

A registry holds things. A locator holds **recipes**.

```
ONE. The advance over a registry: it creates, and decides how long things live.
  nothing has been asked for yet: gateways made 0, notifiers made 0
  three finds of each: gateways made 1 (a singleton), notifiers made 3 (a new one each time).
```

It creates lazily, and manages lifetimes. And it can be swapped for a test:

```
TWO. The other advance: it can be swapped for a test.
  the checkout charged the fake we configured: [9000]
```

That is a genuine step forward, and the project says so.

## What this project must deliver

The failures, as runnable evidence rather than assertion, and an honest account of
where the pattern is still used and why.

# Problem Statement

## Read the partner first

This project assumes [Blue-Green and Canary](../blue-green-and-canary-pattern), which ran two releases of the checkout behind a router that was a rule on the request number, and showed an in-place upgrade failing requests, a switch and a switch back, a canary, and a gate that halts a bad release. Nothing here is lost by skipping Kubernetes, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a checkout with a good release and a release that fails on big orders.

## What is new

**Kubernetes**, run locally with kind inside Docker: two real Deployments, a real Service whose selector is the switch, and real pods that a canary spreads traffic over.

```
  v1 stopped to make room for v2. 20 requests while nothing is running: failed 20 of 20.
```

## The failure this project exists to show

A canary's spread is chosen by the cluster's own rules, not by a formula, so its numbers change from run to run. And the first step of a gate can be too small a sample to see a bug.

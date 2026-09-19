# Problem Statement

## Read the partner first

This project assumes [Service Locator](../service-locator-pattern), which shows the advances of a locator over a
registry and the failures that made it an anti-pattern. Nothing here is lost by skipping Consul, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's checkout, with its collaborators now on the other side of a network. A payment gateway runs as two
instances, and a notifier as one. Their addresses are not known until they are running.

## What is new

The locator is no longer a map inside the JVM. It asks Consul, and Consul answers with what is really running.

```
ONE. The locator asks Consul, and Consul answers with what is really running.
  healthy payment-gateway instances Consul reports: 2
  four orders placed. served by gateway-1: 2, by gateway-2: 2.
  LocatorCheckout never knew an address. it asked for "payment-gateway" by name.
```

## What this project must deliver

The genuine advance, the old costs shown again over a network, a new one, and the alternative.

# Problem Statement

## Read the partner first

This project assumes [Service Registry and Discovery](../service-discovery-pattern), which let three copies of the Pricing service announce themselves to a shared registry, so a caller asked for an address each time instead of holding one, and showed that a registry is only as good as its last update. Nothing here is lost by skipping Spring Cloud Consul, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: three copies of Pricing that come and go with deployments and crashes.

## What is new

**Spring Cloud Consul** registers each copy with a real Consul agent when it starts, with a health check, and lets a client ask Consul by service name.

```
  the client was given the name pricing and no address.
  Consul lists: [pricing-1, pricing-2, pricing-3].
  nobody told Consul. each copy registered itself when it started.
```

## The failure this project exists to show

A crash leaves the registration in place until a health check fails. The client has no list of its own when Consul goes away. And the check interval is a trade between speed and load.

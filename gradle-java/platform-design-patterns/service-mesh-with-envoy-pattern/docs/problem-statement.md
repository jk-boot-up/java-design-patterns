# Problem Statement

## Read the partner first

This project assumes [Service Mesh](../service-mesh-pattern), which showed three services with three retry behaviours, one mesh policy giving them all the same, a policy changed in one place, an unknown caller turned away, and counts kept by the proxies. Nothing here is lost by skipping Envoy, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: services calling a payment service that is having a bad day.

## What is new

**Envoy**, a real proxy in a Docker container, retries, refuses callers and counts requests, to a policy written in its configuration.

```
  the payment service refuses its first 2 calls, for each caller in turn. with retry code of 3, 0 and 1 tries: checkout worked, refunds failed, reports failed.
  three services, three copies of the retry code, three different behaviours.
```

## The failure this project exists to show

Retries multiply the calls the payment service receives. The policy is a configuration file that must be right. And a caller's name here is a header, where a real mesh checks a certificate.

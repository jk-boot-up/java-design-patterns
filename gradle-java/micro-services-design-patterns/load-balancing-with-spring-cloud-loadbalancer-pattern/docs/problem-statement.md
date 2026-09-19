# Problem Statement

## Read the partner first

This project assumes [Client-Side Load Balancing](../load-balancing-pattern), which chose among three copies of the catalogue service on the client side, with four hand-written strategies, and showed that a fair strategy is not always a fast one. Nothing here is lost by skipping Spring Cloud LoadBalancer, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: three copies of the catalogue service, two fast and one on older hardware.

## What is new

**Spring Cloud LoadBalancer** does the choosing inside the HTTP client. The caller writes a service name in the URL, and the balancer turns it into an address on every request.

```
  requests answered by copy-a, copy-b, copy-c: [4, 4, 4].
  the caller wrote http://catalogue/... and never saw an address. the default is round robin.
```

## The failure this project exists to show

Round robin is fair, not fast. Without health checks, a stopped copy still gets its share. And a load-balanced client treats every host name as a service name.

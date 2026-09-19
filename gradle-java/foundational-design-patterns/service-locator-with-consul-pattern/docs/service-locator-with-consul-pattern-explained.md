# Service Locator with Consul, Explained

## The pattern in one sentence

A locator that asks a service registry which instances of a service are healthy.

## The genuine advance

Instances come and go, and the caller's code does not change.

```
TWO. The genuine advance: instances change and the caller's code does not.
  gateway-1's health check is marked failing. healthy instances now: 1
  four more orders. gateway-1 served 0, gateway-2 served 4.
  gateway-1 recovers and is used again: healthy instances 2.
```

A static registry could never do this. Where an instance is, is a genuine run-time fact, which is the
legitimate use the partner project described.

## The old costs, over a network

**The names are strings, and the compiler says nothing.**

```
THREE. The bill: the names are strings, and the compiler says nothing.
  a typo, "payment-gatway", compiled. at run time: no healthy instance of "payment-gatway"
  then, on a real order: no healthy instance of "notifier"
  and the payment gateway had already been called: 1 charge went through.
```

The failure arrived in production, after the money moved: the same bill as the hand-built locator.

## A new cost: a cached answer goes stale

A locator that asks Consul on every call is slow, so it is tempting to remember answers.

```
FOUR. The bill: a cached answer goes stale.
  gateway-1 dies, and Consul is told. the cache is not.
  the cached address is still handed out, and the call fails: could not reach the dead instance: ConnectException
  Consul was asked 1 time in total. faster, and wrong.
  the uncached locator recovers at once
```

Deciding when to refresh is now your problem.

## The alternative: be given

Instead of every class asking, give the caller one address and let something else keep it correct. Here that
is nginx in a Docker container, given the healthy instances once, from Consul.

```
FIVE. The alternative: do not ask. be given.
  the caller was given one address, nginx's, and asked nothing. 4 of 4 requests succeeded.
  gateway-2 is stopped. 4 of 4 more requests still succeed: all 4 were served by gateway-3, because nginx retried the next instance.
  the class never knew, because it never looked anything up.
```

This is [Dependency Injection](../dependency-injection-pattern)'s idea at the level of a network address: the class
is given, and does not ask. Kubernetes DNS, a service mesh and a load balancer are the same move.

## The verdict

Service discovery is the strongest case for a locator, because where instances are is a run-time fact. Even so,
prefer to be given an address by the platform, a proxy or DNS, than to have every class ask.

## How to recognise this in code you did not write

- `DiscoveryClient.getInstances("name")` in Spring Cloud.
- A Consul, Eureka or ZooKeeper client used inside business classes.
- A service name as a string, resolved to a URL at call time.
- A `@LoadBalanced` client, where the lookup is hidden behind an annotation.

## Where you have already met this

Spring Cloud's `DiscoveryClient`, Netflix Eureka, and Consul itself. Kubernetes' built-in DNS is the given form.

## When this is too much

For a fixed set of services with fixed addresses, configuration is simpler and needs no registry at all.

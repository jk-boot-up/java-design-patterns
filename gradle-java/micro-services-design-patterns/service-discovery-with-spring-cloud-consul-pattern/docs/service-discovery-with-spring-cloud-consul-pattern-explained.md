# Service Discovery with Spring Cloud Consul, Explained

## The pattern in one sentence

With Spring Cloud Consul, a service registers itself at startup, and a client asks the registry for healthy copies by name.

## What is new here

The pattern is [Service Registry and Discovery](../service-discovery-pattern). This page is only what Spring Cloud Consul adds.

### Three Copies Announce Themselves

Three copies of Pricing start. Consul lists all three, and nobody told it.

```
  the client was given the name pricing and no address.
  Consul lists: [pricing-1, pricing-2, pricing-3].
  nobody told Consul. each copy registered itself when it started.
```

### Requests Find Them

Six requests to the name pricing are answered twice by each copy.

```
  six requests to http://pricing/...: {pricing-1=2, pricing-2=2, pricing-3=2}.
```

### A Deployment Moves A Copy

One copy restarts on a new port. The address written down for it fails. The name still works.

```
  pricing-1 restarted on a new port.
  a hardcoded address to pricing-1 now fails: ResourceAccessException.
  by name, six requests: {pricing-1=2, pricing-2=2, pricing-3=2}.
```

### A Graceful Stop Is Noticed At Once

A copy that shuts down properly removes itself, and the list shrinks at once.

```
  pricing-3 stopped. Consul lists, immediately: [pricing-1, pricing-2].
  six requests: {pricing-1=3, pricing-2=3}.
```

### A Crash Is Not

A copy that crashes says nothing. Consul still lists it, and half the requests fail, until its health check fails and it is removed.

```
  pricing-2 crashed without a word. Consul lists, straight away: [pricing-1, pricing-2].
  six requests while the entry is stale: {failed=3, pricing-1=3}.
  after its health check fails, Consul lists: [pricing-1] (removed: true).
  six requests: {pricing-1=6}.
  the list is only as good as its last check. that is the taxi rank's catch.
```

### The Registry Itself Goes Away

When Consul stops, the client cannot ask it. It kept no list of its own.

```
  Consul stopped. asking it for pricing: ResourceAccessException.
  the client remembered nothing. a last-known-good list is the client's job.
```

## The verdict

Register at startup, deregister on shutdown, and choose the check interval on purpose. Expect stale entries after a crash and retry across copies. Give the client a last-known-good list for the day the registry is down.

## How to recognise this in code you did not write

- `spring.cloud.consul.discovery.*` in configuration.
- A `DiscoveryClient` bean, or a URL whose host is a service name.
- An actuator health endpoint that a registry calls.

## Where you have already met this

Platforms that run many small services and need them to find each other.

## When this is too much

With three services on fixed hosts that rarely change, a configuration file is simpler than a registry.

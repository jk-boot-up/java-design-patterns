# Load Balancing with Spring Cloud LoadBalancer, Explained

## The pattern in one sentence

In Spring Cloud LoadBalancer, the caller uses a service name, and a balancer picks a copy for each request.

## What is new here

The pattern is [Client-Side Load Balancing](../load-balancing-pattern). This page is only what Spring Cloud LoadBalancer adds.

### Twelve Requests, One Name

Twelve requests to one service name are spread four, four and four.

```
  requests answered by copy-a, copy-b, copy-c: [4, 4, 4].
  the caller wrote http://catalogue/... and never saw an address. the default is round robin.
```

### Fair Is Not Fast

Copy c costs six times as much per request. Round robin gives it a third of the requests, so it does most of the work.

```
  work done, counting the old machine as six times a fast one: [4, 4, 24].
  the slow copy did the most work, because round robin gives every copy the same number of requests.
```

### A Strategy Of Our Own

A balancer that sends each request to the copy with the least work so far gives the slow copy one request, and evens the work out.

```
  least work so far, twelve requests: [6, 5, 1]. work done: [6, 5, 6].
  registered for one service name, catalogue-fast. the name catalogue still uses round robin.
```

### A Copy Goes Down

Copy b is stopped, but it is still in the list, so a third of the requests are sent to it and fail.

```
  copy-b is stopped. 12 requests: 4 failed, 8 answered.
  the list still holds copy-b, so a third of the requests are sent to it.
```

### A Retry Lands Elsewhere

With one retry allowed, all twelve are answered, because the second attempt goes to the next copy.

```
  the same 12 requests, each allowed one retry: 12 answered. some needed a second attempt: true.
  the retry is the caller's, and a balancer without health checks only spreads the failures.
```

### Only For Names

A balanced client treats every host as a service name. An unknown name and a real address both fail.

```
  a name the balancer has no instances for: IllegalStateException.
  a real address on a load-balanced client: IllegalStateException.
  a load-balanced client treats every host as a service name.
```

## The verdict

Use the default until work is uneven. Add health checks or retries, because a balancer alone spreads failures. Use service names, never addresses, on a balanced client.

## How to recognise this in code you did not write

- `@LoadBalanced` on a client builder.
- A URL whose host is a service name.
- `@LoadBalancerClient(name = ...)`.

## Where you have already met this

Any Spring service that calls another by name.

## When this is too much

With one copy of a service, there is nothing to balance.

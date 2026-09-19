# Circuit Breaker with Resilience4j, Explained

## The pattern in one sentence

In Resilience4j, a circuit breaker is an annotation on a method, and its thresholds are configuration.

## What is new here

The pattern is [Circuit Breaker](../circuit-breaker-pattern). This page is only what Resilience4j adds.

### Healthy

A healthy call passes through the closed breaker.

```
  page shows: [Blue Mug Set, Tea Towel]. breaker: CLOSED. backend calls: 1.
```

### The Service Goes Down

The service goes down. The window holds the last four calls, and the healthy one is still in it. At the third failure, three of four have failed, and the breaker opens. The fourth call never reaches the service.

```
  call 1: page shows []. breaker: CLOSED. backend calls: 2.
  call 2: page shows []. breaker: CLOSED. backend calls: 3.
  call 3: page shows []. breaker: OPEN. backend calls: 4.
  call 4: page shows []. breaker: OPEN. backend calls: 4.
```

### Open: Fail Fast

A hundred more page views send nothing to the service. The breaker refuses each one, and the fallback answers.

```
  100 more page views. backend calls: 0 more. breaker: OPEN.
  calls refused by the breaker: 100. the page never saw an error.
```

### Half-Open: One Probe

Half-open lets one call through. While the service is down it fails and the breaker opens again. Once the service is back, the probe succeeds and the breaker closes.

```
  service still down. one probe reached it (1 call). breaker: OPEN.
  service back. the probe shows: [Blue Mug Set, Tea Towel]. breaker: CLOSED.
```

### What Counts As A Failure

Bad requests for a product that does not exist are the caller's fault. One breaker ignores them and stays closed. The other counts them and opens.

```
  8 requests for a product that does not exist.
  breaker that ignores IllegalArgumentException: CLOSED.
  breaker that counts everything: OPEN.
```

### The Annotation Is A Proxy

A method that calls its own protected method on this skips the proxy. All ten errors reach the caller, all ten calls reach the service, and the breaker never notices.

```
  10 calls through this. errors that reached the caller: 10. backend calls: 10.
  breaker: CLOSED. it never saw a call.
```

## The verdict

Configure the window and the threshold on purpose. List the exceptions that are not failures. Alert on the breaker's state, since the fallback hides the errors. Call protected methods from outside the bean.

## How to recognise this in code you did not write

- `@CircuitBreaker(name = ..., fallbackMethod = ...)`.
- `resilience4j.circuitbreaker.instances.*` in configuration.
- A fallback method that takes the original arguments and a `Throwable`.

## Where you have already met this

Any Spring service that calls another service over the network and must keep serving when it fails.

## When this is too much

For a call that is local, fast and reliable, a breaker is only more code.

# Rate Limiter, Explained

## The pattern in one sentence

A rate limiter refuses requests beyond an agreed rate, so that one caller cannot use up a service that everyone shares.

## The six acts

### No Limit

The search can serve a hundred a second. A client sends a thousand, all are accepted, and nine hundred are beyond capacity, so everyone else waits behind them.

```
  the product search can serve 100 requests a second. a client sends 1000 in one second.
  accepted: 1000. beyond what it can serve: 900, and every other customer waits behind them.
```

### A Bucket Of Tokens

A bucket of ten, refilled at five a second, allows ten of a burst of twenty. A second later it allows five. After ten quiet seconds it is full again, and no fuller.

```
  a bucket of 10 tokens, refilled at 5 a second. a burst of 20 at once: 10 allowed, 10 refused.
  one second later, another 20: 5 allowed.
  after ten quiet seconds the bucket is full again, and no more than full: 10 allowed.
```

### A Steady Rate Always Gets Through

Five requests a second, evenly spaced, for a whole minute, are all allowed: three hundred of three hundred. A burst is tolerated up to the size of the bucket, and a sustained rate above the refill is not.

```
  5 requests a second for a minute, evenly spaced: 300 of 300 allowed.
  a burst is tolerated up to the size of the bucket. a sustained rate above the refill is not.
```

### One Bucket For Everyone, Or One Each

With one shared bucket, a greedy client takes all ten tokens and a polite client is refused. With a bucket each, the greedy client is held to ten, and the polite client is allowed.

```
  one shared bucket: the greedy client takes 10. the polite client's one request: refused.
  a bucket each: the greedy client gets 10 of 20. the polite client's one request: allowed.
```

### Say When To Come Back

An empty bucket refuses and says to retry after a thousand milliseconds. One millisecond early is refused, and at the stated moment the request is allowed.

```
  the bucket is empty. the refusal says: retry after 1000 milliseconds.
  one millisecond early: refused.
  at the moment it said: allowed.
```

### The Bill

Three servers each with their own bucket allow thirty, three times the limit. Ten thousand callers mean ten thousand buckets. And a real page that loads twelve things at once gets only ten.

```
  three servers, each with its own bucket of 10: a burst of 90 is allowed 30 times, not 10. the limit is three times looser than it says.
  10000 different callers: 10000 buckets to keep in memory.
  and a real page that loads 12 things at once gets 10 of them. the limit cannot tell a person from a script.
```

## The verdict

Use a rate limiter on any service that shared callers can overwhelm, and on any API you expose. Use a token bucket to allow short bursts, key it by caller, and tell refused callers exactly when to retry. Share the count across servers if the limit must be exact. Set the burst size from real page loads, not from a guess.

## How to recognise this in code you did not write

- A `429 Too Many Requests` response, with a `Retry-After` header.
- A class named `Bucket`, `Limiter` or `Throttle`.
- Resilience4j's `RateLimiter`, Guava's `RateLimiter`, or a gateway plugin.
- A limit written in the API documentation, such as 100 requests a minute.

## Where you have already met this

Every public API you have called, GitHub, Stripe, Twitter, and every API gateway.

## When this is too much

For an internal service with one known caller, a limit is only a way to fail. It earns its place with many or unknown callers.

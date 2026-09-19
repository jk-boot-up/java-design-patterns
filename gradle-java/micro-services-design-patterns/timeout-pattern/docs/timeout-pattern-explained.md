# Timeout, Explained

## The pattern in one sentence

A timeout is a limit on how long you will wait for an answer, so that a slow or silent service cannot hold you forever.

## The six acts

### No Timeout

The supplier never answers, and the product page's thread waits, with no limit on for how long. The customer is looking at a spinner.

```
  the supplier never answers. the product page's thread is: WAITING, with no limit on for how long.
  nothing in the code says it will ever come back, and the customer is looking at a spinner.
```

### A Limit On The Wait

With a limit of a hundred milliseconds, the page shows stock unknown, try again shortly, and loads without the number it could not get.

```
  the same call, with a limit of 100 milliseconds: the page shows "stock unknown, try again shortly".
  the page loaded, without the number it could not get.
```

### Giving Up Does Not Stop The Work

The caller gave up, but the call at the supplier had only started. Later the supplier finishes it anyway, with nobody waiting.

```
  the caller gave up. calls started at the supplier: 1, finished: 0.
  later the supplier finishes anyway: finished 1. nobody was waiting for the answer, and the work was done.
```

### Choosing The Number

On a typical hundred calls, fifty milliseconds lets only fifty four succeed, a hundred lets ninety, two hundred fifty ninety eight, and only three seconds lets all one hundred. Too tight fails healthy calls. Too loose holds a thread for seconds.

```
  a limit of   50 ms: 54 of 100 calls succeed.
  a limit of  100 ms: 90 of 100 calls succeed.
  a limit of  250 ms: 98 of 100 calls succeed.
  a limit of 1000 ms: 98 of 100 calls succeed.
  a limit of 3000 ms: 100 of 100 calls succeed.
  too tight and healthy calls fail. too loose and a slow supplier holds a thread for seconds.
```

### One Budget For The Page

Three calls in a row, each allowed a second, could take three seconds. One budget of a second shared by all three answers the first, cuts off the second, and skips the third, for one second in total.

```
  a page makes 3 supplier calls in a row, each allowed 1000 ms. the worst case for the page is 3000 ms.
  with one budget of 1000 ms shared by all three: call 1: answered at 400 ms. call 2: cut off at 600 ms. call 3: skipped, no budget left. total 1000 ms.
```

### The Bill: You Do Not Know What Happened

A payment call times out, and the customer is told it failed. The provider then completes the charge anyway. A timeout says only that you stopped waiting.

```
  the payment call timed out. the customer is told: we could not take your payment.
  the payment provider then completed the charge: charges taken 1. the customer thinks nothing was taken.
  a timeout says only that you stopped waiting. retrying a payment without an idempotency key would charge again.
```

## The verdict

Put a timeout on every call to another system, chosen from how long the calls really take, and set it on the caller's side. Share one budget across a chain of calls. Decide what to show when time runs out. And never treat a timeout as a failure of the operation: it may have happened, so make the operation safe to ask about or repeat.

## How to recognise this in code you did not write

- `Future.get(timeout, unit)` and `CompletableFuture.orTimeout`.
- A `connectTimeout` and a `readTimeout` on an HTTP client.
- A `TimeoutException` or an HTTP 504 in a log.
- Resilience4j's `TimeLimiter`, and Spring's `@Timeout`-style settings.

## Where you have already met this

Every HTTP client and database driver has a timeout setting, and the default is often none.

## When this is too much

A timeout is never too much. The cost is choosing it well, and handling the case where it fires.

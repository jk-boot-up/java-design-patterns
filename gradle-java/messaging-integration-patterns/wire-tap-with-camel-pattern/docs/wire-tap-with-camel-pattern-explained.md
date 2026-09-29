# Wire Tap with Apache Camel, Explained

## The pattern in one sentence

With Camel, a wire tap is one `wireTap()` step that copies each message to a
side route on its own thread; `onPrepare()` makes the copy independent.

## The 5 acts

### 1. A tap on the route

One step, `wireTap("direct:audit")`, goes into the payments route. Every
message, the refund included, is copied to the audit route, which masks the
card number and records a line: four of four. The payment service handles all
four payments as before, and neither checkout nor the payment service changed.

### 2. Not a copy after all

Camel's tap is handed the same message object as the main route, not a copy.
The audit's masking therefore changed the real payment instruction: checkout's
own ORD-1 message now reads card **** 1234. In a real payment system, that is
a charge that fails.

### 3. onPrepare: a real copy

`onPrepare()` runs on the tap's message before it is sent. Replacing the body
there with a fresh copy gives the audit its own object. The audit still gets
four masked lines, and checkout's ORD-1 message keeps its full card number.

### 4. The audit stops

The audit route is stopped, as it might be for maintenance. ORD-4 is sent:
the tap's copy fails, but that failure stays on the tap's side. ORD-4 is
charged, and neither checkout nor the payment service ever hears about it.

### 5. The bill

The audit is made slow: 100 milliseconds per copy. Four payments still take
under 0.3 seconds, not the 0.4 seconds four slow copies add up to, because the
tap runs on its own thread. The price is lag: the audit catches up only later,
and copies waiting in memory are lost if the program stops. A real audit
should tap to a durable queue.

## The verdict

Use `wireTap()` for auditing and monitoring without touching sender or
receiver. Always make the copy independent, watch the tap's errors
separately, and tap to a durable queue when no copy may be lost.

## How to recognise this in code you did not write

- `.wireTap("...")` in a route.
- `.onPrepare(...)` after a wire tap.
- An audit or metrics route fed from a tap.

## Where you have already met this

- Camel's `wireTap()` and Spring Integration's `wire-tap` interceptor.
- Port mirroring on network switches.
- Kafka consumers that read a topic purely for auditing or analytics.

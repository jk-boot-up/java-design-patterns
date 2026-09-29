# Wire Tap, Explained

## The pattern in one sentence

A wire tap copies every message on a channel to a second listener, while the
original is delivered unchanged, so traffic can be observed without touching
senders or receivers.

## The 5 acts

### 1. Logging typed in by hand

Someone added logging inside `PaymentService`'s charge path. Four messages
are sent; three are logged, because the refund path has no logging. And the
log lines contain complete card numbers.

### 2. A wire tap

An `AuditLog` is attached to the channel as a wire tap. Every message, charge
or refund, is copied to it with the card masked to its last four digits, and
the payment service handles all four as before. Neither checkout nor the
payment service was changed.

### 3. Attach and detach

When the investigation is over, the tap is detached. ORD-4 flows through as
normal, and the audit log still holds its four lines. Taps come and go
without touching the services.

### 4. A second tap

A second kind of tap, `SalesMeter`, adds up charges and subtracts refunds for
a dashboard. It sees the same traffic and reports net takings of £58.42.

### 5. The bill

Taps run in the channel's path. A tap that takes 100 milliseconds per copy,
such as one writing to a remote log, makes four payments take over 0.4
seconds. Run on its own thread, the same tap costs the payments under 0.05
seconds. And a tap sees everything, so sensitive data must be masked before
it is copied.

## The verdict

Use wire taps for auditing, debugging and dashboards. Mask sensitive data
before copying, run slow taps on their own thread, and detach taps you no
longer need.

## How to recognise this in code you did not write

- `wireTap(...)` in Camel routes or interceptors in Spring Integration.
- A separate consumer group reading a topic for auditing.
- Audit logs that are fed from the messaging layer, not from services.

## Where you have already met this

- Apache Camel's `wireTap` and Spring Integration's `wire-tap` interceptor.
- Kafka consumers in a separate group that read a topic for auditing.
- Network port mirroring for monitoring tools.
- Call recording in customer service centres.

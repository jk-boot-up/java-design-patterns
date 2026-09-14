# Prerequisites

What you need before starting this project, what you can pick up as you go, and
what you explicitly do not need to know. The short version: if you can read a
`try`/`catch` and a `for` loop, you are ready.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, `final` fields, constructors, records.
- **Exceptions** — `throw`, `catch`, and what `instanceof` means. The heart of this
  pattern is one `instanceof` check.
- **Lambdas, loosely.** `Retrier.call` takes a `Supplier<T>`, which in practice
  means you pass it `() -> payments.charge(request)`. You do not need to be
  comfortable writing functional interfaces; you need to be able to read that one
  line.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`. You do not need to be
  able to write one, though you will be invited to.

### Helpful, but explained as we go

- **The Load Balancing pattern** ([`../load-balancing-pattern`](../load-balancing-pattern)).
  Retry is what you do when the instance you chose does not answer, so the two
  combine naturally — the obvious retry is a retry against a *different* instance.
  You can do this project first without difficulty.
- **Idempotency.** It is the most important word in this project and it is defined
  in full below. If you have met it before, the only thing new here is how easy it
  is to break by accident.
- **What a payment gateway is.** "Somebody else's service that takes card payments
  over the internet" is entirely sufficient.

### Explicitly NOT required

- **Spring Retry or Resilience4j.** Neither appears here. The whole retrier is
  about forty lines of plain Java, and reading it once is worth more than
  configuring a library twice.
- **Any real payment integration.** No API keys, no sandbox account, no Stripe.
  `PaymentGateway` is an ordinary object you can tell to misbehave.
- **Threads or concurrency.** Everything runs on one thread, in a fixed order, so
  every number in the output is reproducible.
- **A network.** There is none. There is nothing to be offline from.

## A 60-Second "Idempotency" Primer

An operation is **idempotent** if doing it twice has the same effect as doing it
once.

Setting a light switch to "off" is idempotent — flick it off twice and the light is
off. Taking £449.99 from a card is not: do it twice and the shopper is £899.98 out
of pocket.

Most interesting operations are not naturally idempotent, so you make them
idempotent by attaching a key:

```java
public static PaymentRequest forOrder(String orderId, Money amount) {
    return new PaymentRequest(orderId, amount, "key-" + orderId);
}
```

The key is a promise from the caller: *if you have already seen this key, you have
already done this job — do not do it again, just tell me what happened last time.*

Two things about it are easy to get wrong and both are visible in this project.
The key must be derived from the **job** and nothing else — not the attempt number,
not the clock, not a random value — or the two attempts are not recognisably the
same job. And the promise is only worth anything if the *other* end keeps a record
of which keys it has seen. In `PaymentGateway` that record is one map, checked
before any money moves.

## A 60-Second "Backoff And Jitter" Primer

**Backoff** means the waits between attempts get longer: 100ms, then 200ms, then
400ms. `RetryPolicy` computes that by multiplying:

```java
long base = initialDelayMillis;
for (int i = 2; i < attempt; i++) {
    base *= multiplier;
}
```

The reason is that a service which is failing under load needs *less* traffic, not
the same traffic sooner.

**Jitter** is a small random amount added to each wait, so that two callers who
failed at the same moment do not retry at the same moment. In the demo you will see
`WAITED 103ms`, not 100. The three milliseconds are the jitter, and with a thousand
callers they are the difference between a trickle and a synchronised wave.

The jitter here comes from a seeded `Random`, so the demo and the tests produce the
same numbers on every machine. In production the seed comes from the machine, which
is the entire point.

## A 60-Second "Simulated Network" Primer

There is no network in this project, and there is no waiting.

`SimulatedClock` is a `long` with a method to move it forward; it never advances on
its own. When the retrier backs off for 103 milliseconds it pushes the clock
forward by 103 and continues immediately. When the gateway takes 50 milliseconds to
answer, it does the same.

So when the output says a recovered checkout took 203ms, that is arithmetic rather
than a measurement. It is identical on every machine, and the whole test suite —
backoff, jitter and all — finishes in about a second.

`CallLog` keeps the timeline: who called whom, when, and what happened, which is
what lets you read afterwards exactly how a double charge occurred.

## Software Prerequisites

- **JDK 21 or newer.** Nothing else.
- **Gradle:** not needed globally. The project ships a wrapper.

### Installing JDK 21

macOS, with Homebrew:

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk \
    /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

Linux (Debian or Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the
installer, and let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/retry-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 21 tests
./gradlew run          # expect four acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network
connection. Everything after that works offline, including the demo — because the
demo has no network to use.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**Every test in `NaiveCheckoutServiceTest` passes** — that is correct, and it is the
point of the file. One of those passing tests asserts that £899.98 left the
customer's account. A double charge is not detectable by asking "did it throw".

**Act four succeeds, and that bothers you** — good. It is supposed to. The checkout
returns a valid receipt, nothing is logged as an error, and the order looks
perfect. The damage is on a bank statement.

**The wait is 103ms and the docs said 100** — that is the jitter, and it is
deliberate. `baseDelayBeforeAttempt` gives you the promise without the jitter, which
is what the tests assert against.

**The numbers differ from the ones in the docs** — they should not. Every latency
comes from `SimulatedClock` and the jitter is seeded. If your output differs from
`README.md`, something has genuinely changed in the source.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — a flaky gateway, a lost fifth of
   the revenue, and the three-line loop that fixes it and charges people twice
2. Run `./gradlew run` and read the four acts, in order. Read the *last line* of
   each act — the number of times the card was charged.
3. [`retry-pattern-explained.md`](retry-pattern-explained.md) — the pattern, starting
   from an engaged tone
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) —
   the structure, then the five sequences
5. [`animation.html`](animation.html) — the attempts, the waits and the key, one
   step at a time
6. The tests, which are the specification: `RetryTest` first, then
   `NaiveCheckoutServiceTest` to see a passing test file that describes a disaster

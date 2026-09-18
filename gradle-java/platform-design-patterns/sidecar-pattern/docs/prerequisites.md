# Prerequisites

This project is written for beginners. If you can read a Java method and follow a
`for` loop, you have enough. Everything else is explained as it arrives.

There is no network, no Docker, no Kubernetes, no proxy server and no cloud
account. The whole project runs offline with a JDK and nothing else — which is
slightly funny, because the pattern is about running a second *process* beside
your service. Tier 1 teaches the shape and the arithmetic in one program, and is
honest in four separate places that it is doing so. The real second process lives
in `real/`, and you do not need it to understand anything here.

---

## Knowledge Prerequisites

### Required

- **Java basics** — classes, methods, fields, and reading a stack trace.
- **Exceptions** — `throw`, `catch`, and the idea that catching one lets you try
  again rather than give up.
- **Collections** — `List` and `Map`, and a `for` loop over a list.
- **The idea that one program can call another over a network, and that the call
  can fail for reasons that have nothing to do with either program.**

### Helpful, but explained as we go

- **Records** — Java's short syntax for "a value with named fields". Primer below.
- **Retry with backoff** — the loop at the centre of this project. Primer below.
- **Idempotency** — why charging the same card twice does not take money twice
  here. Primer below.
- **Reflection** — exactly one test asks a class which methods it declares, in
  order to assert that a method is *missing*. It is four lines and it is explained
  where it appears.

### Explicitly NOT required

- Any experience with Kubernetes, Istio, Envoy, Linkerd or nginx. Those names
  appear in the explained document as places you have already met this pattern,
  not as things you have to install.
- Any experience with Docker or containers.
- Any concurrency knowledge. Everything runs on one thread, in order, on a
  simulated clock that never actually sleeps.
- Any real payment provider. `PaymentGateway` is forty lines and fails on purpose.

---

## A 60-Second "Record" Primer

A `record` is Java's short way of saying "a value made of these named fields".

```java
public record SidecarConfig(int maxAttempts, long firstBackoffMillis,
                            long deadlineMillis, String tlsProfile) { }
```

That one line gives you a constructor taking all four values, a getter for each
named after the field — `config.maxAttempts()`, not `config.getMaxAttempts()` —
and value equality.

Records are immutable, and here that is the point rather than a detail. Four
proxies share **one** `SidecarConfig` object. If any of them could edit it, the
four copies would be back, just harder to see.

---

## A 60-Second "Retry With Backoff" Primer

When a call fails for a reason that might clear on its own, the sensible thing is
to wait and ask again. Waiting a *little longer each time* is called **backoff**.

```java
long backoff = firstBackoffMillis;
for (int attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
        return gateway.charge(NAME, payment, clock.now());
    } catch (PaymentFailed failure) {
        if (attempt < maxAttempts) {
            clock.waitFor(backoff);
            backoff *= 2;          // 200ms, then 400ms, then 800ms
        }
    }
}
```

Three numbers control it: how many attempts, how long the first wait is, and when
to abandon the whole thing however many attempts are left. Those three plus the
TLS profile are the four decisions this project is about.

Read that loop carefully once, because you are going to see it **five times** —
once in each of four services and once in the proxy. That repetition is not
sloppy writing. It is the problem, typed out.

---

## A 60-Second "Idempotency" Primer

If a payment attempt fails, you cannot always tell whether the provider took the
money before it failed. Retrying might charge the customer twice.

The way out is an **idempotency key**: the caller sends the same key with every
attempt for the same payment, and the provider promises that the second charge
with a key it has already seen returns the *first* result rather than taking more
money.

```java
public static Payment of(String orderRef, int amountPence) {
    return new Payment(orderRef, amountPence, "idem-" + orderRef);
}
```

`PaymentGateway` honours this with one line — `charged.computeIfAbsent(key, ...)`.
It matters here because a project whose central mechanism is "try again" would be
teaching you something dangerous if it quietly took the money twice.

---

## A 60-Second "Who Is Counting?" Primer

Every attempt count in this project is recorded by `PaymentGateway`, in a
`CallLog` the gateway owns. Not one number comes from a service's own tally.

That is deliberate, and it is the whole incident in one sentence: **a service's
belief about how many times it tried is exactly the thing that was wrong.**
Subscription billing believed it was making three attempts. It made six. Every
one of its own dashboards said three.

When you read the demo output, read it as the supplier's ledger, not as the
shop's.

---

## Software Prerequisites

| Need | Version | Check |
| --- | --- | --- |
| JDK | 21 or newer | `java -version` |
| Gradle | none — the wrapper is included | `./gradlew --version` |

Nothing else. No Docker, no network access at build time beyond Gradle fetching
JUnit once.

### Verify Your Setup

```bash
cd gradle-java/platform-design-patterns/sidecar-pattern
./gradlew test
./gradlew run
```

`test` should report 59 tests passing. `run` should print seven acts, ending with
`3 milliseconds, which is 1ms per attempt`.

Every number is fixed rather than random, and the clock is simulated, so two runs
print identical output. That is what lets the documents and the video quote exact
figures.

---

## Troubleshooting

**`./gradlew` says permission denied.** `chmod +x gradlew`.

**Gradle downloads things on the first run.** Expected, once, for the wrapper and
JUnit. After that, `./gradlew run --offline` works.

**The demo finishes instantly even though it waits 600 milliseconds.** `Clock` is
a counter, not a timer. `waitFor(200)` adds two hundred to a number and returns.
Nothing sleeps, which is why 59 tests run in under a second.

**The `£` signs or em dashes show as question marks.** Your terminal is not on
UTF-8. `export LANG=en_GB.UTF-8` usually fixes it.

**The columns look ragged.** The demo assumes a fixed-width font and about
seventy-six columns — there is a test that fails if any line grows past that.
Widen the window or reduce the font size.

**A test fails after I added `applyPolicyReview()` to `SubscriptionBillingService`.**
That is the test working, and it is the most important test in the project. The
absence of that method *is* the incident. If you want to see the fixed world, look
at the sidecars in Act 4 rather than repairing the fourth copy.

---

## Recommended Reading Order

1. `docs/problem-statement.md` — sixteen copies of four decisions, and the night
   three of them were updated.
2. `./gradlew run` — watch all seven acts before reading any source.
3. `docs/sidecar-pattern-explained.md` — the pattern, then the bill, then the
   admission that this is Decorator with a process boundary.
4. `docs/animation.html` — the two arrangements drawn side by side, and the night
   played out in both.
5. `docs/class-diagram.md` and `docs/uml-diagram.md` — the structure, and then the
   five sequences where the process boundaries are drawn as boxes.
6. The source, in this order: `Payment`, `PaymentGateway`, `CallLog`,
   `CheckoutService`, then `SubscriptionBillingService` (look for what is *not*
   there), then `SidecarConfig`, `Sidecar`, `ServiceBehindASidecar` and
   `Concerns`.
7. `real/` if you want to see an actual second process: nginx beside the service,
   with the retry policy in a config file nobody compiles.
8. `docs/session.md` if you are running this for a group.

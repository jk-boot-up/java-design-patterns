# Prerequisites

This project is written for beginners, but it is a **follow-on**. The one thing it assumes
is not a Java feature — it is the previous project.

Read [`sidecar-pattern`](../../sidecar-pattern) first. That project explains what a sidecar
is, why the retry code left the service, and what a second process costs. This one explains
none of that again. If you arrive here without it, the demo will look like a small program
about waiting, and the point will be invisible.

Everything else is ordinary Java. There is no network, no Docker and no Kubernetes in
Tier 1: the whole thing runs offline with a JDK and nothing else.

---

## Knowledge Prerequisites

### Required

- **The previous project.** Sidecar, in `../../sidecar-pattern`. This is the real
  prerequisite.
- **Java basics** — classes, methods, fields, interfaces, and a `for` loop.
- **Exceptions** — `throw`, `catch`, and the idea that catching one lets you try again.
- **The idea that one program can call another over a network**, and that the call can
  fail for reasons that have nothing to do with either program.

### Helpful, but explained as we go

- **Retry with backoff** — waiting a little longer before each attempt. Primer below.
- **Records** — Java's short syntax for a value with named fields. `ProxyPolicy` is one.
- **Reading an nginx configuration file** — you will see about twenty lines of it in the
  explained document. You do not have to be able to write one, and nothing here asks you
  to install nginx.

### Explicitly NOT required

- **Any nginx experience.** The one nginx behaviour that matters — retrying by moving to
  the next server in an upstream group, immediately — is explained in full where it comes
  up, twice, from two angles.
- **Any Docker or Kubernetes experience.** Those live in `real/`, which is optional.
- **Any concurrency knowledge.** One thread, in order, on a clock that never sleeps.
- **Any opinion about nginx.** This project is not a criticism of it. nginx was the right
  decision in §41 and it stays the right decision for almost everybody.

---

## A 60-Second "Retry With Backoff" Primer

When a call fails for a reason that might clear on its own, the sensible thing is to wait
and ask again. Waiting *longer each time* is called **backoff**, and it is the entire
subject of this project.

```java
long backoff = policy.firstBackoffMillis();
for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
    try {
        return charge(payment);
    } catch (PaymentFailed failure) {
        if (attempt < policy.maxAttempts()) {
            clock.waitFor(backoff);
            backoff *= 2;          // 200ms, then 400ms
        }
    }
}
```

Read the two proxies in this project side by side and you will find that loop in both, with
those four lines present in one and missing from the other. That is the difference, all of
it.

The doubling is not decoration. If every service in the shop retried after a fixed two
hundred milliseconds, they would all come back at the same instant and the provider's first
breath after a bad second would be the whole shop arriving at once.

---

## A 60-Second "Who Is Counting?" Primer

Every time in this project is recorded by `PaymentGateway`, at the **provider's** end, in a
log the provider owns. Not one number comes from a proxy's own tally.

That is the difference between a claim and evidence. A proxy that says it spaced its
retries out is a proxy reporting on itself. Arrival times measured at the far end are what
actually happened.

When you read the demo output, read it as the supplier's ledger.

---

## A 60-Second "What Is A Port, Here?" Primer

In Tier 1, `LocalPort` is an object with one field: whatever proxy is currently bound to
it. `install` puts something there, `vacate` empties it, and `send` hands a payment to
whoever is there — or throws *connection refused* if nobody is.

That is a fair model of one real thing and one real thing only: **the service's contract
with its proxy is an address, not a type.** It is not a model of sockets, TLS, or what an
operating system does when two processes want the same port. For those, go to `real/`.

---

## Software Prerequisites

| Need | Version | Check |
| --- | --- | --- |
| JDK | 21 or newer | `java -version` |
| Gradle | none — the wrapper is included | `./gradlew --version` |

Nothing else for Tier 1. Docker is needed only for `real/`, and that directory has its own
prerequisites.

### Verify Your Setup

```bash
cd gradle-java/platform-design-patterns/sidecar-java-proxy-pattern
./gradlew test
./gradlew run
```

`test` should report 30 tests passing. `run` should print seven acts, ending with a table
comparing twenty-two lines of nginx configuration against forty lines of Java.

Every number is fixed rather than random and the clock is simulated, so two runs print
identical output. That is what lets the documents and the video quote exact figures.

---

## Troubleshooting

**`./gradlew` says permission denied.** `chmod +x gradlew`.

**The demo finishes instantly even though it waits six hundred milliseconds.** `Clock` is a
counter, not a timer. `waitFor(200)` adds two hundred to a number and returns. Nothing
sleeps, which is why thirty tests run in under a second — and why the arrival times are
exactly 1, 202 and 603 on every machine.

**The `£` signs or em dashes show as question marks.** Your terminal is not on UTF-8.
`export LANG=en_GB.UTF-8` usually fixes it.

**The columns look ragged.** The demo assumes a fixed-width font and seventy-six columns;
a test fails if any line grows past that. Widen the window or reduce the font size.

**I added a retry loop to `PaymentsService` and a test failed.** That is the test working.
`ServiceStaysEmptyTest` reads the service's source with comments stripped and fails if the
words *retry*, *backoff*, *timeout*, *keystore* or *tls* appear in it. The service knowing
nothing about any of this is the claim the project makes; a test guards it rather than a
sentence.

**I added a second `new PaymentsService(...)` and a test failed.** Also the test working,
and it is the most important one here. There is exactly one construction in the whole
program, counted by reading the source, because *the service is never restarted* is not
something a demo should be trusted to remember.

---

## Recommended Reading Order

1. `../../sidecar-pattern` — all of it. This is not optional.
2. `docs/problem-statement.md` — the sentence nginx has no words for.
3. `./gradlew run` — watch all seven acts before reading any source.
4. `docs/sidecar-java-proxy-pattern-explained.md` — the swap, then the bill, which is
   longer than the benefit.
5. `docs/animation.html` — the two proxies' attempts drawn on one timeline.
6. `docs/sequence-diagram.md`, then `docs/uml-diagram.md` — the spacing, and then the four
   things the main story walks past.
7. The source, in this order: `ProxyPolicy`, `Proxy`, `NginxProxy`, `JavaProxy` (compare
   the last two line by line), then `LocalPort`, then `PaymentsService` — looking for what
   is *not* in it.
8. `real/` if you want to watch a real container replaced under a service that is not
   restarted.
9. `docs/session.md` if you are running this for a group.

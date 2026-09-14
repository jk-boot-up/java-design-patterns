# Prerequisites

What you need before starting this project, what you can pick up as you go, and what
you explicitly do not need to know. The short version: if you can read a `try`/`catch`
and an `enum`, you are ready.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, `final` fields, constructors, enums.
- **Exceptions** — `throw`, `catch`, and the idea that two different exception types
  can mean two different things. This project turns on exactly that: one exception
  means "a call was made and it timed out", the other means "no call was made at all".
- **Lambdas, loosely.** `CircuitBreaker.call` takes a `Supplier<T>`, which in practice
  means you pass it `() -> recommendations.suggestionsFor(sku)`. You need to be able
  to read that line, not to write functional interfaces from scratch.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`. You will be invited to
  write one, but you do not need to arrive able to.

### Helpful, but explained as we go

- **The Retry pattern** ([`../retry-pattern`](../retry-pattern)). This project is
  partly an argument about when retrying is the *wrong* tool, and act one is retry
  applied to an outage. You can do this project first without difficulty — the
  comparison is spelled out in full — but doing retry first makes act one land harder.
- **Timeouts.** "The call gives up after three seconds and throws" is entirely
  sufficient. There is no configuration to learn.
- **What a thread pool is.** Useful for the deepest version of the argument — why an
  outage in an optional feature can take down checkout — but the project explains the
  idea in words when it needs it.

### Explicitly NOT required

- **Resilience4j or Hystrix.** Neither appears here. The whole breaker is about a
  hundred lines of plain Java, and reading it once is worth more than configuring a
  library twice.
- **Threads or concurrency.** Everything runs on one thread, in a fixed order, so
  every number in the output is reproducible. The *argument* is about threads; the
  code is not.
- **A network.** There is none. There is nothing to be offline from.
- **Spring, Docker, Kubernetes or a service mesh.** None of them. A JDK is the whole
  toolchain.

## A 60-Second "Circuit Breaker" Primer

The name comes from the fuse box in a house, and so do the three states.

**CLOSED** is the healthy state, and this is the one piece of vocabulary that trips
everybody up. A closed circuit is one where current flows, so calls go through. An
**OPEN** circuit is a broken one, so calls do not. If that feels the wrong way round,
you are thinking of a door instead of a wire.

**HALF_OPEN** is the moment somebody is standing at the fuse box with a finger on the
switch: exactly one call is let through, to see what happens.

The rule in one breath: count consecutive failures while closed; at the threshold,
open; while open, refuse instantly without calling; after the reset wait, let one call
through — if it works, close; if it fails, open again for another full wait.

In this project the threshold is **3** and the reset wait is **5000ms**.

## A 60-Second "Why Not Just Retry" Primer

Retry asks: *did that call fail?*

A breaker asks: **is the next attempt plausibly going to work?**

For a dropped connection the answer is yes, so retry. For a service that has failed
the last twenty calls in a row the answer is no, and retrying is three more seconds
gone, one more thread held open, and one more call aimed at something already
struggling.

Act one of the demo measures it: nine seconds of waiting, three calls into a service
that is down, and a page identical to the one you would have got immediately.

## A 60-Second "Fallback" Primer

A breaker does not make failures disappear. It makes them fail **fast**. What that
speed buys you depends entirely on what you were calling.

Suggestions are **optional**, so there is something true to say instead: the shop has
no suggestions to show right now. The page goes out without them and the shopper can
still buy the espresso machine.

Payment is **essential**. There is nothing a shop can substitute for taking the money,
so the breaker buys no fallback there — it buys a fast, honest "no" instead of a
three-second spinner, which is still a better product.

And if you invent a fallback anyway, you get act five: a receipt for money that never
moved, no exception, no alert, and a warehouse shipping an espresso machine nobody
paid for. The test for whether a fallback is legitimate is simply **is it true?**

## A 60-Second "Simulated Network" Primer

There is no network in this project, and there is no waiting.

`SimulatedClock` is a `long` with a method to move it forward; it never advances on
its own. When a call to Recommendations "takes three seconds", it pushes the clock
forward by 3000 and returns immediately. When the breaker waits five seconds before
probing, nothing waits — the next call simply reads a clock that says 14000.

So when act two reports a total of 9000ms, that is arithmetic rather than a
measurement. It is identical on every machine, and all 26 tests finish in about a
second.

`CallLog` keeps the timeline: who called whom, when, and what happened. In act two the
timestamps *are* the argument — watch the left-hand column stop moving.

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

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the installer,
and let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/circuit-breaker-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 26 tests
./gradlew run          # expect five acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network connection.
Everything after that works offline, including the demo — because the demo has no
network to use.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**Every test in `RetryingProductPageServiceTest` passes** — that is correct, and it is
the point of the file. Retry applied to an outage is not a bug. It compiles, it
returns a correct page, and it costs nine seconds. Its tests assert the nine seconds.

**Act five succeeds, and that bothers you** — good. It is supposed to. The shopper is
thanked, the receipt looks real, nothing throws and no alert fires. The damage is that
zero cards were charged and the warehouse is shipping anyway.

**"Open" sounds like it should mean working** — you are not alone, and it is the one
thing worth memorising before the rest makes sense. Think of a wire, not a door. A
closed circuit carries current; an open one is broken.

**The clock jumps from 9000 to 14000 with nothing in between** — that is the reset
wait, and nothing happened during it because nothing needed to. The breaker has no
scheduler; it just compares the clock on the next call that arrives.

**The numbers differ from the ones in the docs** — they should not. Every millisecond
comes from `SimulatedClock`. If your output differs from `README.md`, something has
genuinely changed in the source.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — a service that stopped answering,
   and the retry loop that turns a broken feature into a nine-second page
2. Run `./gradlew run` and read all five acts, in order. In act two, read the
   **left-hand column** — the timestamps are the argument.
3. [`circuit-breaker-pattern-explained.md`](circuit-breaker-pattern-explained.md) —
   the pattern from a fuse box, and the half that gets left out
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, the state machine, then the five acts as sequences
5. [`animation.html`](animation.html) — the states, the refusals and the probe, one
   step at a time
6. The tests, which are the specification: `CircuitBreakerTest` first, then
   `FallbackChoiceTest` — which is where the interesting argument lives

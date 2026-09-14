# Prerequisites

What you need before starting this project, what you can pick up as you go, and what
you explicitly do not need to know. The short version: if you can read a `record` and
a lambda, you are ready.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, `final` fields, constructors, `List` and `Map`.
- **Records.** `Order`, `OrderDetailsPage`, `DeliveryStatus` and `Money` are all
  records. You need to be able to read `page.delivery().carrier()`, not to write
  compact constructors.
- **Lambdas, loosely.** `fanout.add("catalog", () -> catalog.namesFor(order.skus()))`
  passes a piece of work that has not been run yet. Being able to read that line is
  enough.
- **Exceptions** — `throw`, `catch`, and the idea that catching one somewhere other
  than where it was thrown is a deliberate design choice.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`.

### Helpful, but explained as we go

- **Database per Service** ([`../database-per-service-pattern`](../database-per-service-pattern)).
  That project is the reason this one exists: it takes the join away. You can do this
  project first without difficulty, but the previous one explains *why* nobody can
  just write a `SELECT` across three tables any more.
- **Latency as a number you can add up.** Nothing formal. "This call takes sixty
  milliseconds" is the whole model.
- **Basic probability.** Act five multiplies three numbers together. If
  `0.999 × 0.999 × 0.999` is familiar arithmetic, you have everything you need.

### Explicitly NOT required

- **`CompletableFuture`, threads, executors or virtual threads.** None of them appear.
  `Fanout` runs its branches in a loop and winds a fake clock back between them, which
  produces exactly the timeline parallel calls would produce without anything to
  reason about concurrently. The *pattern* is about parallelism; the code is not.
- **HTTP, gRPC, or any client library.** `RemoteCall` advances a clock. There is no
  network in this project.
- **GraphQL, BFFs, or a service mesh.** All of them are ways to arrange this pattern,
  and none of them are needed to understand it.
- **Spring, Docker, Kubernetes.** A JDK is the whole toolchain.

## A 60-Second "API Composition" Primer

One page needs data from three services, and no single service knows enough to build
it. So the code behind the page calls all of them and assembles the answer itself.

The mechanical half is one sentence: **sequential calls cost the sum of their
latencies, parallel calls cost the maximum.** Thirty plus sixty plus a hundred and
twenty is two hundred and ten milliseconds; the same three calls sent together cost
a hundred and fifty.

The harder half is that every dependency must be classified in advance as one the
page cannot live without or one it can, so that an outage in any single service has a
decided answer rather than an accidental one.

## A 60-Second "Required vs Optional" Primer

In this project:

- **Orders is required.** A page with no order on it is not a partial page, it is a
  blank one. If Orders is down the shopper gets an honest error, and that is the
  right answer.
- **Catalog is optional.** Without it the page shows `SKU-KETTLE` instead of
  *Stainless Steel Kettle*. The quantities and the money are still correct, because
  they were never Catalog's to know.
- **Shipping is optional.** Without it the delivery section says it cannot check.

In the code this is not configuration. It is which method the composer calls on a
branch: `value()` rethrows the failure, `valueOr(fallback)` substitutes. One line per
dependency, written by somebody who knows what the page is for.

## A 60-Second "Availabilities Multiply" Primer

A page that needs three services is up only when all three are up **at the same
moment**. Probabilities of independent things all happening are multiplied:

```
0.999 × 0.999 × 0.999 = 0.997
```

Each service, at 99.9%, is allowed about forty-three minutes of downtime a month. The
page gets a hundred and twenty-nine, because the three outages mostly do not overlap.

Three excellent services make a page worse than any one of them. The way out is not
better services — it is needing fewer of them, which is what making Catalog and
Shipping optional buys: the page is then up whenever Orders is up.

## A 60-Second "Simulated Network" Primer

There is no network here and no waiting.

`SimulatedClock` is a `long` with methods to move it; it never advances on its own.
`RemoteCall` "takes sixty milliseconds" by pushing the clock forward by sixty and
returning immediately.

`Fanout` is the interesting one. To make two calls look parallel it notes the
departure time, and before running each branch it winds the clock **back** to that
moment. At the end it moves the clock forward to the slowest arrival. So the timeline
it produces is the timeline two genuinely concurrent calls would have produced, and
`bothBranchesLeaveTogether` checks it.

`CallLog` keeps that timeline — who called whom, when, and what came back. In acts one
and two the timestamps *are* the argument.

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
cd micro-services-design-patterns/api-composition-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 22 tests
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

**Every test in `SequentialOrderDetailsComposerTest` passes** — that is correct, and it
is the point of the file. The sequential composer is not buggy. It returns the right
page and it costs 210ms, and its tests assert the 210ms.

**Act four throws and that looks like a failure** — it is the intended outcome. Orders
is required, so a missing order means no page. The test asserting it is called
`itRefusesToBuildAPageWithoutTheOrder`.

**Catalog and Shipping show the same start time and that looks wrong** — it is exactly
right. They left together. That shared departure is what makes the page cost 150ms
instead of 210ms, and `bothBranchesLeaveTogether` exists to keep it that way.

**There are no threads, so how is this parallel?** It is not, and it does not need to
be. `Fanout` winds the clock back between branches so the recorded timeline matches
what parallel calls would produce. The pattern is about which calls wait for which,
and that can be reasoned about exactly without concurrency.

**The numbers differ from the ones in the docs** — they should not. Every millisecond
comes from `SimulatedClock`. If your output differs from `README.md`, something has
genuinely changed in the source.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — one page, three services, and the
   three-line version that costs 210ms and loses work in an outage
2. Run `./gradlew run` and read all five acts in order. In acts one and two, read the
   **left-hand column** — the timestamps are the argument.
3. [`api-composition-pattern-explained.md`](api-composition-pattern-explained.md) —
   the sandwich from three shops, and the half that is harder than the parallelism
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, then the five acts as sequences
5. [`animation.html`](animation.html) — the calls leaving, the branch that fails, and
   the page with a named hole in it, one step at a time
6. The tests, which are the specification: `OrderDetailsComposerTest` first, then
   `AvailabilityTest` — which is where the argument stops being about milliseconds

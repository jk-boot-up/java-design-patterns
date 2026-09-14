# Prerequisites

What you need before starting this project, what you can pick up as you go, and what
you explicitly do not need to know.

There is no message broker here and no database. The bar is Java, and a rough sense of
what it means to cache something.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, records, sealed interfaces, `List`, `Map`, lambdas.
- **What a cache is.** A copy kept for speed, with an expiry. You need to believe that
  it is a copy, because the difference between a cache and a read model is the point of
  the whole project.
- **The idea of an event.** A record of something that happened, published by whoever
  it happened to. No broker knowledge required.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`, `assertTrue`.

### Helpful, but explained as we go

- **API Composition** ([`../api-composition-pattern`](../api-composition-pattern)) —
  this project opens with exactly that pattern, done correctly, and then argues that
  doing it on every single view is the problem. Reading it first makes act one land
  harder.
- **Database per Service**
  ([`../database-per-service-pattern`](../database-per-service-pattern)) — why the page
  needs composing at all.
- **Eventual consistency.** The primer below is enough, and act three shows it rather
  than defining it.

### Explicitly NOT required

- **Event Sourcing.** CQRS and Event Sourcing are constantly taught as one thing. They
  are not. This project uses events to update a projection; it does not store events as
  the system of record. You can use either without the other.
- **Kafka, RabbitMQ, or any broker.** `EventBus` is about forty lines and delivers to
  subscribers in memory.
- **Any database.** No JDBC, no ORM, no schema, no container.
- **Axon, Spring Modulith, or any CQRS framework.** The lesson is not in the plumbing,
  and a framework would hide the parts worth seeing.
- **Distributed transactions or the Saga pattern.** Later projects in the category.

## A 60-Second CQRS Primer

Commands change things. Queries read things. CQRS says: stop making them the same code
path, and stop making the read side re-derive an answer the write side already knew.

The write side does its work and announces what it did. Something listens and keeps a
prepared answer. Reads hit the prepared answer.

In this project: `OrderWriteService` places an order and publishes `OrderPlaced`;
`OrderHistoryReadModel` hears it, does the composition **once**, and keeps the finished
rows; `historyFor` then costs five milliseconds and calls nobody.

## A 60-Second "Read Model Versus Cache" Primer

This is the distinction the project exists to make, and it is not about speed. Both are
fast.

A **cache** is a copy that cannot know it is wrong. It stored bytes, it does not
understand them, and nothing can tell it that the world moved on. Its only correction is
an expiry. `CachedOrderHistory` is a real, working cache, and
`itIsCorrectedByATimerAndNothingElse` is the whole story.

A **read model** is a copy that is told. The same event that makes it wrong corrects it,
and it is corrected immediately rather than on a schedule.

There is no expiry setting that turns the first into the second — which is what
`thereIsNoFreeSetting` asserts. Short expiry, and you threw away the savings. Long
expiry, and you are confidently wrong for longer.

## A 60-Second "Eventual Consistency" Primer

A copy updated by a message is behind for as long as the message is in flight.

Act three shows that at its most alarming: an order that is placed, paid for and final,
and a customer looking at an order history page with nothing on it. Nothing is broken.
The events have not arrived yet.

Two properties make this liveable, and you need both. The window is short. And it closes
**by itself** — no operator, no retry button, no cleanup job.

What is not optional is deciding, page by page, whether that window is acceptable. An
order history page, yes. The screen a warehouse worker packs boxes from, no.

## The One Rule

> **Show a read model's number. Never decide anything with it.**

Act five is this rule with a price tag. The read model says one kettle is available, the
ledger says zero, a second shopper tries to buy it — and the shop is saved because the
sale is decided on the write side, against the ledger, which refuses.

`theWriteSideIsWhereASaleIsDecided` is the test. It is the one to quote when somebody
proposes checking a balance, a stock level or an entitlement against a projection in
order to allow something.

## Why There Is No Broker Or Database Here

A broker would add a container, a topic, serialisation, and several minutes to every
run — and it would teach nothing this project is about.

The subject is **which copy is allowed to decide, and how each copy learns it is
wrong.** `EventBus` delivers in memory, and `holdEvents()` lets act three make delivery
time visible instead of describing it.

`SimulatedClock` does the same for time: thirty milliseconds for an Orders call, sixty
for Catalog, five for a read-model lookup. Nothing sleeps, so every timing is exact,
repeatable, and free.

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

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the installer, and
let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/cqrs-pattern
./gradlew test         # expect BUILD SUCCESSFUL
./gradlew run          # expect five acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network connection.
Everything after that works offline.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**Act 3 shows zero rows and the build still succeeds** — correct, and it is the most
important frame in the demo. The order is real; the events have not been delivered yet.

**Act 5 shows a stock number that is wrong and nothing crashes** — deliberate. The read
model is allowed to be wrong about stock, because nothing is decided by it. The ledger
refuses the sale.

**The cache in act 4 looks broken** — it is working exactly as caches work. It was never
told about the rename, and there is no mechanism by which it could have been.

**The timings are always 30, 60 and 5ms** — they are meant to be. `SimulatedClock` is not
a real clock; those are stated assumptions, not measurements.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why composing on every view is
   correct and still wrong, and why a cache is not the answer
2. `ComposingOrderHistory.java` — read it **generously**. It is done properly, the
   catalog call is batched, and it is the thing being replaced
3. `CachedOrderHistoryTest.java` — five tests that are the argument of the project,
   especially `aRenameCannotInvalidateIt` and `thereIsNoFreeSetting`
4. Run `./gradlew run` and read all five acts, comparing act one's call count against
   act two's
5. [`cqrs-pattern-explained.md`](cqrs-pattern-explained.md) — the departures board, and
   what the split does and does not buy
6. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, including the arrow that is missing on purpose, then the five acts as
   sequences
7. [`animation.html`](animation.html) — the two copies drifting apart, and only one of
   them finding out
8. `CqrsTest.java`, which is the specification. Read `theStalenessWindowIsReal` first,
   then `theWriteSideIsWhereASaleIsDecided`, which is the rule, and `itRebuilds`, which
   is the consolation

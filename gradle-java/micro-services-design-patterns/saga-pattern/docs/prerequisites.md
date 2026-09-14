# Prerequisites

What you need before starting this project, what you can pick up as you go, and what you
explicitly do not need to know.

There is no message broker here, no database, and no distributed transaction coordinator.
The bar is Java, and having once written four service calls in a row inside a `try` block.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, records, enums, `List`, lambdas, exceptions.
- **What a database transaction does.** All of it commits or none of it does. You need to
  believe in that guarantee, because the whole project is about what happens when you
  cannot have it.
- **What a service call is.** A method call that goes over a network, takes time, and can
  fail on its own.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`, `assertTrue`.

### Helpful, but explained as we go

- **The Command pattern**
  ([`../../behavioural/command-pattern`](../../behavioural/command-pattern)) — `SagaStep`
  is `execute` and `undo` with different names, and reading Command first makes the shape
  of the interface obvious.
- **Database per Service**
  ([`../database-per-service-pattern`](../database-per-service-pattern)) — why there is no
  single database to put a transaction on in the first place.
- **Idempotency.** Retrying a compensation matters in real systems; the project after this
  one covers it properly.

### Explicitly NOT required

- **Two-phase commit or XA transactions.** They are discussed in one paragraph and then
  set aside, and you do not need to have used one.
- **Kafka, RabbitMQ, or any broker.** The orchestrator calls services directly.
- **Any database.** The five services are maps.
- **Axon, Temporal, Camunda, or any workflow engine.** They implement this pattern, and
  they would hide the twenty lines worth seeing.
- **Spring.** `@Transactional` appears only as a comment, in the class that is wrong.

## A 60-Second Saga Primer

You need five things to happen across five services, and you cannot hold a transaction open
across all of them.

So you let each step commit on its own, immediately — and you write, for each step, the
action that cancels it out. Reserve stock, release stock. Take the money, refund it. Create
the order, cancel it.

Run the steps forward, keeping a list of the ones that succeeded. If one fails, stop, and
walk that list backwards calling the cancel actions. That is the entire pattern, and it is
about twenty lines in `SagaOrchestrator.run`.

## A 60-Second "Why Not @Transactional" Primer

This is the misconception the project exists to remove, so it is worth being blunt.

`@Transactional` wraps a method in a transaction **on the database that service owns**. It
does not reach into another service's database. It does not reach across the card network.
When the shipping call fails and the transaction rolls back, the rollback covers whatever
this service wrote — and the money, which went to a payment provider through an HTTP call,
is still gone.

A distributed transaction across all five services does exist as a technology. Nobody uses
it for this, because it requires every participant to hold a lock open while waiting for
the others, and one slow courier API then holds a lock on the stock table. Under load the
shop stops.

## A 60-Second "Compensation Is Not Rollback" Primer

A rollback leaves no trace. The database behaves as though the write never happened.

A compensation is a **new action that cancels out an old one**. After a compensated saga in
this project, the payment ledger has two lines — a charge and a refund — not zero. The net
is zero and the history is not. The customer saw the money leave and come back, and in a
real shop the card network may keep its fee.

Anybody who describes a saga as "rollback for microservices" has skipped the part that
makes it hard.

## The Three Outcomes

Most explanations of this pattern have two: it worked, or it was undone. This project has
three, and the third is the one worth the hour.

- `COMPLETED` — every step ran.
- `COMPENSATED` — a step failed and every earlier step was successfully undone.
- `NEEDS_HUMAN_HELP` — a step failed, and then a compensation failed too.

The third names a state no code here can fix: the money was taken and the refund was
refused. In a real shop it is a row in a queue that a person works through. Not having one
does not make the situation go away — it only means nobody finds out.

## Why There Is No Broker Or Database Here

The subject is **what you do when you cannot roll back**, and that question is unchanged by
the transport.

The five services are maps with a simulated latency, and `SimulatedClock` advances by fixed
amounts: thirty milliseconds for Stock, a hundred for Payments, twenty for Orders, sixty for
Shipping, forty for Email. Nothing sleeps, so the timeline in the demo is exact and
repeatable, and the reverse order of the compensations is something you can see rather than
something you are told.

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
cd micro-services-design-patterns/saga-pattern
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

**"Unsupported class file major version"** — Gradle is using an older JDK than the toolchain
asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**Act 3 ends with money the shop should not have, and the build still succeeds** — correct,
and it is the most important outcome in the project. The saga reported it rather than hiding
it. In production that is a row in a queue.

**Act 4 leaves an email in the inbox and nothing throws** — deliberate. There is no
compensation for a sent email, so the step is marked as uncompensatable and the saga says so.

**Act 5 returns null and nothing fails** — that is the point of act 5. Every test in
`NaiveCheckoutServiceTest` passes while asserting that the shop is broken.

**The timings are always 30, 100, 20, 60 and 40ms** — they are meant to be. `SimulatedClock`
is not a real clock; those are stated assumptions, not measurements.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the customer who paid for a parcel that
   will never be sent
2. `NaiveCheckoutService.java` — four calls in a `try` block, and the comment where
   `@Transactional` would go
3. `NaiveCheckoutServiceTest.java` — four passing tests that assert the shop is broken
4. `SagaStep.java` and `SagaOrchestrator.java` — the whole mechanism, and it is short
5. Run `./gradlew run` and read all five acts, watching the compensations come back in
   reverse order
6. [`saga-pattern-explained.md`](saga-pattern-explained.md) — the holiday booking, and what
   the pattern costs
7. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, then the five acts as sequences
8. [`animation.html`](animation.html) — the steps committing one at a time, and then
   unwinding
9. `SagaTest.java`, which is the specification. Read `aRefundIsANewFactNotAnErasure`,
   then `aFailedCompensationNeedsAHuman`, then `theEmailGoesLast`

# Prerequisites

What you need before starting this project, what you can pick up as you go, and what you
explicitly do not need to know.

There is no real message broker here and no real database. The bar is Java, and having once
written a method that handles a message.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, records, `Map`, `Set`, lambdas, exceptions.
- **What a database transaction does.** All of it commits or none of it does. That single
  guarantee is the entire pattern.
- **Roughly what a message broker is.** Something publishes a message and something else
  receives it later. That is enough.
- **Reading a JUnit test** — `assertEquals`, `assertTrue`, `assertFalse`.

### Helpful, but explained as we go

- **Transactional Outbox**
  ([`../transactional-outbox-pattern`](../transactional-outbox-pattern)) — where the
  duplicate comes from, and why the sending side cannot remove it.
- **Saga** ([`../saga-pattern`](../saga-pattern)) — why services send each other messages at
  all.
- **Database per Service**
  ([`../database-per-service-pattern`](../database-per-service-pattern)) — why the dedupe
  store belongs to the consumer and nobody else reads it.

### Explicitly NOT required

- **Kafka, RabbitMQ, or any broker.** `MessageBroker` is a class with a `deliverTwice`
  method, which is the only behaviour this project needs from a broker.
- **Any database.** `NotificationsDatabase` is a couple of collections with a small
  transaction class in front of them.
- **Spring, `@Transactional`, or JPA.** Not used and not needed.
- **Any exactly-once framework.** The point of the project is that you do not need one.

## A 60-Second Idempotency Primer

An operation is **idempotent** if doing it twice has the same effect as doing it once.

Setting a shipment's status to `SHIPPED` is idempotent — do it again and the status is still
`SHIPPED`. Adding seventy loyalty points is not — do it again and the customer has a hundred
and forty.

A consumer is idempotent when handling the same message twice leaves the system in the state
it would have been in if the message had arrived once. Sometimes that is free, because the
work itself is idempotent. When it is not free, you buy it by remembering which message ids
you have already handled.

## A 60-Second "Why Duplicates Happen" Primer

A broker delivers a message and waits for an acknowledgement. If that acknowledgement does
not come back — a network blip, a timeout, a restart — the broker cannot tell whether the
message was handled or lost. It has two options: send it again, or drop it.

Real brokers send it again, because sending twice is recoverable and losing a message is
not. That is **at-least-once delivery**, and it is what almost everything in production
offers.

So duplicates are not a bug somebody will eventually fix. They are the contract. The
receiving side is the only place that can do anything about them.

## A 60-Second "Why A HashSet Is Not Enough" Primer

The obvious fix is a set of message ids you have already seen, held in a field.

It fails in two ways. A deploy restarts the process and the set is empty, and a restart is
frequently *why* the acknowledgement went missing in the first place — so the redelivery and
the empty memory arrive together. And even with no restart, doing the work and then adding
the id are two separate moments, and a crash can land between them.

Both failures have the same shape: the memory of having handled the message is not in the
same place, or the same instant, as the work.

## Why There Is No Broker Or Database Here

The subject is **one transaction on the receiving side**, and that is identical whether the
broker is Kafka or a method call.

A real broker would add a container, a topic and several minutes to every run, and it would
make the interesting failures — a process dying at an exact instant — far harder to produce
on demand. Here, `dieAfterQueueing()` and `dieBeforeCommitting()` put a crash exactly where
it is needed, every single run.

`SimulatedClock` advances by fixed amounts: ten milliseconds for a delivery, five for a
database commit. Nothing sleeps, so the timelines in the demo are exact and repeatable.

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

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the installer, and let
it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/idempotent-consumer-pattern
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

**Acts 2 and 3 send two confirmation emails and the build still succeeds** — correct. Those
acts exist to show the duplicate, and `theMemoryLivesInTheProcess` and `theGapIsTheProblem`
are passing tests asserting it.

**Act 5 shows a duplicate getting through after the expiry window and nothing fails** — also
correct, and it is the most important cost in the project. `theWindowIsAGuess` asserts it on
purpose.

**The timings are always 10ms and 5ms** — they are meant to be. `SimulatedClock` is not a
real clock; those are stated assumptions, not measurements.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the same email, twice, and the test that
   said it could not happen
2. `NaiveNotificationConsumer.java` — a `HashSet` of ids, which is what everybody writes
3. `NaiveNotificationConsumerTest.java` — four passing tests, two of which describe a failure
4. `IdempotentNotificationConsumer.java` — the same job, with the record in the commit
5. `NotificationsDatabase.Transaction` — the only guarantee the pattern relies on
6. Run `./gradlew run` and read all five acts, especially the last one
7. [`idempotent-consumer-pattern-explained.md`](idempotent-consumer-pattern-explained.md) —
   the ticket stub, and what the store costs
8. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the four
   consumers, then the five acts as sequences
9. [`animation.html`](animation.html) — the duplicate arriving, in a browser
10. `IdempotentConsumerTest.java`, which is the specification. Read `bothOrNeither`, then
    `exactlyOnceOutOfAtLeastOnce`, then `theWindowIsAGuess`, then the two loyalty-points
    tests together

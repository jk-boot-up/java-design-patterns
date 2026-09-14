# Prerequisites

What you need before starting this project, what you can pick up as you go, and what you
explicitly do not need to know.

There is no real message broker here and no real database. The bar is Java, and having once
written a database save followed by a call to something else.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, records, `List`, lambdas, exceptions.
- **What a database transaction does.** All of it commits or none of it does. The whole
  pattern is a trick for getting something into that guarantee that does not naturally
  belong there.
- **Roughly what a message broker is.** Something publishes a message, something else
  receives it later. That is enough.
- **Reading a JUnit test** — `assertEquals`, `assertTrue`, `assertThrows`.

### Helpful, but explained as we go

- **Saga** ([`../saga-pattern`](../saga-pattern)) — why services announce things to each
  other at all, and what happens when one of those announcements goes missing.
- **Database per Service**
  ([`../database-per-service-pattern`](../database-per-service-pattern)) — why the message
  and the data are in the same database and the receiver's data is not.
- **Idempotent Consumer**
  ([`../idempotent-consumer-pattern`](../idempotent-consumer-pattern)) — the duplicate this
  pattern creates is fixed there, and nowhere else.

### Explicitly NOT required

- **Kafka, RabbitMQ, or any broker.** `MessageBroker` is an in-memory class with a fixed
  latency and a failure switch.
- **Any database.** `OrderDatabase` is a couple of maps with a transaction class in front
  of them.
- **Debezium, change data capture, or replication log tailing.** They are one way to build
  the relay, mentioned in a paragraph, and they change the latency rather than the
  guarantee.
- **Spring, `@Transactional`, or JTA.** Not used and not needed.

## A 60-Second Outbox Primer

You need two things to happen together: the order is saved, and everybody else is told. One
is a database write and one is a message send, and there is no transaction that spans both.

So do not try. Write the message **into the database**, as an ordinary row, in the same
transaction as the order. Now it is one commit, and one commit either happens or does not.

Then a separate process — the relay — reads the unsent rows, publishes each one, and marks
each one sent. That is the whole pattern.

## A 60-Second "Why Not Just Publish" Primer

The obvious code is two lines: save, then publish. Between those two lines is a gap, and a
process can die in it. A deploy landing mid-request will do it.

When that happens the order exists and the message does not — and, crucially, **nothing
anywhere knows a message was owed**. There is no failed send to retry. There is no error. The
message did not fail; it stopped existing.

Reversing the lines does not close the gap; it just changes which lie you tell. Wrapping
them in a transaction does not work either: a database transaction has no authority over a
broker, and a broker will not join yours.

## A 60-Second "At-Least-Once" Primer

The relay publishes a message and then marks it sent. Those are two systems again, so there
is a gap again.

The pattern chooses which way that gap falls. Mark sent first, and a crash between them
loses the message. Publish first, and a crash between them sends it twice. **This pattern
publishes first**, so the failure mode is a duplicate rather than a loss.

That is at-least-once delivery, and you should say it out loud when you adopt this pattern:
never lost, sometimes twice. Anybody who tells you their outbox gives exactly-once has not
looked at the gap.

## Why There Is No Broker Or Database Here

The subject is **the gap between two systems**, and that gap is identical whether the broker
is Kafka or a `List`.

A real broker would add a container, a topic, and several minutes to every run, and it would
make the interesting failures — the process dying at an exact instant — much harder to
produce on demand. Here, `dieBetweenTheTwoLines()` and `dieAfterPublishing()` put a crash
exactly where it is needed, every single run.

`SimulatedClock` advances by fixed amounts: fifteen milliseconds for a broker publish, seven
for a notification. Nothing sleeps, so the timelines in the demo are exact and repeatable.

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
cd micro-services-design-patterns/transactional-outbox-pattern
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

**Act 2 loses an order and the build still succeeds** — correct. That act exists to show the
loss, and `theEventIsLostForever` is a passing test asserting it.

**Act 5 puts the same email in the inbox twice and nothing fails** — also correct, and it is
the most important outcome in the project. At-least-once is the guarantee, not a bug.

**The timings are always 15ms and 7ms** — they are meant to be. `SimulatedClock` is not a
real clock; those are stated assumptions, not measurements.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the order that is real and that nobody
   will ever be told about
2. `NaiveOrderService.java` — two lines, and the gap between them
3. `NaiveOrderServiceTest.java` — four passing tests describing a shop that loses orders
4. `OrderService.java` and `OrderDatabase.Transaction` — two rows, one commit, and no
   reference to the broker at all
5. `OutboxRelay.java` — read, publish, mark sent, and notice there is no retry logic
6. Run `./gradlew run` and read all five acts, especially the last one
7. [`transactional-outbox-pattern-explained.md`](transactional-outbox-pattern-explained.md)
   — the out-tray, and what the guarantee costs
8. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, then the five acts as sequences
9. [`animation.html`](animation.html) — the gap opening and closing in a browser
10. `TransactionalOutboxTest.java`, which is the specification. Read `bothOrNeither`, then
    `nothingIsLostWhenTheBrokerIsDown`, then `deliveryIsAtLeastOnce`

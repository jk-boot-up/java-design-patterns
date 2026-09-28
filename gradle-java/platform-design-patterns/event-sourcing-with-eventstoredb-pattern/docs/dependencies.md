# Dependencies

This project uses KurrentDB, its Java client and Testcontainers, which the plain-Java twin does not. This page says what they are, why they are here and what they cost. It comes before the first line of KurrentDB code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Event Sourcing project in this course teaches all of it, with nothing installed.

## What KurrentDB is

KurrentDB, called EventStoreDB until its vendor renamed it, is a database built for one job: keeping events in order and never changing them.

Think of a set of paper ledgers with numbered lines, one ledger per customer. You may only write on the next empty line, and you never rub anything out. Before you write, you may say "I last read line 3", and the clerk refuses your entry if somebody has written line 4 since.

In KurrentDB's words:

- Each ledger is a **stream**, here `loyalty-C-4417`.
- Each line's number is its **revision**, starting at 0.
- Writing on the next line is an **append**.
- "I last read line 3" is the **expected revision**, which the Java client calls a `StreamState`. The refusal is a **WrongExpectedVersion** error. `StreamState.any()` means "don't check".
- Every event also carries an **event id**, a random identifier the writer picks, which the server uses to recognise a retry.
- The server also keeps one log of every event in every stream, in the order it wrote them, called **`$all`**.
- A reader that asks for everything from the start, then for each new event as it arrives, holds a **catch-up subscription**. A copy of the data it builds for one screen is a **projection**, or **read model**.
- Deleting a stream normally is a **soft delete**: the stream is hidden and its name can be used again. A **tombstone** is a hard delete that forbids the name for ever. Neither removes the bytes until a clean-up called a **scavenge** runs.

## What the KurrentDB Java client is

`io.kurrent:kurrentdb-client` is the official Java library. It talks to the server over gRPC on port 2113. Its main class is `KurrentDBClient`, with `appendToStream`, `readStream`, `readAll`, `subscribeToAll` and `deleteStream`. Every call returns a `CompletableFuture`, and this project waits on each one with `get()` to keep the code in order.

It replaces `com.eventstore:db-client-java`, whose last release was 5.4.5. It is much larger than the libraries in most projects in this course: it brings gRPC, Netty, Protocol Buffers, Jackson, Bouncy Castle and OpenTelemetry with it.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so the demo owns KurrentDB's lifetime: `./gradlew run` brings the server up, uses it and takes it away at the end. It maps port 2113 to a free random port on your machine, and it waits until `/health/live` answers before the demo carries on. There is no KurrentDB module in Testcontainers, so the plain container type is used.

## Why this project uses them

The things this project teaches cannot happen when the event store is a list inside one program:

- two writers racing for the same points, and the check that stops the second one
- a retry after a lost reply
- a reader that starts late and catches up
- a delete that hides rather than erases

The store has to be its own process, reached over a network, by more than one client. That is what KurrentDB is.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| KurrentDB server image | `kurrentplatform/kurrentdb:26.1.2` (ARM: `26.1.2-experimental-arm64-10.0-noble`) |
| `io.kurrent:kurrentdb-client` | 1.2.1 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release. None is held back.

## What it costs

The first run pulls the KurrentDB image, about 590 MB unpacked. KurrentDB publishes no Alpine image. The server uses about 160 MB of memory while it runs. After the first run, a run takes about five seconds, most of it the container starting.

Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through. It exits on its own a few seconds after the demo does.

The server runs insecure: no TLS and no passwords. That is fine on your own machine for one run, and never acceptable in production.

## Where this pattern lives in a real system

- In the command handler that reads a stream, decides and appends with the revision it read.
- In the retry loop around it, which must look again and decide again rather than resend blindly.
- In the event id chosen once per decision.
- In each projection's subscription and its checkpoint.
- In the scavenge schedule, and the erasure procedure that has to reach every projection as well as the stream.

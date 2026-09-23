# Dependencies

This project uses NATS, Testcontainers and a container runtime, which the hand-built projects do not. This page says what they are, why they are here, and what they cost. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Event Bus](../../event-bus-pattern) teaches all of it with plain Java and nothing installed.

## What NATS is

NATS is a message bus that runs as a program of its own. A service **publishes** an event under a name, and returns straight away. Another service **subscribes** to a name, and from that moment the server sends it every event published under that name. The name is called a *subject*. It is written in dotted parts, like `store.orders.placed`, so that a subscriber can ask for a family of them: a star matches one part, and an arrow matches the rest.

The thing to hold on to is what NATS does **not** do. It stores nothing. It remembers nobody. An event is handed to whoever is listening at that instant, and then it is gone. That is called at-most-once delivery, and it is a choice, not a limitation.

## Why this project uses it

A real server makes the miss real. In one program you can always arrange for the subscriber to exist first. Across a network you cannot, and the event that falls in the gap is the lesson.

NATS was chosen rather than Kafka on purpose. [Event-Driven Architecture with Kafka](../../../architectural-design-patterns/event-driven-architecture-with-kafka-pattern) already teaches the durable-log shape, where nothing is lost and readers catch up. NATS is the opposite trade, and the two side by side are worth more than a second Kafka project.

## What Testcontainers is

Testcontainers is a library that starts a container from Java and stops it again. It is here so that the demo owns its own server: you run `./gradlew run` and everything it needs appears and then disappears. Nothing is left behind, and nothing has to be installed and configured first.

## What to install

Only a JDK, version 21, and a container runtime that is running. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker Desktop, Colima or equivalent | running; 24 or later |
| NATS server image | `nats:2.15.0-alpine` |
| `io.nats:jnats` | 2.26.3 |
| `org.testcontainers:testcontainers` | 2.0.5 |

These are the newest generally available releases at the time this project was built. Nothing is held back.

The demo starts one container, opens the client port that services connect to and a second port that the server answers questions about itself on, and removes the container at the end.

## What it costs

The first run pulls the image, about ten megabytes, which is small as brokers go. The demo takes a few seconds once the image is on disk. The server uses a few tens of megabytes of memory while it runs.

The real cost is not the megabytes. It is that the bus is now a program that has to be run, watched, upgraded and kept up, and that it will drop an event the moment nobody is listening for it.

## Where this pattern lives

In the server's configuration, in the subject names a team agrees on, and in each service's client library.

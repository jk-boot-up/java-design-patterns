# Prerequisites

## Required

- [Splitter and Aggregator](../../splitter-aggregator-pattern), the hand-built partner project. Read it first. This one assumes the idea and spends its time on what the framework makes you deal with.
- The idea of a correlation identifier: something shared by messages that belong together.

## Helpful but not required

- Message Channel and Content-Based Router, earlier in this category.
- Any previous contact with Apache Camel. If you have none, [`dependencies.md`](dependencies.md) says every word this project uses before it uses it.

## Explicitly not required

- **No container runtime.** Camel is a library and runs inside the demo's own process. There is no broker, no database and no network call in this project.
- No Spring, and no application server.

## What you will need

Java 21 and the Gradle wrapper in this directory. The first build downloads the Apache Camel 4.20.0 jars, about twelve megabytes; after that `./gradlew run` and `./gradlew test` work offline.

The whole demo finishes in about a second. Most of that second is the aggregator's own six-hundred-millisecond deadline in the fifth act, which is the point of the project.

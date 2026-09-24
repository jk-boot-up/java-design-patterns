# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later, with about 1 GB of memory to spare. The demo starts a Kafka container and a Postgres container and stops both again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need the containers are skipped and the rest still run.
- The idea of an idempotent consumer: a receiver that remembers which messages it has handled, so a repeat has no effect. The plain-Java Idempotent Consumer project in this course teaches it with nothing installed. This project explains the idea again in its own words, but does not dwell on it.

## Explicitly not required

- No prior Kafka. Every word it introduces — topic, offset, consumer group, committing an offset, the patience limit Kafka calls `max.poll.interval.ms`, retention, replay — is said in plain language before the name for it is used.
- No prior Postgres beyond "a database with tables". Transaction, primary key, lock and `on conflict do nothing` are each explained where they are used.
- No installed Kafka or Postgres, and no configuration on your machine. Both live in containers for the length of the run, on ports picked at random.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls both images; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| Kafka broker image | `apache/kafka:4.3.1` |
| Postgres image | `postgres:18.6-alpine` |
| `org.apache.kafka:kafka-clients` | 4.3.1 |
| `org.postgresql:postgresql` | 42.7.13 |
| `org.testcontainers:testcontainers-kafka` | 2.0.5 |
| `org.testcontainers:testcontainers-postgresql` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back.

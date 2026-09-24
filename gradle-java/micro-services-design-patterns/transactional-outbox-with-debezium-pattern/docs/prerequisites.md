# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later, with about 1 GB of memory to spare. The demo starts a Postgres container and a Kafka container and stops both again. Debezium needs no container: it runs inside the demo's own Java program. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need the containers are skipped and the rest still run.
- The idea of a transactional outbox: write the message as a row beside the record, in the same transaction, and let something else send it later. The plain-Java Transactional Outbox project in this course teaches it with nothing installed. This project explains the idea again in its own words, but does not dwell on it.

## Explicitly not required

- No prior Debezium or change data capture. Every word they bring — write-ahead log, logical decoding, replication slot, offset, outbox event router — is said in plain language before the name for it is used.
- No prior Kafka. Topic, partition, key and offset are each explained where they first matter.
- No prior Postgres beyond "a database with tables". Transaction, commit and rollback are explained where they are used.
- No installed Postgres, Kafka or Debezium, and no configuration on your machine. Both containers live for the length of the run, on ports picked at random.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls both images; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| Postgres image | `postgres:18.6-alpine`, started with `wal_level=logical` |
| Kafka broker image | `apache/kafka:4.3.1` |
| `io.debezium:debezium-embedded` | 3.6.3.Final |
| `io.debezium:debezium-connector-postgres` | 3.6.3.Final |
| `org.apache.kafka:kafka-clients` | 4.3.1 |
| `org.postgresql:postgresql` | 42.7.13 |
| `org.testcontainers:testcontainers-postgresql` | 2.0.5 |
| `org.testcontainers:testcontainers-kafka` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back. Debezium 3.7 was a release candidate at the time, not a general release, so the 3.6 line is used.

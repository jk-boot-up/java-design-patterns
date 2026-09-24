# Dependencies

This project uses Postgres, Debezium, Kafka and Testcontainers, which the plain-Java version does not. This page says what they are, why they are here, and what they cost. It comes before the first line of connector code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Transactional Outbox project in this course teaches all of it, with nothing installed.

## What Postgres's log is

Postgres is a relational database: tables of rows, and a guarantee about groups of changes. A **transaction** is a group of changes kept together or thrown away together. Nothing in it is visible to anyone until it is **committed**; a **rollback** throws it all away.

Before Postgres changes any table, it writes the change to a log on disk, so that after a crash it can replay the log and lose nothing. That is the **write-ahead log**, or **WAL**. Normally only Postgres reads it. Started with **`wal_level=logical`**, Postgres writes enough into it for an outside program to read the changes back as rows: this row was inserted into this table, in a transaction that committed. Turning that into rows is **logical decoding**, and `pgoutput` is the decoder built into Postgres that does it. The setting can only change when Postgres starts, which is why the demo starts its Postgres with it.

A reader of the log connects through a **replication slot**: a named bookmark Postgres keeps for that one reader. Postgres will not throw away any part of the log the slot's reader has not confirmed. That is what makes change data capture safe, and what makes a forgotten slot dangerous. The setting `max_slot_wal_keep_size` can put a ceiling on it; its default is -1, no ceiling.

## What Debezium is

Debezium is change data capture: a program that connects to a database's log through a replication slot and turns every committed change into a message. Its **Postgres connector** does the reading. Its **outbox event router** is a small step that turns each new outbox row into one clean event: the row's `aggregateid`, here the order id, becomes the message key; the `payload` becomes the message body; the row's `id` and `type` become headers; and the topic is chosen for it, here `order-events`. Debezium writes down how far it has read, its **offset**, which for Postgres is a position in the log, and tells Postgres the same through the slot.

Debezium can run in three ways: inside Kafka Connect, as the standalone Debezium Server, or as a library inside a Java program, which Debezium calls the **embedded engine**. This project uses the embedded engine, so no third container is needed. It keeps its offset in a small file that the demo deletes at the end.

## What Kafka is

Kafka is a message log: a separate program that keeps messages in the order they were written and lets any number of readers read them. A **topic** is one such log. It is split into **partitions**, separate lists that can be read side by side; `order-events` has three. A message's **key** decides its partition, so every message with the same key lands in the same one, and order is kept within a partition, never across them. Each message sits at a numbered place in its partition, its **offset**.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so the demo owns both tools' lifetimes: `./gradlew run` brings Postgres and Kafka up, uses them, and takes them away at the end. It maps each tool's port — 5432 for Postgres, 9092 for Kafka — to a free port on your machine picked at random.

## Why this project uses them

Because the things this project teaches only happen when there is a real database log: a row deleted in its own transaction that is still sent, a rolled-back transaction that never appears, a slot that keeps the log while its reader is away, and a reader that is handed the same changes again after dying between sending and writing down its place. A map and a list inside one Java program have no log, so they cannot show any of that.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| Postgres image | `postgres:18.6-alpine` |
| Kafka broker image | `apache/kafka:4.3.1` |
| `io.debezium:debezium-embedded` | 3.6.3.Final |
| `io.debezium:debezium-connector-postgres` | 3.6.3.Final |
| `org.apache.kafka:kafka-clients` | 4.3.1 |
| `org.postgresql:postgresql` | 42.7.13 |
| `org.testcontainers:testcontainers-postgresql` | 2.0.5 |
| `org.testcontainers:testcontainers-kafka` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. Debezium 3.6.3 is built against Kafka 4.3.0, and Gradle settles the Kafka libraries on 4.3.1, matching the broker. Postgres uses its Alpine build because it is smaller; Kafka has no Alpine build, so the Apache project's one image is used, in KRaft mode on a single node with its memory held to 256 MB.

## What it costs

The first run pulls two images, Postgres at about 298 MB and Kafka at about 446 MB once unpacked, and downloads Debezium's libraries. After that a run takes about fifteen seconds. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

In production the bill is larger than the containers. Postgres has to run with `wal_level=logical`, which means a restart to switch on and a little more log written. Somebody has to watch the slot, because a slot that stops moving makes the database keep its log until the disk fills. And every reader of the topic has to cope with an event arriving twice.

## Where this pattern lives in a real system

In one `outbox` table with the columns Debezium's router expects, in the insert beside every business write, in a connector configuration with `table.include.list` naming that table and a `transforms` line naming the outbox event router, in an alert on the slot's lag, and in an idempotent reader at the other end.

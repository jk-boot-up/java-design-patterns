# Dependencies

This project uses Kafka, Postgres and Testcontainers, which the plain-Java version does not. This page says what they are, why they are here, and what they cost. It comes before the first line of broker code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Idempotent Consumer project in this course teaches all of it, with nothing installed.

## What Kafka is

Kafka is a message log: a separate program that keeps messages in the order they were written and lets any number of readers read them. Think of a shared notebook in which the till writes one line per sale, and the back office reads down it with a bookmark.

In Kafka's words, the notebook is a **topic**. Every message sits at a numbered place in it, counting from 0, and that number is its **offset**. A service that reads the topic is a **consumer group**; however many copies of the service are running, they share one group. The broker keeps each group's bookmark: the place it has reached. Asking the broker to move the bookmark is **committing the offset**, and until a copy does it, the broker assumes nothing past the old bookmark was handled. That is why delivery is **at least once**: a copy that does the work and stops before moving the bookmark leaves the same messages to be handed out again.

A copy must keep asking for more messages. If it goes too long without asking, the broker decides it is stuck and gives its share of the topic to another copy. That patience limit is **`max.poll.interval.ms`**, five minutes by default. A topic keeps its messages for a set time, its **retention**, seven days by default; an operator can move a group's bookmark back and have it read them all again, which is a **replay**.

## What Postgres is

Postgres is a relational database: tables of rows, and a guarantee about groups of changes. A **transaction** is a group of changes that are kept together or thrown away together; nothing in it is visible to anyone else until it is **committed**. A **primary key** is a column the database will not allow two rows to share. When two sessions try to write the same key at once, the second is made to wait for the first, on a **lock**, and then told whether the key is taken. `on conflict do nothing` asks Postgres to write nothing, rather than fail, when the key is already there, and to say it wrote zero rows.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so the demo owns both tools' lifetimes: `./gradlew run` brings Kafka and Postgres up, uses them, and takes them away at the end. It maps each tool's port — 9092 for Kafka, 5432 for Postgres — to a free port on your machine picked at random, so neither collides with anything already running.

## Why this project uses them

Because the things this project teaches only happen when the log and the store are separate programs from the service: a copy stopping and the log handing its messages to a different copy, two copies holding the same message at once, a transaction thrown away by the database when a connection drops, and a bookkeeping request refused by the broker. A broker and a map inside one Java program cannot show any of that.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| Kafka broker image | `apache/kafka:4.3.1` |
| Postgres image | `postgres:18.6-alpine` |
| `org.apache.kafka:kafka-clients` | 4.3.1 |
| `org.postgresql:postgresql` | 42.7.13 |
| `org.testcontainers:testcontainers-kafka` | 2.0.5 |
| `org.testcontainers:testcontainers-postgresql` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. Postgres uses its Alpine build because it is smaller; Kafka has no Alpine build, so the Apache project's one image is used. Kafka runs in KRaft mode, a single node that needs no ZooKeeper, with its memory held to 256 MB. In the Testcontainers 2 line every module's name starts with `testcontainers-`.

## What it costs

The first run pulls two images, Kafka at about 446 MB and Postgres at about 298 MB once unpacked. After that a run takes about twenty seconds. The two containers use a few hundred megabytes of memory between them while they are up. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Where this pattern lives in a real system

In one table with one primary key, in the insert at the top of the consumer's transaction, in the consumer setting that turns off Kafka's automatic bookmark and commits it by hand after the work, and in the cleanup job whose window somebody has checked against the topic's retention.

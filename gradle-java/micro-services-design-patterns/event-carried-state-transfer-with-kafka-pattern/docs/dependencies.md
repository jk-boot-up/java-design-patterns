# Dependencies

This project uses a real Kafka broker, run in a container by Testcontainers,
which the plain Java version of Event-Carried State Transfer does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What Apache Kafka is

Kafka stores events on topics, and keeps them after they are read, so anyone can read a topic from the beginning. A topic is split into partitions; events with the same key always go to the same partition, and order is kept only within a partition. A compacted topic keeps at least the latest event for each key and may discard older ones. A tombstone is an event with a key and no value; on a compacted topic it means the key is deleted.

## What Testcontainers is

Testcontainers is a Java library that starts a container, here the Kafka image, from inside a program, and removes it afterwards.

## Why this project uses them

The plain version shows the idea. This version shows how the most common
real carrier of state events, Kafka, handles history, order and deletion.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| Kafka image | apache/kafka:4.3.1 |
| Kafka Java client | 4.3.1 |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and a first run that downloads the Kafka image.
- A Kafka cluster to run in production, and keys chosen with care.

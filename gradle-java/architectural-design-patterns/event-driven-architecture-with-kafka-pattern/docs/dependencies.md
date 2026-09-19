# Dependencies

This project uses Apache Kafka, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Event-Driven Architecture](../event-driven-architecture-pattern) teaches all of it with plain Java.

## What Apache Kafka is

Apache Kafka is a distributed log. Producers append events to a topic, and consumer groups read them, each group with its own committed offset held by the broker. Lag is the difference between the end of the topic and a group's offset.

## Why this project uses it

A real broker gives real offsets and a real lag, and real redelivery, so the pattern's behaviour is its own and not a model.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| Kafka broker image | `apache/kafka:4.3.1`, in KRaft mode |
| `org.apache.kafka:kafka-clients` | 4.3.1 |

The demo runs the container as `patterns-kafka` on port 9092, and removes it at the end. Each act uses a topic of its own with one partition, so offsets are in the order of events.

## What it costs

The first run pulls the image, about 400 megabytes. The demo takes about twenty seconds. A broker uses several hundred megabytes of memory while it runs.

## Where this pattern lives

In a broker cluster, in topic and consumer group settings, and in the client libraries of each service.

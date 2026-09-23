# Dependencies

This project uses RabbitMQ and Testcontainers, which the hand-built projects do not. This page says what they are, why they are here, and what they cost. It comes before the first line of broker code on purpose.

**Skipping this project loses none of the pattern.** [Dead Letter Channel](../../dead-letter-channel-pattern) teaches all of it in plain Java, with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program that holds queues of messages for other programs. A producer hands a message to an exchange, which is the broker's sorting desk, and the desk puts a copy on every queue tied to it. A consumer takes messages off a queue one at a time and tells the broker when it is done with each one.

A queue can carry rules, written when it is declared. One of those rules names an exchange to send a message to when it dies in that queue. RabbitMQ calls it the dead-letter exchange, and it is the pattern this project teaches, built into the broker.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns the broker's lifetime: `./gradlew run` brings RabbitMQ up, uses it, and takes it away. Nothing is installed and nothing is left running.

## Why this project uses them

Because the point of the project is the line between what the application decides and what the broker decides, and you cannot draw that line without a real broker on the other side of it. The reasons `expired` and `maxlen` are not things an application can produce; they are things that happen to a message while nobody is holding it.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| RabbitMQ broker image | `rabbitmq:4.3.6-alpine` |
| `com.rabbitmq:amqp-client` | 5.36.0 |
| `org.testcontainers:testcontainers-rabbitmq` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

The alpine image is chosen over the management image because nothing here needs the web interface, and the smaller image starts faster. Each act declares queues of its own, so no act can see another act's messages.

## What it costs

The first run pulls the image, about seventy megabytes compressed. After that a run takes a few seconds beyond the broker's start-up. The broker uses a couple of hundred megabytes of memory while it is up. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through.

## Where this pattern lives in a real system

In the arguments on a queue declaration, usually in whatever sets your infrastructure up rather than in application code; in the consumer's choice between asking for a message back and refusing it for good; and on the dashboard that watches the depth of the parked queue.

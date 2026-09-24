# Dependencies

This project uses RabbitMQ and Testcontainers, which the plain-Java version does not. This page says what they are, why they are here, and what they cost. It comes before the first line of broker code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Competing Consumers project in this course teaches all of it, with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program whose whole job is to hold messages and hand them to the programs that do the work. Think of a kitchen's ticket rail, and the person who hands tickets to the cooks.

In RabbitMQ's words, the rail is a **queue**: a named place where messages wait, in the order they arrived. A program that takes messages from a queue is a **consumer**; here each consumer is a warehouse picker. When a picker has finished with an order it tells the broker, and that message is an **acknowledgement**. A picker can also tell the broker to count each order as done the moment it is handed over, which is **automatic acknowledgement**. How many orders the broker will hand one picker before hearing done for any of them is the **prefetch**; setting none means no limit. An order handed out a second time carries a **redelivered** flag, which this project calls seen before.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so the demo owns the broker's lifetime: `./gradlew run` brings RabbitMQ up, uses it, and takes it away at the end. It also maps the broker's port, 5672 inside the container, to a free port on your machine picked at random, so it never collides with anything already running.

## Why this project uses them

Because the things this project teaches only happen when the queue is in a separate program that pushes work down real network connections: a picker being handed more than it asked for, a crash cutting a connection and the broker taking back everything that picker held, and the choice of when an order counts as done. A queue inside the same program as the consumers cannot show any of that.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| RabbitMQ broker image | `rabbitmq:4.3.6-alpine` |
| `com.rabbitmq:amqp-client` | 5.36.0 |
| `org.testcontainers:testcontainers-rabbitmq` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. The Alpine build of the image is used because it is smaller. In the Testcontainers 2 line every module's name starts with `testcontainers-`.

## What it costs

The first run pulls the broker image, about 161 MB once unpacked. After that a run takes about ten seconds, most of it the broker starting. The broker uses a couple of hundred megabytes of memory while it is up. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Where this pattern lives in a real system

In one `basicQos` call before each consumer starts, in the consumer's choice of automatic or manual acknowledgement, in how many copies of the worker service are running, and on the dashboard that watches how many messages are waiting and how many are held but not yet done.

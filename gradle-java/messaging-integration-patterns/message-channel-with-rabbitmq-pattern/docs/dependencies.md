# Dependencies

This project uses RabbitMQ and Testcontainers, which the hand-built project does not. This page says what they are, why they are here, and what they cost. It comes before the first line of broker code on purpose.

**Skipping this project loses none of the pattern.** [Message Channel](../../message-channel-pattern) teaches all of it in plain Java, with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program whose whole job is to hold messages for other programs. Think of a post office. You hand in a parcel and walk away; the post office keeps it until the person it is addressed to comes to collect it, however long that takes.

In RabbitMQ's words, the parcel shelf is a **queue**: a named place where messages wait, in the order they arrived. The counter where you hand the parcel in is an **exchange**: the part of the broker that decides which queue a message goes on. This project only ever uses the default exchange, which puts a message on the queue whose name it is addressed to, so the exchange never has a decision to make here. When the receiver has finished with a message it tells the broker, and the broker forgets it; that message is an **acknowledgement**. A queue the broker writes down, so it survives a restart, is **durable**; a message the broker writes down is **persistent**. A receipt the broker sends back to say it took a message, or turned it away, is a **publisher confirm**.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns the broker's lifetime: `./gradlew run` brings RabbitMQ up, uses it, stops and starts the broker program inside it for the fifth act, and takes it away at the end. Nothing is installed and nothing is left running.

## Why this project uses them

Because the three things this project teaches — a message waiting for a receiver that does not exist yet, a message coming back when its receiver dies, and a message surviving the channel's own restart — cannot happen when the channel lives inside the same program as the sender. The channel has to be a separate process that you can restart without restarting anything else, and that is what a broker is.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| RabbitMQ broker image | `rabbitmq:4.3.6` |
| `com.rabbitmq:amqp-client` | 5.36.0 |
| `org.testcontainers:testcontainers-rabbitmq` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. In the Testcontainers 2 line every module's name starts with `testcontainers-`, which is why the artifact is not called plain `rabbitmq` as it was in 1.x.

## What it costs

The first run pulls the broker image, about 256 MB once unpacked. After that a run takes about ten seconds, most of it the broker starting, and the restart in the fifth act. The broker uses a couple of hundred megabytes of memory while it is up. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Where this pattern lives in a real system

In the queue declarations, usually in whatever sets your infrastructure up rather than in application code; in the one flag on each send that says whether the message is written down; in the consumer's choice of when to acknowledge; and on the dashboard that watches how many messages are waiting.

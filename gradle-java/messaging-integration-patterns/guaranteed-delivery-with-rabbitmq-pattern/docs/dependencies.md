# Dependencies

This project uses a real RabbitMQ broker, run in a container by
Testcontainers, which the plain Java version of Guaranteed Delivery does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program that holds messages between senders and receivers. A queue is a named line of messages. A durable queue is written to disk and survives a restart. A persistent message is written to disk too; a durable queue can still lose messages that were not persistent. Publisher confirms make the broker tell the sender when each message is safely stored. An acknowledgement is the receiver telling the broker it has finished with a message; until then, the broker keeps it, and gives it out again if the receiver disappears, marked as redelivered.

## What Testcontainers is

Testcontainers is a Java library that starts a container, here the RabbitMQ image, from inside a program, and removes it afterwards, so nothing has to be installed or started by hand.

## Why this project uses them

The plain version shows the idea with its own journal file. This version
shows the settings a real broker needs for the same guarantee, and what goes
wrong when one of them is missing.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| RabbitMQ image | rabbitmq:4.3.6 |
| RabbitMQ Java client | 5.36.0 |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and a first run that downloads the broker image.
- A broker to operate in production, with replicated queues for real safety.

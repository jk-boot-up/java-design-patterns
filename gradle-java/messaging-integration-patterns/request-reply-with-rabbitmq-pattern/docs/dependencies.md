# Dependencies

This project uses a real RabbitMQ broker, run in a container by
Testcontainers, which the plain Java version of Request-Reply does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program that holds messages. Every message can carry properties. replyTo names the queue a reply should go to. correlationId is a reference the replier copies onto its reply. expiration tells the broker to drop the message if nobody has taken it within that many milliseconds. amq.rabbitmq.reply-to is direct reply-to: a special address a client can consume from, so replies reach it without any reply queue being declared. An exclusive queue belongs to one connection and disappears with it.

## What Testcontainers is

Testcontainers is a Java library that starts a container, here the RabbitMQ image, from inside a program, and removes it afterwards.

## Why this project uses them

The plain version shows the idea. This version shows the message properties a
real broker provides for it, and the two things a real broker forces into the
open: that publishing does not wait, and that an abandoned request needs an
expiry.

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
- A waiting table and time-outs in every requester.

# Dependencies

This project uses a real RabbitMQ broker, run in a container by
Testcontainers, which the plain Java version of Priority Queue does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program that holds messages on queues. A queue declared with the argument x-max-priority becomes a priority queue; each message then carries a priority property, and higher priorities are handed out first. basicGet takes one message now. basicConsume asks the broker to push messages, and basicQos sets the prefetch: how many unacknowledged messages it may push to that consumer. Messages already pushed are no longer on the queue, so priority cannot reorder them.

## What Testcontainers is

Testcontainers is a Java library that starts a container, here the RabbitMQ image, from inside a program, and removes it afterwards.

## Why this project uses them

The plain version shows the idea. This version shows what a real broker's
priority queue does, and the two limits the plain version could not show.

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
- Prefetch and queue layout to design for priority to work.

# Dependencies

This project uses a real RabbitMQ broker, run in a container by
Testcontainers, which the plain Java version of Polling Consumer does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program that holds messages on queues. basicGet asks for one message now, and gets nothing if the queue is empty: that is polling. basicConsume asks the broker to push messages as they arrive. basicQos sets the prefetch: the most unacknowledged messages the broker will push to one receiver; zero means no limit. An acknowledgement tells the broker a message is finished; unacknowledged messages go back on the queue if the receiver disappears.

## What Testcontainers is

Testcontainers is a Java library that starts a container, here the RabbitMQ image, from inside a program, and removes it afterwards.

## Why this project uses them

The plain version shows the idea. This version shows what a real broker does
when it is allowed to push without a limit, what each poll costs, and the
limit RabbitMQ offers instead.

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
- A prefetch value to choose and tune.

# Prerequisites

## Required

- [Content-Based Router](../content-based-router-pattern), the hand-built version this project pairs with.
- **A container runtime, running.** This demo starts a real RabbitMQ broker in a container. Without a runtime the demo says so in two plain sentences and stops, and the broker tests are skipped rather than failed.

## Explicitly not required

- No prior Apache Camel. Route, endpoint, exchange and predicate are each explained in plain words before Camel's name for them is used.
- No prior RabbitMQ. Queue, exchange and routing key are explained the same way.
- No installed broker. It runs in a container the demo starts and removes; nothing is left behind.

## What you will need

Java 21, and a container runtime. Everything else is downloaded by Gradle.

| Tool | Version |
| --- | --- |
| Java | 21 |
| Gradle | 9.2.1, via the wrapper in this directory |
| Docker | 24 or later, running |
| RabbitMQ image | `rabbitmq:4.3.6-alpine` |
| Apache Camel | 4.20.0 |
| RabbitMQ Java client | 5.36.0 |
| Testcontainers | 2.0.5 |
| JUnit 5 | 5.10.2 |

The first run pulls the broker image and takes longer. After that, `./gradlew run` takes about twenty seconds.

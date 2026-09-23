# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts a RabbitMQ container and stops it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need the broker are skipped and the rest still run.
- [Dead Letter Channel](../../dead-letter-channel-pattern), the hand-built version this project pairs with. Read it first: this project does not re-teach the pattern.

## Explicitly not required

- No prior RabbitMQ. Every word it introduces — queue, exchange, dead letter exchange, refusing a message, asking for it back — is said in plain language before the name for it is used.
- No installed RabbitMQ, and no RabbitMQ configuration on your machine. The broker lives in the container for the length of the run.
- No message broker experience of any kind.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the broker image; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| RabbitMQ broker image | `rabbitmq:4.3.6-alpine` |
| `com.rabbitmq:amqp-client` | 5.36.0 |
| `org.testcontainers:testcontainers-rabbitmq` | 2.0.5 |
| Java | 21 |
| Gradle | 9.2.1 |

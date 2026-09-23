# Prerequisites

## Required

- A container runtime running on the machine: Docker Desktop, Colima, or an equivalent, version 24 or later. Without it the demo prints one sentence saying so and stops, and the tests are skipped rather than failed.
- [Event Bus](../../event-bus-pattern): the hand-built version this project pairs with. Read it first.

## Explicitly not required

- No prior NATS. Every word it uses — subject, publish, subscribe, wildcard, no responders — is explained in plain language as it appears.
- No installed NATS server: it runs in a container the demo starts and removes.
- No prior Testcontainers. It appears in one small class, and that class is six lines of setup.

## What you will need

Java 21, and a network connection the first time, to pull the image and the libraries. After that the demo runs from what is already on disk.

## Helpful, but not needed

- [Publisher-Subscriber](../../../micro-services-design-patterns/publisher-subscriber-pattern), the same idea across processes.
- [Event-Driven Architecture with Kafka](../../../architectural-design-patterns/event-driven-architecture-with-kafka-pattern), which makes the opposite trade and is worth reading beside this one.

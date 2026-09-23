# Messaging and Integration Patterns

The eleventh category. How separate systems, and separate parts of one system, exchange
messages safely. Each project is plain Java with tests, docs, diagrams, an animation, a
narrated video pipeline and a YouTube document, and each shows its bill.

**Status: five built, each with a real-infrastructure version.**

1. [Message Channel](message-channel-pattern) — a named queue between a sender and a receiver, so
   neither waits for the other.
2. [Content-Based Router](content-based-router-pattern) — reads a message and sends it where its
   content says, in one place.
3. [Splitter and Aggregator](splitter-aggregator-pattern) — breaks a message into parts that carry
   their place, and puts them back by id.
4. [Dead Letter Channel](dead-letter-channel-pattern) — where a message goes when it can never
   succeed, so it stops blocking the line.
5. [Event Bus](event-bus-pattern) — one meeting place inside a program, where components post
   events and subscribe to the kinds they care about.

They are meant to be watched in that order. Related patterns elsewhere in the repository:
[Publisher-Subscriber](../micro-services-design-patterns/publisher-subscriber-pattern),
[Competing Consumers](../micro-services-design-patterns/competing-consumers-pattern),
[Claim Check](../micro-services-design-patterns/claim-check-pattern) and
[Idempotent Consumer](../micro-services-design-patterns/idempotent-consumer-pattern).

## With real infrastructure

The hand-built projects above run in plain Java with nothing installed. These pair with them and run the same idea on the real tool: a RabbitMQ broker or a NATS server in Docker, or Apache Camel. Each one names what its simulation got right and what it left out. The tests that need Docker are skipped when it is missing.

- [Message Channel with RabbitMQ](message-channel-with-rabbitmq-pattern), with RabbitMQ in Docker
- [Content-Based Router with Camel](content-based-router-with-camel-pattern), with Apache Camel over RabbitMQ in Docker
- [Splitter and Aggregator with Camel](splitter-aggregator-with-camel-pattern), with Apache Camel, and nothing to install
- [Dead Letter Channel with RabbitMQ](dead-letter-channel-with-rabbitmq-pattern), with RabbitMQ in Docker
- [Event Bus with NATS](event-bus-with-nats-pattern), with NATS in Docker

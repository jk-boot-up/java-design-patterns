# Messaging and Integration Patterns

The eleventh category. How separate systems, and separate parts of one system, exchange
messages safely. Each project is plain Java with tests, docs, diagrams, an animation, a
narrated video pipeline and a YouTube document, and each shows its bill.

**Status: five built.**

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

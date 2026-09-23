# Dependencies

This project uses Apache Camel and a real RabbitMQ broker, which the hand-built projects do not. This page says what they are, why they are here, and what they cost. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Content-Based Router](../content-based-router-pattern) teaches all of it with plain Java and nothing installed.

## What Apache Camel is

Apache Camel is a library for moving messages between things. You write a *route*: a short description that says where messages come from, what should be asked about each one, and where each answer sends it. Camel reads that description and runs it.

Four of Camel's words are worth saying in plain language once.

- A **route** is the written description just mentioned. It is a rule, not a running loop you have to write.
- An **endpoint** is one end of a route: a queue to read from, or a queue to write to. It is written as a short piece of text, which is why you will see the destination look like an address.
- An **exchange**, in Camel's sense, is the message while it is travelling, together with anything learned about it on the way.
- A **predicate** is a yes-or-no question asked about that message. Camel's `choice` asks a list of predicates in order and takes the first branch whose question is answered yes. If none is, it takes the `otherwise` branch, and if there is no `otherwise` branch it takes none of them and the route ends.

That last sentence is the whole reason this project exists.

## What RabbitMQ is

RabbitMQ is a message broker: a separate program that holds messages for you.

- A **queue** is a named line that messages wait in until somebody takes them.
- An **exchange**, in RabbitMQ's sense — a different sense from Camel's — is the post box a sender drops a message into. It never keeps anything. It looks at the message's label and hands the message to the queue or queues that label belongs to.
- A **routing key** is that short label, written on the message when it is posted.

This demo uses one exchange, named `shop`, and ten queues. Every queue is reached by a routing key that is simply the queue's own name, so the topology stays out of the way and the route is the only thing making decisions.

## Why this project uses them

Because the interesting question is not "how would I write a router" — the partner project answers that in about forty lines. The interesting question is "what does the tool make me deal with that the hand-written version quietly skipped", and only a real tool over a real broker can answer it.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| RabbitMQ broker image | `rabbitmq:4.3.6-alpine` |
| Apache Camel | 4.20.0 (`camel-core`, `camel-spring-rabbitmq`) |
| RabbitMQ Java client | 5.36.0 |
| Testcontainers | 2.0.5 |

RabbitMQ 4 no longer permits transient non-exclusive queues, so every queue this demo declares is durable. That is not a workaround; it is what the current broker requires.

## What it costs

The first run pulls the broker image, about seventy megabytes to download and about a hundred and sixty once unpacked, and the Testcontainers helper image. After that the demo takes about twenty seconds end to end, and the broker uses a couple of hundred megabytes of memory while it runs. Camel itself adds a library and, more to the point, a second way of describing behaviour that a reader of the codebase has to learn.

## Where this pattern lives

In an integration layer: Camel routes, Spring Integration flows, an enterprise service bus, or a broker's own exchange and binding rules. Anywhere one stream of messages carries several kinds of work.

# Dependencies

This project uses Apache Camel, which the plain Java version of Message
Filter does not. Skipping it loses none of the pattern: the plain version
teaches all of it with nothing installed.

## What Apache Camel is

Camel is a library for moving messages. A route begins with from, names an endpoint, and lists steps. filter lets a message continue only if a rule says yes. choice, when and otherwise are Camel's if, else-if and else. multicast sends a copy of one message to several endpoints.

## What the Simple language is

Simple is Camel's small expression language, written inside strings. ${body.gift} calls isGift() on the message body; ${header.threshold} reads a header set earlier in the route. Expressions are evaluated when each message passes, which is why a threshold can change while the routes run.

## Why this project uses them

The plain version shows the idea. This version shows how an integration
library expresses it: as a step in a route, with rules next to the routing,
and with a discard channel that is easy to add.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than ten library files on the classpath.
- Rules in strings are checked at run time, not by the compiler.

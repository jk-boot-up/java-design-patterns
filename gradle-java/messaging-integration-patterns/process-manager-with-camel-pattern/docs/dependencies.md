# Dependencies

This project uses Apache Camel and its Saga step, which the plain Java
version of Process Manager does not. Skipping it loses none of the pattern:
the plain version teaches all of it with nothing installed.

## What Apache Camel is

Camel is a library for moving messages. A route begins with from and lists steps.

## What a saga in Camel is

saga starts a saga for the message. completion names the route Camel calls when the saga ends well; compensation names the route it calls to undo, when a step fails. A step route that joins the saga with propagation MANDATORY can name its own compensation. option copies a value, such as the order number, into headers that the completion and compensation routes receive. The saga service keeps track of open sagas; the in-memory one used here forgets them when the program stops.

## Why this project uses them

The plain version shows the idea. This version shows the form a process
manager takes in production when a journey crosses services: a saga with
declared compensations.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core, with InMemorySagaService) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than ten library files on the classpath.
- Compensations run on Camel's own threads, so results must be waited for.
- An in-memory saga service that does not survive a restart.

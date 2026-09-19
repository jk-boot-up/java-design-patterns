# Dependencies

This project uses two things the hand-built projects do not: Hibernate and H2.
This page says what they are, why they are here, and what they cost. It comes
before the first annotation on purpose.

**Skipping this project loses none of the pattern.** [Lazy Load](../lazy-load-pattern)
teaches all of it with plain Java. This project only shows you where you have
already met it, and explains an exception.

## What Hibernate is

Hibernate ORM is the most widely used implementation of JPA, the Java standard for
storing objects in a relational database. You write plain classes, mark them with
annotations such as `@Entity`, and Hibernate turns operations on them into SQL.
`FetchType.LAZY` is one of its settings.

## What H2 is

H2 is a database written in Java. It runs entirely in memory, inside the test, and
vanishes when the process ends, so nothing needs installing.

## Why this project uses them

A genuine `LazyInitializationException` cannot be faked convincingly, and faking
it would defeat the project. It comes from Hibernate's own proxy.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version | Where the version comes from |
| --- | --- | --- |
| Hibernate ORM | 7.4.5.Final | Spring Boot 4.1.1's bill of materials |
| H2 | 2.4.240 | Spring Boot 4.1.1's bill of materials |

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. After that it
runs offline. Start-up takes a second or two.

## Where this pattern lives

In every `FetchType.LAZY` association, and in the proxy Hibernate generates for it.

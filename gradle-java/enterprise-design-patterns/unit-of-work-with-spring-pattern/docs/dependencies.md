# Dependencies

This project uses three things the hand-built projects do not: Spring Boot,
Hibernate and H2. This page says what they are, why they are here, and what they
cost. It comes before the first annotation on purpose.

**Skipping this project loses none of the pattern.** [Unit of Work](../unit-of-work-pattern)
teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework that creates the objects of an application and wires them
together. Spring Boot configures it with sensible defaults. `@Service` marks a
class Spring should create. `@Transactional` marks a method Spring should wrap in
a transaction.

## What Hibernate and H2 are

Hibernate is the JPA implementation that turns operations on objects into SQL.
H2 is a database written in Java that runs in memory, so nothing needs installing.

## Why this project uses them

`@Transactional` is the pattern as most readers meet it, and its surprises, the
checked exception that commits and the flush nobody wrote, are Spring's own.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Hibernate ORM | whatever Spring Boot 4.1.1 manages (7.x) |
| H2 | whatever Spring Boot 4.1.1 manages |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about sixty megabytes of jars. After that it
runs offline. Starting the Spring context takes two to four seconds, where the
hand-built project takes milliseconds.

## Where this pattern lives

At every `@Transactional` boundary, in the proxy Spring wraps around the bean.

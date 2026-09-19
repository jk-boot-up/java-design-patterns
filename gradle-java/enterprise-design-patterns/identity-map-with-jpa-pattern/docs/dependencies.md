# Dependencies

This project uses two things the hand-built projects do not: Hibernate and H2.
This page says what they are, why they are here, and what they cost. It comes
before the first annotation on purpose.

**Skipping this project loses none of the pattern.** [Identity Map](../identity-map-pattern)
teaches all of it with plain Java. This project only shows you where you have
already met it.

## What Hibernate is

Hibernate ORM is the most widely used implementation of JPA, the Java standard
for storing objects in a relational database. You write plain classes, mark them
with annotations such as `@Entity`, and Hibernate turns operations on them into
SQL. It is what most Java applications use underneath Spring Data.

## What H2 is

H2 is a database written in Java. It can run entirely in memory, inside the same
process as the test, and vanishes when the process ends. It is here so nothing
needs installing. A real application would use PostgreSQL or similar.

## Why this project uses them

The persistence context is part of Hibernate. Nothing else demonstrates it, and
the detached-entity failure needs a real one.

## What to install

Only a JDK, version 21. Gradle downloads the rest on the first run, and the
versions are pinned:

| Dependency | Version | Where the version comes from |
| --- | --- | --- |
| Hibernate ORM | 7.4.5.Final | Spring Boot 4.1.1's bill of materials |
| H2 | 2.4.240 | Spring Boot 4.1.1's bill of materials |
| Jakarta Persistence API | 3.2.0 | Spring Boot 4.1.1's bill of materials |

Spring Boot itself is not a dependency. Its bill of materials is used only so
these versions are ones that release was tested together.

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. After that it
runs offline. Start-up takes a second or two, where the hand-built projects take
milliseconds.

## Where this pattern lives

In the `EntityManager`. Every `find` consults the persistence context first.

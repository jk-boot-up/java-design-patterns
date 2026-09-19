# Dependencies

This project uses three things the hand-built projects do not: Spring Boot,
Spring Data JPA, and Hibernate with H2. This page says what they are, why they are
here, and what they cost. It comes before the first annotation on purpose.

**Skipping this project loses none of the pattern.** [Repository](../repository-pattern)
teaches all of it with plain Java.

## What Spring Data JPA is

Spring Data JPA writes your repository for you. You declare an interface that
extends `JpaRepository`, and at start-up Spring generates a class that implements
it, including queries built from your method names.

## What Spring Boot, Hibernate and H2 are

Spring Boot creates and wires the objects of an application. Hibernate is the JPA
implementation that turns operations on objects into SQL. H2 is a database written
in Java that runs in memory, so nothing needs installing.

## Why this project uses them

An interface with no implementation cannot be shown any other way. And the leak,
the managed entity, is a property of the persistence context.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Data JPA | whatever Spring Boot 4.1.1 manages |
| Hibernate ORM | whatever Spring Boot 4.1.1 manages (7.x) |
| H2 | whatever Spring Boot 4.1.1 manages |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about sixty megabytes of jars. After that it
runs offline. Starting the Spring context takes two to four seconds.

## Where this pattern lives

In every interface that extends `JpaRepository`, and in the class Spring generates
for it.

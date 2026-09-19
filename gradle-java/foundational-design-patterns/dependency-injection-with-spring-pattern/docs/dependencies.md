# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is,
why it is here, and what it costs. It comes before the first annotation on purpose.

**Skipping this project loses none of the pattern.** [Dependency Injection](../dependency-injection-pattern)
teaches all of it, and writes a container.

## What Spring Boot is

Spring is a framework whose core is a container: it creates the objects of an application and
wires them together. Spring Boot configures it with sensible defaults. `@Component` marks a class
Spring should create.

## Why this project uses it

Spring is how nearly every reader has met dependency injection. Recognition is the whole job.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Framework | whatever Spring Boot 4.1.1 manages |

There is no web server, no database and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty megabytes of jars. After that it runs offline.
Starting a context takes a few milliseconds here and grows with the size of the application.

## Where this pattern lives

In the `ApplicationContext`, which reads constructors and builds beans.

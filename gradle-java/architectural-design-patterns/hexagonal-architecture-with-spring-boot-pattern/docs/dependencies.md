# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Hexagonal Architecture](../hexagonal-architecture-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring Boot's container creates beans and can choose among them by a property. H2 is an in-memory database used by one adapter. ArchUnit checks dependencies between packages.

## Why this project uses it

It shows the hexagon in the framework most teams use, and where the framework can undo it.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `spring-boot-starter-jdbc` | managed by Spring Boot 4.1.1 |
| H2 | managed by Spring Boot 4.1.1 |
| ArchUnit | 1.5.0 |

There is no web server. Both driving adapters are plain classes.

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. After that it runs offline.

## Where this pattern lives

In `@ConditionalOnProperty` on the adapters, in `ShopConfig`, and in one ArchUnit rule.

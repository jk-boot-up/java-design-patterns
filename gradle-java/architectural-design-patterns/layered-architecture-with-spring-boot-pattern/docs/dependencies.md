# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Layered Architecture](../layered-architecture-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring Boot provides the web server, the container and a transaction manager. `@RestController`, `@Service` and `@Repository` mark the layers. H2 is an in-memory database. ArchUnit checks dependencies between packages in a test.

## Why this project uses it

It is the layered architecture most Java teams actually run, and its failure is the one the partner warned about.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `spring-boot-starter-webmvc` | managed by Spring Boot 4.1.1 |
| `spring-boot-starter-jdbc` | managed by Spring Boot 4.1.1 |
| H2 | managed by Spring Boot 4.1.1 |
| ArchUnit | 1.5.0 |

The demo starts a real web server on a free port.

## What it costs

The first `./gradlew run` downloads about sixty megabytes of jars. After that it runs offline. The server starts in about a second.

## Where this pattern lives

In the stereotype annotations, in `@Transactional` on the service, and in one ArchUnit rule.

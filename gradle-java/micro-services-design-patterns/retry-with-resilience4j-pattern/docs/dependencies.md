# Dependencies

This project uses Resilience4j, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Retry with Backoff](../retry-pattern) teaches all of it with plain Java.

## What Resilience4j is

Resilience4j is a lightweight fault-tolerance library. Its retry repeats a failed call up to a number of attempts, with a wait that can grow, and only for the exceptions you list. Its Spring Boot module applies it through an annotation.

## Why this project uses it

It is the retry most Spring services use today, and its settings are where the mistakes are made.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `io.github.resilience4j:resilience4j-spring-boot4` | 2.4.0 |
| `spring-boot-starter-aspectj` | managed by Spring Boot 4.1.1 |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. After that it runs offline. The waits in this project are one and two milliseconds, so the demo does not sit idle.

## Where this pattern lives

In `application.properties`, under `resilience4j.retry.instances`, and in one annotation per method.

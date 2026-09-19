# Dependencies

This project uses Resilience4j, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Circuit Breaker](../circuit-breaker-pattern) teaches all of it with plain Java.

## What Resilience4j is

Resilience4j is a lightweight fault-tolerance library. Its circuit breaker keeps a sliding window of recent calls, and its Spring Boot module reads settings from `application.properties` and applies the breaker through an annotation.

## Why this project uses it

It is the breaker most Spring services use today, so the way it can be bypassed or misconfigured is worth seeing.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `io.github.resilience4j:resilience4j-spring-boot4` | 2.4.0 |
| `spring-boot-starter-aspectj` | managed by Spring Boot 4.1.1 |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. After that it runs offline.

## Where this pattern lives

In `application.properties`, under `resilience4j.circuitbreaker.instances`, and in one annotation per protected method.

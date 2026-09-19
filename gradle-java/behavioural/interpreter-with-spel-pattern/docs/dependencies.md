# Dependencies

This project uses Spring Expression Language, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Interpreter](../interpreter-pattern) teaches all of it with plain Java.

## What Spring Expression Language is

SpEL is the expression language in the Spring Framework. `spring-expression` is a small library and does not need the Spring container.

## Why this project uses it

It is the interpreter most Java developers will meet, and the safe way to use it is a choice, not a default.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| `org.springframework:spring-expression` | managed by Spring Boot 4.1.1 |

No container starts in this project. Only the expression library is used.

## What it costs

The first `./gradlew run` downloads a few megabytes of jars. After that it runs offline.

## Where this pattern lives

In the evaluation context you choose: full, or read-only.

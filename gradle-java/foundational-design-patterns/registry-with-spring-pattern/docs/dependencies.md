# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it
is here, and what it costs. It comes before the first annotation on purpose.

**Skipping this project loses none of the pattern.** [Registry](../registry-pattern) teaches all of it with
plain Java.

## What Spring Boot is

Spring is a framework whose core is a container, the `ApplicationContext`: it creates the objects of an
application and lets you find them by type. Spring Boot configures it with sensible defaults, and its test
support caches contexts between tests.

## Why this project uses it

The context is the registry most readers have met. The test-cache leak is Spring's own, and cannot be shown
any other way.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Framework and Spring Test | whatever Spring Boot 4.1.1 manages |

There is no web server, no database and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty megabytes of jars. After that it runs offline. Each context
takes a few hundred milliseconds to start, and the tests start several.

## Where this pattern lives

In `ApplicationContext.getBean`, `Environment.getProperty`, and the Spring TestContext cache.

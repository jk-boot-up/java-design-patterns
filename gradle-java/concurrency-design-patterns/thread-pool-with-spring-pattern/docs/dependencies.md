# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Thread Pool](../thread-pool-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. Spring Boot configures it with defaults. `@Async` marks a method that should run on another thread, and the container supplies the thread pool, a `ThreadPoolTaskExecutor`.

## Why this project uses it

The pool behind `@Async` is a real thread pool with real defaults, and those defaults, and the annotation's proxy, are what this project examines. Nothing else shows them.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Framework | whatever Spring Boot 4.1.1 manages |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty megabytes of jars. After that it runs offline. Each Spring context takes a few hundred milliseconds to start, and the demo starts several.

## Where this pattern lives

In `ThreadPoolTaskExecutor`, and in the proxy Spring wraps around every bean that has an `@Async` method.

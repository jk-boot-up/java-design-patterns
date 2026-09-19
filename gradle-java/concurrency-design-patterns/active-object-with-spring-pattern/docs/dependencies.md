# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Active Object](../active-object-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. `@Async("name")` sends a method to a named executor. Give that executor exactly one thread and a queue, and you have a mailbox and a worker.

## Why this project uses it

It shows the pattern as most Java developers would build it, and the failures that come from the proxy and the executor are Spring's own.

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

In a `ThreadPoolTaskExecutor` with a core and max size of one, and every `@Async("name")` method that uses it.

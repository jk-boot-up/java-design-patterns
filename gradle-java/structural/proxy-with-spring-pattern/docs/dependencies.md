# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Proxy](../proxy-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. With its AspectJ support, it wraps a bean in a generated subclass and runs advice, written once in an aspect, around matching calls.

## Why this project uses it

It is how most Spring code gets its proxies: transactions, caching, security and async all work this way.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `spring-boot-starter-aspectj` | managed by Spring Boot 4.1.1 |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty-five megabytes of jars. After that it runs offline. Proxies are generated at startup, which adds a few milliseconds per proxied bean.

## Where this pattern lives

In the aspect class, and in the annotation that selects the methods.

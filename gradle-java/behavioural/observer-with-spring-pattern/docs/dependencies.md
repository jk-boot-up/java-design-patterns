# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Observer](../observer-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. It includes an event publisher, and every bean method marked `@EventListener` receives events of its argument's type.

## Why this project uses it

It is the observer most Spring applications use, so the surprises are worth knowing.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty megabytes of jars. After that it runs offline.

## Where this pattern lives

In the listener annotations, the ordering annotations, and `@EnableAsync`.

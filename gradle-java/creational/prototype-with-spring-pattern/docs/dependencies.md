# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Prototype](../prototype-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. Its prototype scope builds a new instance of a bean every time one is requested.

## Why this project uses it

It is the form of Prototype most developers meet first, and it means something different from the pattern.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Framework | whatever Spring Boot 4.1.1 manages |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty megabytes of jars. After that it runs offline. Each Spring context takes a few hundred milliseconds to start.

## Where this pattern lives

In the scope annotation on the `Listing` class, and in every place that asks for one.

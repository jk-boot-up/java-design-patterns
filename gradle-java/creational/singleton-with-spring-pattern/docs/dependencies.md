# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Singleton](../singleton-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application and hands them to the code that needs them. By default each bean is a singleton within its container.

## Why this project uses it

Most Java code today gets its singletons from a container, not from a static field. The guarantee is different, and so are the ways it breaks.

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

In the bean definition: scope, laziness, and the container that holds it.

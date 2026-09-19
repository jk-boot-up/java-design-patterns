# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Chain of Responsibility](../chain-of-responsibility-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. Ask for a list of an interface and it injects every bean of that type, sorted by `@Order`.

## Why this project uses it

It removes the hand-written wiring of successors, and it moves the order into annotations.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about thirty megabytes of jars. After that it runs offline.

## Where this pattern lives

In the `@Order` annotations, and in `@ConditionalOnProperty` on any link that can be switched off.

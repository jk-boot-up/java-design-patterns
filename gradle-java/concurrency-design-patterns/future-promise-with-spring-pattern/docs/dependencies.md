# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Future/Promise](../future-promise-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring is a framework whose core is a container that creates the objects of an application. `@Async` marks a method that should run on another thread. If it returns a `CompletableFuture`, the container completes that future with the method's result, or fails it with the method's exception.

## Why this project uses it

`@Async` is how most Java developers meet the Future/Promise split, and what it loses (exceptions, context, cancellation) is Spring's own and cannot be shown any other way.

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

In every `@Async` method that returns a `CompletableFuture`, and in the `TaskDecorator` and `AsyncUncaughtExceptionHandler` beans that customise it.

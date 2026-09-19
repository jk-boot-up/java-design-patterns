# Dependencies

This project uses Spring MVC, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [MVC](../mvc-pattern) teaches all of it with plain Java.

## What Spring MVC is

Spring MVC maps HTTP requests to controller methods. A returned name is resolved to a template, and Thymeleaf fills the template from the model. A method marked as a response body is turned into JSON instead.

## Why this project uses it

It is the MVC most Java web developers use, and its templates are where the pattern most often leaks.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `spring-boot-starter-webmvc` | managed by Spring Boot 4.1.1 |
| `spring-boot-starter-thymeleaf` | managed by Spring Boot 4.1.1 |

The demo starts a real web server on a free port.

## What it costs

The first `./gradlew run` downloads about sixty megabytes of jars. After that it runs offline. The server starts in about a second.

## Where this pattern lives

In `@Controller` methods and in the templates under `src/main/resources/templates`.

# Dependencies

This project uses Spring Cloud Gateway, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [API Gateway](../api-gateway-pattern) teaches all of it with plain Java.

## What Spring Cloud Gateway is

Spring Cloud Gateway is a project of Spring Cloud. It runs on Spring WebFlux and Netty. A route matches a request by predicates, such as a path, applies filters, and forwards it to a URI.

## Why this project uses it

It is the gateway most Spring shops use, and the way it behaves at the edges, on errors and on slow services, is worth seeing.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Cloud BOM | 2025.1.3 |
| `spring-cloud-starter-gateway-server-webflux` | 5.0.3 (managed by the Spring Cloud BOM) |

The four services are plain JDK HTTP servers on free local ports, so nothing else is installed.

## What it costs

The first `./gradlew run` downloads about sixty megabytes of jars, including Netty. After that it runs offline. Each gateway starts in about a second.

## Where this pattern lives

In a `RouteLocator` bean, in filters, and in `spring.cloud.gateway.server.webflux.*` settings.

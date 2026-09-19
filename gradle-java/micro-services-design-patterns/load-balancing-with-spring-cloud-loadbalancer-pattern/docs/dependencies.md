# Dependencies

This project uses Spring Cloud LoadBalancer, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Client-Side Load Balancing](../load-balancing-pattern) teaches all of it with plain Java.

## What Spring Cloud LoadBalancer is

Spring Cloud LoadBalancer plugs into Spring's HTTP clients. An instance list comes from a discovery client, here a fixed list in configuration, and a balancer chooses from it for each request.

## Why this project uses it

It is the balancer inside most Spring service-to-service calls, and it is replaceable one service name at a time.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Cloud BOM | 2025.1.3 |
| `spring-cloud-starter-loadbalancer` | 5.0.3 (managed by the Spring Cloud BOM) |
| `spring-boot-starter-restclient` | managed by Spring Boot 4.1.1 |

The three copies are plain JDK HTTP servers on free local ports.

## What it costs

The first `./gradlew run` downloads about fifty megabytes of jars. After that it runs offline.

## Where this pattern lives

In a `@LoadBalanced` client builder, in `spring.cloud.discovery.client.simple.instances.*`, and in `@LoadBalancerClient` for a custom strategy.

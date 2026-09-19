# Dependencies

This project uses Spring Cloud Consul, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Service Registry and Discovery](../service-discovery-pattern) teaches all of it with plain Java.

## What Spring Cloud Consul is

Consul is a service registry with health checks. Spring Cloud Consul registers each Spring Boot application with it at startup and removes it on a graceful shutdown. Its discovery client returns the copies whose health check passes.

## Why this project uses it

It is a real registry, so the timing of registration, health checks and failure is real too.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Cloud BOM | 2025.1.3 |
| `spring-cloud-starter-consul-discovery` | 5.0.3 (managed by the Spring Cloud BOM) |
| `spring-cloud-starter-loadbalancer` | 5.0.3 (brought in by the discovery starter) |
| `spring-boot-starter-actuator` | managed by Spring Boot 4.1.1 (the health check calls it) |
| Consul | 1.16 or later, the `consul` program on the PATH |

Install Consul with `brew install consul`, or download it from HashiCorp. The demo starts its own agent in development mode on free ports, and stops it afterwards.

## What it costs

The first `./gradlew run` downloads about seventy megabytes of jars. The demo takes about half a minute, because it waits for a real health check to fail.

## Where this pattern lives

In `spring.cloud.consul.*` settings, and in the health check interval of each service.

# Dependencies

This project uses Spring Cloud Gateway, which the plain Java version of
Gateway Offloading does not. Skipping it loses none of the pattern: the plain
version teaches all of it with nothing installed.

## What Spring Cloud Gateway is

Spring Cloud Gateway is a gateway built on Spring Boot and the reactive web stack. A route matches requests, here by path, and forwards them to a service's address. A global filter runs for every route, before forwarding; it can refuse a request, or change it, for example by adding or removing headers.

## What Reactor Netty is

Reactor Netty is the server underneath the gateway. The Spring Boot properties server.compression.enabled, mime-types and min-response-size make it gzip responses for clients that ask.

## What Release trains is

Spring Cloud versions come in release trains that match a Spring Boot line: train 2025.1.3 goes with Spring Boot 4.1.1.

## Why this project uses them

The plain version shows the idea. This version shows the gateway most Spring
teams actually run, and where each chore lives in it.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot | 4.1.1 |
| Spring Cloud release train | 2025.1.3 |

## What it costs

- A reactive framework to learn for filters.
- A gateway to run with high availability.

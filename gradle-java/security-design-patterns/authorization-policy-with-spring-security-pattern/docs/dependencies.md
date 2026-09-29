# Dependencies

This project uses Spring Boot and Spring Security, which the plain Java
version of Authorization Policy does not. Skipping it loses none of the
pattern: the plain version teaches all of it with nothing installed.

## What Spring Boot is

Spring Boot starts a Java web server from your classes, here on a free local port.

## What Spring Security is

Spring Security checks every request before your code runs. authorizeHttpRequests lists URL rules, first match wins; denyAll refuses everything else. With method security switched on, @PreAuthorize puts a rule on a single method, written in the Spring Expression Language: hasRole checks a role, #amount reads a parameter, and @orderPolicy calls a bean. A refused request gets HTTP 403. With an AuthorizationEventPublisher, each refusal is published as an AuthorizationDeniedEvent.

## Why this project uses them

The plain version shows the idea in one class. This version shows how most
Java web applications actually express a policy, and the details that trip
people up.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot (webmvc, security starters) | 4.1.1 |

## What it costs

- A framework and its expression language to learn.
- Rules in two places, URL and method, to keep in step.

# Dependencies

This project uses Spring MVC through Spring Boot, which the plain Java
version of Page Controller does not. Skipping it loses none of the pattern:
the plain version teaches all of it with nothing installed.

## What Spring MVC is

Spring MVC routes web requests to Java methods. @RestController marks a class whose methods answer requests. @GetMapping gives the path a method answers. @RequestParam reads a query parameter and converts it to the parameter's type, answering 400 if it cannot. A ResponseStatusException carries the status to answer with. A HandlerInterceptor runs before the controllers it is registered for, and can stop the request.

## What Spring Boot is

Spring Boot starts an embedded web server and finds the controllers by their annotations.

## Why this project uses them

The plain version registers handlers by hand. This version shows how most
Java web applications are organised, and where Spring puts the checks that
every page needs.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot (webmvc starter) | 4.1.1 |

## What it costs

- A framework and its conventions to learn.

# Dependencies

This project uses Spring MVC through Spring Boot, which the plain Java
version of Remote Facade does not. Skipping it loses none of the pattern: the
plain version teaches all of it with nothing installed.

## What Spring MVC and Jackson is

A @RestController method's return value becomes the response; Jackson turns a Java record into JSON. @RequestBody turns a request's JSON into a record. @ExceptionHandler catches an exception from the controller and decides the response; ProblemDetail is Spring's standard problem report, sent as application/problem+json.

## What A servlet filter is

A filter runs for every request before any controller. Here MobileNetwork adds 80 milliseconds, to play a mobile network's round trip.

## Why this project uses them

The plain version builds the facade by hand. This version shows how most Java
services offer one, with JSON and standard error reports for free.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot (webmvc starter) | 4.1.1 |

## What it costs

- A framework to run for what could be a few handlers.

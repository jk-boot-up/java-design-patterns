# Dependencies

This project uses Vavr, which the plain Java version of Railway-Oriented
Programming does not. Skipping it loses none of the pattern: the plain
version teaches all of it with nothing installed.

## What Vavr is

Vavr is a functional library for Java. Either holds a Left or a Right; by convention Left is the failure and Right the success, and flatMap and map work on the Right, passing a Left straight through. fold turns either side into one answer. orElse supplies another Either when the first is a Left. Try.of runs code that may throw and holds the result or the exception; toEither turns it into an Either. Validation holds a valid value or errors; combine checks several Validations and collects all their errors.

## Why this project uses them

The plain version builds the idea. This version shows the library Java
developers most often use for it, and the Validation type that removes the
railway's one-error limit.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Vavr | 1.0.1 |

## What it costs

- A library and its conventions to learn.

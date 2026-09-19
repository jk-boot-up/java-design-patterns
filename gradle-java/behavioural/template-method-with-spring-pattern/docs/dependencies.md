# Dependencies

This project uses Spring Boot, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Template Method](../template-method-pattern) teaches all of it with plain Java.

## What Spring Boot is

Spring's JDBC support includes `JdbcTemplate`, which owns the connection, the statement, the loop over rows, the closing, and the translation of errors. H2 is a small database that runs inside the same process.

## Why this project uses it

It is the textbook example of Template Method in a real library, and it uses composition where the partner used inheritance.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| `spring-boot-starter-jdbc` | managed by Spring Boot 4.1.1 (brings HikariCP) |
| H2 | managed by Spring Boot 4.1.1 |

There is no web server and no web starter.

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. After that it runs offline. H2 runs in memory, so there is nothing to install or clean up.

## Where this pattern lives

In `JdbcTemplate` and `TransactionTemplate`, and the lambdas passed to them.

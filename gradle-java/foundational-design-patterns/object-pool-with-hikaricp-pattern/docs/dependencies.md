# Dependencies

This project uses two things the hand-built projects do not: HikariCP and H2. This page says what they are,
why they are here, and what they cost. It comes before the first line of pool code on purpose.

**Skipping this project loses none of the pattern.** [Object Pool](../object-pool-pattern) teaches all of it with
plain Java.

## What HikariCP is

HikariCP is a JDBC connection pool. You ask it for a connection, use it, and close it. Closing does not close the
connection; it returns it to the pool. It is the default pool in Spring Boot.

## What H2 is

H2 is a database written in Java that runs in memory, so nothing needs installing.

## Why this project uses them

A real connection pool is the mature answer to the hand-built pool's costs, and cannot be shown any other way.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| HikariCP | whatever Spring Boot 4.1.1's bill of materials manages |
| H2 | whatever Spring Boot 4.1.1's bill of materials manages |
| slf4j-nop | the same bill of materials; it only silences logging |

Spring Boot itself is not a dependency.

## What it costs

The first `./gradlew run` downloads a few megabytes of jars. After that it runs offline. The demo takes about ten
seconds, mostly waiting on the pool-sizing act.

## Where this pattern lives

In `HikariDataSource`, the object behind every `DataSource` in a Spring Boot application.

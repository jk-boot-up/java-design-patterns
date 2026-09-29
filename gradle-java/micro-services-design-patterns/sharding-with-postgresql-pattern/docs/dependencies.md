# Dependencies

This project uses real PostgreSQL databases, run in containers by
Testcontainers, which the plain Java version of Sharding does not. Skipping it
loses none of the pattern: the plain version teaches all of it with nothing
installed.

## What PostgreSQL is

PostgreSQL is a relational database. Here there are three separate PostgreSQL servers, each with the same two tables. A UNIQUE constraint makes one database refuse a second row with the same value, but it only sees its own rows.

## What Testcontainers is

Testcontainers is a Java library that starts containers from inside a program and removes them afterwards. The demo starts the three databases at the same time.

## Why this project uses them

The plain version shows the idea. This version shows what three real
databases can no longer do together: answer one query, enforce one rule, or
share one transaction.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| PostgreSQL image | postgres:18.6-alpine |
| PostgreSQL JDBC driver | 42.7.13 |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and several database containers to start.
- Routing, merging and cross-shard rules written in the application.

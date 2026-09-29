# Dependencies

This project uses a real Redis and a real PostgreSQL, run in containers by
Testcontainers, which the plain Java version of Write-Through Cache does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What Redis is

Redis is an in-memory data store run as its own server, often used as a cache shared by many application instances. SET stores a value under a key, optionally with an expiry in seconds; GET reads it. INFO stats reports counters such as keyspace_hits, the number of reads that found their key.

## What PostgreSQL is

PostgreSQL is a relational database. Here it holds one table, prices, the record of truth. A session can be made read-only, which is how the demo simulates maintenance.

## What Testcontainers is

Testcontainers is a Java library that starts containers from inside a program and removes them afterwards. The demo also pauses the Redis container, to make it unreachable for a moment.

## Why this project uses them

The plain version shows the idea. This version shows a shared cache server,
and the consistency gap between two real systems that the plain version, with
both stores in one program, could not have.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| Redis image | redis:8.10.2-alpine |
| PostgreSQL image | postgres:18.6-alpine |
| Jedis | 8.0.1 |
| PostgreSQL JDBC driver | 42.7.13 |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and a first run that downloads two images.
- Two servers to run in production, and a plan for when they disagree.

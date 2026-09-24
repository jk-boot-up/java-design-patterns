# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts a Redis container and stops it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need Redis are skipped and the rest still run.
- The plain-Java Publisher-Subscriber project in this course is the hand-built version this project pairs with. Reading it first helps, but this project explains everything it uses on its own.

## Explicitly not required

- No prior Redis. Every word it introduces — publish, channel, subscribe, pattern subscription, output buffer — is said in plain language before the name for it is used.
- No installed Redis, and no Redis configuration on your machine. The server lives in the container for the length of the run.
- No messaging experience of any kind.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the Redis image; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| Redis server image | `redis:8.10.2-alpine` |
| `redis.clients:jedis` | 8.0.1 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back.

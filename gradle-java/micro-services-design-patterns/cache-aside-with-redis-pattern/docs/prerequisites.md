# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts a Redis container and stops it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need Redis are skipped and the rest still run.
- The idea of cache-aside: the shop asks the cache first, and on a miss asks the database and remembers the answer. The plain-Java Cache-Aside project in this course teaches it with nothing installed, but this project explains everything it uses in its own files, so it can be read on its own.

## Explicitly not required

- No prior Redis. Every word it introduces — key, value, expiry and its name TTL, SET, NX, redis-cli, maxmemory, eviction — is said in plain language before the name for it is used.
- No installed Redis, and no Redis configuration on your machine. The server lives in the container for the length of the run.
- No experience with threads. The fifth act starts fifty of them, and the code that does it is a dozen lines.

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

# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts a Redis container and stops it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need Redis are skipped and the rest still run.
- The plain-Java Rate Limiter project in this course, the hand-built version this project pairs with. Reading it first helps, but this project explains the token bucket again in its own documents, so it is not required.

## Explicitly not required

- No prior Redis. Every word it introduces — key, time to live, script — is said in plain language before the name for it is used.
- No prior Bucket4j. Its words — bucket configuration, proxy manager, compare-and-swap, client clock — are said in plain language first too.
- No installed Redis, and no Redis configuration on your machine. Redis lives in the container for the length of the run, on a random free port.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the Redis image; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| Redis image | `redis:8.10.2-alpine` |
| `com.bucket4j:bucket4j_jdk17-lettuce` | 8.20.0 |
| `io.lettuce:lettuce-core` | 7.7.0.RELEASE |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back.

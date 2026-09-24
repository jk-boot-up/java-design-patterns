# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later, with about 1.5 GB of disk free for the two images. The demo starts one PostgreSQL container and one MongoDB container and removes both at the end. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need the databases are skipped and the rest still run.
- The plain-Java Database per Service project in this course, the hand-built version this project pairs with. Reading it first helps, but this project tells the whole story again in its own documents, so it is not required.

## Explicitly not required

- No prior SQL beyond "a query asks a database a question". Every term — table, column, join, foreign key, transaction, rollback — is said in plain language before it is used.
- No prior MongoDB. Its words — document, collection, find, `$lookup` — are said in plain language first too.
- No installed PostgreSQL or MongoDB, and no configuration on your machine. Both live in containers for the length of the run, each on a random free port.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls both images; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| PostgreSQL image | `postgres:18.6-alpine` |
| MongoDB image | `mongo:8.3.11-noble` |
| `org.postgresql:postgresql` | 42.7.13 |
| `org.mongodb:mongodb-driver-sync` | 5.12.0 |
| `org.testcontainers:testcontainers-postgresql` | 2.0.5 |
| `org.testcontainers:testcontainers-mongodb` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back. MongoDB publishes no Alpine image; `noble`, Ubuntu 24.04, is its smallest official Linux image.

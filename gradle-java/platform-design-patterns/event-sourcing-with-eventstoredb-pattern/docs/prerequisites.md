# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts one KurrentDB container and stops it again. With no runtime, the demo prints two sentences saying what to do, and stops. The tests that need KurrentDB are skipped and the rest still run.
- About 600 MB of free disk for the KurrentDB image, and about 200 MB of memory for the container while it runs.
- The idea of event sourcing: keep every change as an event, never edit one, and add them up to get the current state. The plain-Java Event Sourcing project in this course teaches it with nothing installed. This project explains everything it uses in its own files, so you can read it on its own.

## Explicitly not required

- No prior EventStoreDB or KurrentDB. Every word it introduces is said in plain language before the name for it is used: stream, revision, append, expected revision, WrongExpectedVersion, event id, catch-up subscription, projection, `$all`, soft delete, tombstone, scavenge, insecure mode and TLS.
- No installed KurrentDB and no configuration on your machine. The server lives in the container for the length of the run.
- No knowledge of gRPC, the network protocol the client uses. The client hides it.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the KurrentDB image. After that it works with no network.

## A note on the name

EventStoreDB was renamed KurrentDB by its vendor. It is the same database, and the directory keeps the old name because most material still uses it. New versions ship only under the new name, so this project uses the KurrentDB image and the KurrentDB Java client.

## A note on security

The demo runs KurrentDB in insecure mode, `KURRENTDB_INSECURE=true`. That means no TLS, so network traffic is not encrypted, and no user accounts, so anyone who can reach the port can read and write everything. It keeps the demo to one container on your own machine, on a random local port. A production server must never run like this.

## Versions this project pins

| Tool | Version |
| --- | --- |
| KurrentDB server image (Intel) | `kurrentplatform/kurrentdb:26.1.2` |
| KurrentDB server image (ARM, Apple silicon) | `kurrentplatform/kurrentdb:26.1.2-experimental-arm64-10.0-noble` |
| `io.kurrent:kurrentdb-client` | 1.2.1 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built, and none is held back. The vendor labels its ARM image "experimental", but it is the same 26.1.2 release. The code picks the image that matches your container runtime. There is no Alpine image of KurrentDB.

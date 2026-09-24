# Dependencies

This project uses Redis, Bucket4j, Lettuce and Testcontainers, which the hand-built project does not. This page says what they are, why they are here, and what they cost. It comes before the first line of Redis code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Rate Limiter project in this course teaches the token bucket itself in plain Java, with nothing installed.

## What Redis is

Redis is a separate program that keeps small values in memory, each under a name, and lets many programs read and change them over the network. Think of a whiteboard in a shared office. Anybody can walk up, read what is written under a heading, and rub it out and write something new.

In Redis's words, the heading is a **key**. This project keeps one key per client, named like `search-limit:client-42`, holding that client's bucket. A key can be told to rub itself out after a while; that countdown is its **time to live**. And Redis can be handed a short **script**, a few commands it runs one after another with nothing from any other connection in between, which is how a check and a write become one step.

## What Bucket4j is

Bucket4j is a Java library for rate limiting with a token bucket. On its own it keeps buckets in the program's memory, the way the twin project did. Its Redis integration keeps them in Redis instead. The bucket's size and refill rule is its **bucket configuration**. The object that fetches a client's bucket from Redis and writes it back is its **proxy manager**.

Two of its habits matter here. When it writes a bucket back, it does so only if nobody has changed it since it was read; if somebody has, it reads again and tries again. Bucket4j calls this **compare-and-swap**. And it works out how many tokens have come back using the clock of the server it is running on, which it calls the **client clock**. Redis never looks at a clock.

## What Lettuce is

Lettuce is a Redis client for Java: the part that opens a network connection to Redis and sends it commands. Bucket4j talks through it. Bucket4j's Lettuce module was built against the older Lettuce 6 line and asks the application to supply Lettuce itself; this project supplies the newest, 7.7.0.RELEASE, and the tests confirm the two work together.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns Redis's lifetime: `./gradlew run` brings Redis up, uses it, stops it on purpose in the sixth act, and takes it away. Redis is reached on a random free port chosen each run, so it never clashes with anything else on the machine. Testcontainers 2 has no Redis module, so the core library's generic container is used.

## Why this project uses them

Because the thing this project teaches — one limit shared by every copy of a service — needs a place outside all the copies that each of them can reach. Inside one Java program there is no such place. And the three surprises it shows — two servers reading the same last token, a server with the wrong clock refilling everyone's bucket, and the store itself going away — only happen when the bucket really is somewhere else.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| Redis image | `redis:8.10.2-alpine` |
| `com.bucket4j:bucket4j_jdk17-lettuce` | 8.20.0 |
| `io.lettuce:lettuce-core` | 7.7.0.RELEASE |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back.

## What it costs

The first run pulls the Redis image, about 120 MB once unpacked. After that a run takes about ten seconds, most of it Redis starting. Redis uses a few megabytes of memory for this demo. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

In a real shop the larger cost is on every search: before the search runs, the server makes a round trip to Redis, and if Redis is slow or down, so is the limiter.

## Where this pattern lives in a real system

In a filter or gateway in front of the search endpoint that asks the proxy manager for the caller's bucket; in the bucket configuration, usually read from settings; in the Redis connection that every copy of the service shares; and in the decision, written down somewhere, about what to do when Redis cannot be reached.

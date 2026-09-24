# Dependencies

This project uses Redis, Jedis and Testcontainers, which the hand-built project does not. This page says what they are, why they are here, and what they cost.

**Skipping this project loses none of the pattern.** The plain-Java Publisher-Subscriber project in this course teaches all of it with nothing installed.

## What Redis is

Redis is a server that keeps data in memory and answers over the network. Most people meet it as a cache. It also has a small, separate feature for live announcements, and that is the only part this project uses.

Think of a live radio station. The presenter speaks once, and every radio tuned in at that moment hears it; if your radio was off, there is no recording. In Redis's words, speaking once is **publishing**, the frequency is a **channel** — just a name, here `orders.placed` — and tuning in is **subscribing**. Tuning in to every frequency whose name fits a shape, such as `orders.*`, is a **pattern subscription**. For every listener, Redis keeps a pile of what it has sent but the listener has not read yet; that is the **client output buffer**, and it has a size limit, past which Redis closes the listener's connection.

## What Jedis is

Jedis is a Java library for talking to Redis. Each subscriber in this project holds its own Jedis connection, because a Redis connection that is subscribed can do nothing else until it unsubscribes.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. Here it runs `redis:8.10.2-alpine` on a random free port on your machine, so two copies of the demo, or the demo beside another project using Redis, never collide. Redis needs nothing beyond a plain container, so this project uses the core `testcontainers` module rather than a Redis-specific one.

## Why this project uses them

Because the three things this project teaches — a subscriber in another process, a server that keeps nothing for a latecomer, and a server that cuts off a listener that falls behind — cannot happen when the topic is an object inside the same program as every subscriber.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| Redis server image | `redis:8.10.2-alpine` |
| `redis.clients:jedis` | 8.0.1 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. The Alpine Linux variant of the Redis image is used because it is the smallest.

## What it costs

The first run pulls the Redis image, about 120 MB once unpacked. After that a run takes about ten seconds. Redis itself uses a few megabytes of memory. The second act starts one extra Java process for a moment. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Where this pattern lives in a real system

In a `PUBLISH` call beside the code that changes something, in a long-lived `SUBSCRIBE` connection in each interested service, and in one line of Redis configuration, `client-output-buffer-limit`, that decides how far behind any of them may fall before Redis gives up on it.

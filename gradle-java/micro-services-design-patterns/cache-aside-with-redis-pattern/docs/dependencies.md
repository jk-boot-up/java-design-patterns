# Dependencies

This project uses Redis, Jedis and Testcontainers, which the plain-Java twin does not. This page says what they are, why they are here, and what they cost. It comes before the first line of Redis code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Cache-Aside project in this course teaches all of it, with nothing installed.

## What Redis is

Redis is a separate program that keeps small pieces of data in memory and hands them out very quickly over the network. Think of the whiteboard by the door of a busy kitchen. The recipes live in a thick book in the office, and walking to the office is slow. So when a cook looks something up, they write the answer on the whiteboard, and the next cook reads the board instead of walking to the office. Every cook in the kitchen sees the same board. And the head chef writes a time next to each note, after which it is wiped off, because the book may have changed.

In Redis's words, each note is a **key** and its **value**: here the key `product:SKU-0` and the value `1000`, a price in pence, stored as text. The time a note has left before it is wiped is its **time to live**, which Redis shortens to **TTL**. The command that writes a note is **SET**; SET can carry an expiry with it, and SET with **NX** means "only if nobody has written this key already", which is how this project makes a lock. **redis-cli** is Redis's own command-line program, used here as a second, separate reader. **maxmemory** is the size limit Redis is given, and **eviction** is Redis throwing entries away to stay under it.

## What Jedis is

Jedis is a Java library for talking to Redis. Its method names are the Redis command names — `get`, `set`, `del`, `ttl`, `exists` — so a line of Java reads almost the same as the Redis command it sends. Version 8 names the client `RedisClient`; it keeps a small pool of network connections so that fifty requests at once do not wait for each other.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns Redis's lifetime: `./gradlew run` brings Redis up, uses it, and takes it away at the end. It maps Redis's port to a free random port on your machine, so this demo can run beside any other copy of Redis without a clash. The 2.x line has no dedicated Redis module, so the plain container type is used and told which port Redis listens on.

## Why this project uses them

Because the three things this project teaches — a cache that a second process can see, an entry that expires on a clock nobody in the shop controls, and a stampede that happens without being arranged — cannot happen when the cache is a map inside the shop's own program. The cache has to be its own process, reached over a network, by more than one shop. That is what Redis is.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| Redis server image | `redis:8.10.2-alpine` |
| `redis.clients:jedis` | 8.0.1 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. The Alpine variant of the Redis image is used because it is the smallest.

## What it costs

The first run pulls the Redis image, about 120 MB once unpacked. After that a run takes about ten seconds, most of it the container starting, the second shop's Java process starting twice, and two seconds of genuine waiting for Redis's clock in the fourth act. Redis itself uses a few megabytes of memory for this demo. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Where this pattern lives in a real system

In the service code that reads a price, where the lookup, the miss and the refill sit together; in the one argument on every write that sets the expiry; in the delete that follows every change to the database; in Redis's configuration, where maxmemory and the eviction policy are set; and on the dashboard that watches the hit rate.

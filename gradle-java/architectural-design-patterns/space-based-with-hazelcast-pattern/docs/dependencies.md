# Dependencies

This project uses Hazelcast, which the plain Java version of Space-Based
Architecture does not. Skipping it loses none of the pattern: the plain
version teaches all of it with nothing installed.

## What Hazelcast is

Hazelcast is an in-memory data grid: several programs, called members, join into a cluster and share data. An IMap is a map split across the members; each key has one owning member, and with a backup count of one, another member keeps a copy. An entry processor is a piece of code sent to the owning member and run on one entry, one at a time for that key, so a read-change-write cannot be interleaved. A map store connects a map to a database; with a write delay, it writes in the background, and with write coalescing, only the latest value of each key.

## Why this project uses them

The plain version shows the idea. This version shows how a real data grid
answers the two problems the plain version left open: the oversold last item
and the crashed unit.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Hazelcast | 5.7.0 |

## What it costs

- A cluster to size, run and upgrade in production.
- JVM flags that Hazelcast asks for on newer Java versions, set in build.gradle.

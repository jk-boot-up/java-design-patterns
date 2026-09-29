# Dependencies

This project uses Project Reactor, which the plain Java version of
Backpressure does not. Skipping it loses none of the pattern: the plain
version teaches all of it with nothing installed.

## What Project Reactor is

Reactor is a library for streams of data. A Flux is a stream of zero or more items. Nothing flows until someone subscribes, and a subscriber requests how many items it wants; the source may not send more. limitRate asks for items in batches. publishOn moves work to another thread with a fixed-size queue. onBackpressureLatest, onBackpressureDrop and onBackpressureBuffer say what to do with items a source produces while nobody has asked for them.

## Why this project uses them

The plain version shows the idea with the JDK's Flow interfaces. This version
shows a library where demand runs through every operator, which is how most
Java services meet backpressure in practice.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Project Reactor (reactor-core) | 3.8.7 |

## What it costs

- A reactive style of code to learn and debug.
- An explicit choice for every source that cannot wait.

# Dependencies

This project uses Apache Camel, which the plain Java version of Wire Tap does
not. Skipping it loses none of the pattern: the plain version teaches all of
it with nothing installed.

## What Apache Camel is

Camel is a library for moving messages. A route begins with from and lists steps. wireTap sends a copy of the current message to another endpoint on a separate thread and carries on at once. onPrepare runs a piece of code on that copy just before it is sent; it is where the copy is made independent. The route controller can stop and start a route while the program runs.

## Why this project uses them

The plain version shows the idea. This version shows what a real integration
library does differently: a tap on its own thread, and a shared-object trap
that must be closed on purpose.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than ten library files on the classpath.
- A thread pool whose waiting copies are lost if the program stops.

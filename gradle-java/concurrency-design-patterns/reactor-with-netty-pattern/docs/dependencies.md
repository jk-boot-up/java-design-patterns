# Dependencies

This project uses Netty, which the plain Java version of Reactor does not.
Skipping it loses none of the pattern: the plain version teaches all of it
with nothing installed.

## What Netty is

Netty is a library for network servers and clients. An event loop is one thread that waits on many connections and runs their handlers: a reactor. A boss group accepts connections; a worker group serves them. Each connection has a channel pipeline: a chain of handlers that data passes through, such as LineBasedFrameDecoder, which turns bytes into whole lines, and your own handler at the end. An executor group is a set of ordinary threads; a handler added with one runs there instead of on the event loop.

## Why this project uses them

The plain version shows the reactor built from a selector. This version shows
the library most Java networking is built on, and the tools it gives for
framing, scaling and slow work.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Netty | 4.2.18.Final |

## What it costs

- A new vocabulary to learn.
- The discipline of never blocking an event loop.

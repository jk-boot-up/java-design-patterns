# Dependencies

This project uses Apache Camel, which the plain Java version of Resequencer
does not. Skipping it loses none of the pattern: the plain version teaches
all of it with nothing installed.

## What Apache Camel is

Camel is a library for moving messages. A route begins with from and lists steps. resequence takes an expression that gives each message's sequence number, here a header called seq. In stream mode, a message is released when the one before it has been released, and a gap is waited for until the timeout. In batch mode, messages are collected until the batch size or the timeout is reached, sorted, and released together. The release happens on Camel's own thread, which is why the demo waits for the page with a bounded poll.

## Why this project uses them

The plain version shows the idea. This version shows how a production
resequencer actually behaves at the edges: the first message, a full batch,
several sequences, and a lost message.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than ten library files on the classpath.
- Timing behaviour to understand: timeouts, and releases on another thread.

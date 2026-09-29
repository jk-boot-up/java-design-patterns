# Dependencies

This project uses Apache Camel, which the plain Java version of Recipient
List does not. Skipping it loses none of the pattern: the plain version
teaches all of it with nothing installed.

## What Apache Camel is

Camel is a library for moving messages. A route begins with from and lists steps. multicast sends a copy to a fixed list of endpoints. recipientList computes the list for each message, here by calling a Java method that returns endpoint addresses separated by commas, and sends a copy to each. An endpoint address such as direct:north names a route inside the program; the same step could name a queue, a file or a web service instead.

## Why this project uses them

The plain version shows the idea. This version shows the step every
integration library has for it, and what that step does and does not do for
you when one recipient fails.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than ten library files on the classpath.
- Endpoint addresses in strings, checked only when used.

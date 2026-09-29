# Dependencies

This project uses Apache Camel, which the plain Java version of Routing Slip
does not. Skipping it loses none of the pattern: the plain version teaches all
of it with nothing installed.

## What Apache Camel is

Camel is a library for moving messages. A route begins with from and lists steps. routingSlip reads a list of endpoint addresses, here from a header called slip, and sends the message to each in turn. dynamicRouter calls a method before every step; the method looks at the message and at the step just finished, and returns the next endpoint, or nothing to finish.

## Why this project uses them

The plain version shows the idea. This version shows how a routing library
carries a slip, and the tool it offers when the route must change on the way.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than ten library files on the classpath.
- Endpoint names in strings, checked only when used.

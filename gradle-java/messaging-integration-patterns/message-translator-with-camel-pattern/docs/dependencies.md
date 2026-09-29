# Dependencies

This project uses Apache Camel, which the plain Java version of Message
Translator does not. This page says what Camel is, why it is here, and what it
costs. Skipping this project loses none of the pattern: the plain version
teaches all of it with nothing installed.

## What Apache Camel is

Camel is a library for moving and transforming messages. You write a route: a short description of where messages come from, what happens to them, and where they go. A route begins with from, and each step after it is one method call. An endpoint is one end of a route, written as text such as direct:inbox; direct endpoints live inside the program, so nothing else needs to run. A data format is a ready-made reader and writer for text such as CSV, JSON or XML; unmarshal reads text into Java objects. A type converter turns one Java type into another; when none exists, Camel refuses the message rather than guessing.

## Why this project uses them

The plain version answers "what is a message translator". This version
answers "what does a real integration library give you for it, and what does
it make you learn": ready-made format readers, a type check at the door,
routing by name, and adding a translator while the rest keeps running.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Apache Camel (core, csv, jackson, xpath) | 4.22.1 |
| SLF4J simple | 2.0.17 |

## What it costs

- More than twenty library files on the classpath.
- Camel's route language and its error messages to learn.
- Stack traces that pass through Camel's engine, which are longer to read.

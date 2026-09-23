# Dependencies

This project uses Apache Camel, which the hand-built project does not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Splitter and Aggregator](../../splitter-aggregator-pattern) teaches all of it in plain Java.

## What Apache Camel is

Apache Camel is an integration engine. You describe the path a message takes — where it starts, the steps it passes through, where it ends — and Camel moves messages along that path. Camel calls one such path a **route**, and it calls a message travelling along it an **exchange**.

Two of its steps are this pattern by name. **Split** takes one message and sends out one message for each piece of it. **Aggregate** does the opposite: it holds messages that belong together and sends out one message when they are done. What ties them together is the **correlation expression**, which is just a rule for reading the identifier that says which order a message belongs to.

The aggregate step will not emit anything until a **completion condition** is met. There are several, and you may set more than one; whichever is met first ends the wait. This project uses two of them: completion by size, meaning a count of messages, and completion by timeout, meaning a deadline.

## Why this project uses it

Because a real aggregator makes you say when it should stop waiting, and a real deadline needs something that watches the clock while the rest of the program carries on. Both are given away free by a simulation, and both are where the interesting failures live.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| `org.apache.camel:camel-core` | 4.20.0 |
| `org.slf4j:slf4j-simple` | 2.0.16 |

**No container runtime is needed.** Camel is a library, and it runs inside the demo's own process. There is no broker, no database and no network call anywhere in this project. Nothing is downloaded at run time after the first Gradle build.

Camel 4.20.0 is the newest generally available release at the time this was written, and it needs Java 17 or later. Nothing is held back.

## What it costs

The first build downloads about twelve megabytes of Camel jars. The demo runs in about a second, most of which is the aggregator's six-hundred-millisecond deadline in the fifth act. Camel's engine starts in roughly ten milliseconds and holds one background thread for the deadline checker while a timeout aggregator is running.

Camel holds unfinished aggregations in memory by default, and this demo's sixth act shows a thousand of them held at once. In production that store is usually moved to a database, so a restart does not throw away work in progress.

## Where this pattern lives

In the route file. `split` and `aggregate` are steps you read top to bottom, and the completion conditions sit on the aggregate step where anybody reading the route can see them.

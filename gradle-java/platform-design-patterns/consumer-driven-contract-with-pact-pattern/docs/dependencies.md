# Dependencies

This project uses Pact, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Consumer-Driven Contract](../consumer-driven-contract-pattern) teaches all of it with plain Java.

## What Pact is

Pact JVM is the Java implementation of Pact. Its consumer DSL builds an expected interaction and runs the consumer's own client against a mock of the provider. If they agree, it writes a pact file. Its provider module replays the file against the real provider, through JUnit 5.

## Why this project uses it

The pact file is real, the mock is real, and the replay over HTTP is real. The failure message that names the consumer and the field is Pact's own.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Dependency | Version |
| --- | --- |
| `au.com.dius.pact.consumer:junit5` | 4.7.5 |
| `au.com.dius.pact.provider:junit5` | 4.7.5 |
| JUnit Platform launcher | from the JUnit 5.10.2 BOM |

Nothing else to install. Gradle downloads the jars. The demo sets `pact_do_not_track`, so Pact sends no usage statistics.

## What it costs

The first `./gradlew run` downloads about forty megabytes of jars. The demo takes about fifteen seconds.

## Where this pattern lives

In the consumer's tests, in a `pacts` folder or a Pact Broker, and in the provider's build as a verification step.

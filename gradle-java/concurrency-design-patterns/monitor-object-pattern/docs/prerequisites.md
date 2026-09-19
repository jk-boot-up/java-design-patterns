# Prerequisites

## Required

- **Producer–Consumer (§46).** This project reuses its harness unchanged.
- **Read–Write Lock (§49)** helps: the lock and condition types are met
  there first.

## Explicitly not required

- No prior experience with `Condition`, `await` or `signalAll`. Act four
  introduces them from nothing.
- No knowledge of the Java memory model. Act two says what `volatile`
  does and does not do, in a sentence.

## What you will need

Java 21. Nothing else; `./gradlew run` works offline.

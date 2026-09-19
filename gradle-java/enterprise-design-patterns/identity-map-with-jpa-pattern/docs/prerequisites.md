# Prerequisites

## Required

- Identity Map: the hand-built version this project pairs with.
- Java annotations, in one sentence: labels the framework reads.

## Explicitly not required

- No Spring. Hibernate is used directly.
- No prior JPA. `@Entity` and `@Id` are introduced in the first scene.
- No installed database. H2 runs inside the test.

## What you will need

Java 21. `./gradlew run` works offline.

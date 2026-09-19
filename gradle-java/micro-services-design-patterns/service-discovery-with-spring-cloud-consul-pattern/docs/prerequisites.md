# Prerequisites

## Required

- Service Registry and Discovery: the hand-built version this project pairs with.
- The `consul` program installed and on the PATH. Without it the demo says so and stops, and the tests are skipped.

## Explicitly not required

- No prior Spring Cloud. It is introduced as it appears.
- No running Consul: the demo starts its own agent on free ports and stops it.

## What you will need

Java 21. `./gradlew run` works offline.

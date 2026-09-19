# Prerequisites

## Required

- Blue-Green and Canary: the hand-built version this project pairs with.
- Docker running, with `kind` and `kubectl` installed. Without them the demo says so and stops, and the cluster test is skipped.

## Explicitly not required

- No prior Kubernetes. It is introduced as it appears.
- No existing cluster: the demo makes its own with kind, and deletes it.

## What you will need

Java 21. `./gradlew run` works offline.

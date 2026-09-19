# Prerequisites

## Required

- Sidecar: the project before this one, which teaches the pattern.
- What a container is, in one sentence: a packaged process with its own filesystem and network.

## Explicitly not required

- No Kubernetes. The model in Tier 1 needs none, and `docs/dependencies.md` explains it.
- No Docker for Tier 1.
- No YAML: the manifests are Java records here.

## What you will need

Java 21. `./gradlew run` works offline.

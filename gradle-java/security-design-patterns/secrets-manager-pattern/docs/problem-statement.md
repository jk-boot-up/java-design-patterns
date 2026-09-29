# Problem Statement

## The scenario

The store's payment key was committed in configuration and built into three
services.

## The naive version

Forty people could read it, it lived in the history, and changing it meant
rebuilding three services.

## What this project must deliver

- A hard-coded key and its exposure.
- A secrets manager with per-service grants and an audit log.
- Rotation with a cache and a grace period.
- An emergency rotation with refetch on refusal.
- The costs: availability and secret zero.
- Every printed result asserted by a test.

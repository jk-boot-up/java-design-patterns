# Problem Statement

## The scenario

The payment key is committed in code and built into three services.

## The naive version

Anyone with the repository can read it, and changing it means rebuilding
every service.

## What this project must deliver

- A hard-coded key.
- A policy and per-service tokens in OpenBao.
- Versioned rotation.
- Revoking a leaked token.
- The costs of running a secrets manager.
- Every printed result asserted by a test, skipped without Docker.

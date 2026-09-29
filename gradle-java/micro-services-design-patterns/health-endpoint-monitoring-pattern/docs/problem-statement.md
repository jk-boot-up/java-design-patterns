# Problem Statement

## The scenario

Three checkout instances sit behind a load balancer. Each has its own database
and shares the payment provider and recommendations service.

## The naive version

The load balancer checks only that each instance's port is open. A stuck
instance keeps its port open, keeps receiving a third of the orders, and fails
every one of them.

## What this project must deliver

- The open-port check shown losing 3 of 9 orders to a stuck instance.
- A liveness endpoint that takes the stuck instance out and gets it restarted.
- A readiness endpoint that separates DOWN (critical dependency) from DEGRADED (non-critical).
- The restart storm shown when liveness includes a shared dependency: 3 of 3 against 0.
- The costs shown: 54 dependency calls a minute, and details that must stay private.
- Every printed number asserted by a test.

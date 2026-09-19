# Problem Statement

## The scenario

A new release of the checkout is ready. One in ten orders is a big one, and the new release has a bug with big orders that nobody has found yet.

## The naive version

Stop the old release, install the new one, and start it.

```
  stop v1, install v2, start v2: 10 requests arrive while it is down. of 100 requests, failed: 10.
```

## What this project must deliver

Two releases behind a router with a fixed rule for each request; an in-place upgrade with a gap; a switch to a good release; a switch to a buggy one and back; a five percent canary; a step-by-step rollout with a failure gate; and the costs of double capacity and of shared data.

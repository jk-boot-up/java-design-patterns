# Problem Statement

## The scenario

Pickers take ten orders a minute; same-day orders must reach the van by 9:05.

## The naive version

A first-in-first-out queue makes same-day orders wait behind every standard
order.

## What this project must deliver

- Same-day orders missing the van on an ordinary queue.
- A RabbitMQ priority queue picking them first.
- The same with a thousand orders ahead.
- The prefetch trap, and prefetch 1.
- Starvation, and a reserved share built with two queues.
- Every printed result asserted by a test, skipped without Docker.

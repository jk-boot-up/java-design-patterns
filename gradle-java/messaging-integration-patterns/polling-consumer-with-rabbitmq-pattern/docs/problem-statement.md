# Problem Statement

## The scenario

A label printer with a ten-job buffer must print a burst of fifty orders, and
pause when paper runs out.

## The naive version

Pushing every order as it arrives floods the printer's memory.

## What this project must deliver

- Unlimited push flooding the printer.
- Polling with `basicGet`, five per tick.
- Pausing by not polling, with nothing lost.
- Empty polls counted, and push with prefetch as the middle way.
- The costs named.
- Every printed result asserted by a test, skipped without Docker.

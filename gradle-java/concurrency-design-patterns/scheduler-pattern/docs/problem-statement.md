# Problem Statement

## The scenario

Six packing stations share one label printer; express orders must catch the
afternoon van.

## The naive version

A fair lock serves jobs in arrival order, so express labels wait behind every
standard label that arrived first.

## What this project must deliver

- Arrival order shown with a fair lock.
- A scheduler with an express-first policy.
- The policy swapped for smallest-first with no other change.
- Starvation shown, and prevented by ageing.
- Every printed order asserted by a test.

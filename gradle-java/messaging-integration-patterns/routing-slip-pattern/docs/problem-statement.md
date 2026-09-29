# Problem Statement

## The scenario

Orders need different sets of processing steps depending on whether they are
gifts, age-restricted or going abroad.

## The naive version

`FixedPipeline` sends every order through all six steps, and each step checks
whether it applies: 24 visits for 15 pieces of work.

## What this project must deliver

- Wasted visits counted in a fixed pipeline.
- A routing slip written per order.
- Steps passing orders along their slips.
- A new step added through the slip rules.
- A failed step stopping a slip that cannot re-route.
- Every printed result asserted by a test.

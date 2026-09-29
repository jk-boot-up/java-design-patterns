# Problem Statement

## The scenario

Checkout turns postcodes into addresses with a paid external service that
needs the network.

## The naive version

Developers call the real service for every test checkout: £2.50 and 20 seconds
a day, no work possible offline, and no way to test an outage.

## What this project must deliver

- The cost of developing against the real service shown.
- A stub behind the same gateway interface: free, instant, offline.
- Unknown postcodes and outages played on demand.
- A contract check that finds the stub's small-letters difference.
- Every printed result asserted by a test.

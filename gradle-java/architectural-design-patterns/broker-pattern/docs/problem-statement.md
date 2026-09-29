# Problem Statement

## The scenario

Checkout calls a stock service and a price service, which sometimes move or
run as several instances.

## The naive version

Checkout holds the services' addresses. When the stock service moves, checkout
calls the old address and every order fails.

## What this project must deliver

- A hard-coded address failing after a move.
- A broker forwarding calls by name over HTTP.
- A moved service re-registering with no client change.
- Two instances served in turn.
- The costs shown: an extra hop and a single point of failure.
- Every printed result asserted by a test.

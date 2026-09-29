# Problem Statement

## The scenario

Checkout's tests use a stub of the payment service, which another team
releases independently.

## The naive version

A hand-written stub keeps the old behaviour after the real service changes.

## What this project must deliver

- A hand-written WireMock stub drifting from the real service.
- A WireMock stub built from a shared contract file.
- The real service verified against the same file.
- A strict stub answering 404 for an unlisted request.
- The shared cost, and where Spring Cloud Contract fits.
- Every printed result asserted by a test.

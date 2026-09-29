# Problem Statement

## The scenario

The store's order service answered the internet directly and held the
database password.

## The naive version

Internal-only features, a spoofable admin header and a path to the admin
export, were reachable by anyone.

## What this project must deliver

- A directly exposed service leaking every order two ways.
- A gatekeeper that strips internal headers.
- An allow-list of request shapes.
- Size and pattern limits.
- The costs and the limits of the gate.
- Every printed result asserted by a test.

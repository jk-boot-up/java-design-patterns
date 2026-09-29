# Problem Statement

## The scenario

The store runs on two servers behind a load balancer, and each kept its
signed-in customers in its own memory.

## The naive version

A request sent to the other server finds no session, and the customer is asked
to sign in again.

## What this project must deliver

- Sessions failing across two servers.
- A JWT-shaped token signed with HMAC-SHA256.
- Forged and expired tokens refused.
- Early sign-out and the revoked-list problem.
- The key and payload warnings.
- Every printed result asserted by a test.

# Problem Statement

## The scenario

The shop runs two server instances, and sessions live in each one's memory.

## The naive version

A request that reaches the other instance finds no session, and the customer
must sign in again.

## What this project must deliver

- Sessions failing across two Spring Boot instances.
- A JWT issued at sign-in and accepted by both.
- Forged and expired tokens refused by Spring Security.
- A revoked list as a validator, per instance.
- The readable payload and a stolen key.
- Every printed result asserted by a test.

# Problem Statement

## The scenario

The store's checkout and reviews used form text exactly as it arrived.

## The naive version

A negative quantity made a negative total, junk was saved as an email, and a
review could run a script in other shoppers' browsers.

## What this project must deliver

- Unchecked input producing a negative total.
- Boundary checks reporting every problem at once.
- Self-checking types and a `ValidOrder`.
- HTML output encoding.
- A fair name rule, and why the server must check.
- Every printed result asserted by a test.

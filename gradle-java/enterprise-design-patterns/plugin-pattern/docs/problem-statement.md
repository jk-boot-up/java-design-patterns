# Problem Statement

## The scenario

The store runs in development, staging and production. Real payments and
emails must only happen in production.

## The naive version

`ScatteredChoices` picks each implementation with an `if` on the environment
name. Adding staging updated one choice and missed another, and staging sent a
real email.

## What this project must deliver

- The missed choice shown: staging sending a real email.
- A configuration file per environment and a factory that reads it.
- Staging added as a file with no code change.
- A startup check that reports a misspelt class name.
- Every printed result asserted by a test.

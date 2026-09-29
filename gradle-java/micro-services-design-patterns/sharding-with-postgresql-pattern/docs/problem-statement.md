# Problem Statement

## The scenario

Black Friday brings 2,500 orders a minute, more than one database can take.

## The naive version

One database takes every read and write, and becomes the limit.

## What this project must deliver

- All orders on one PostgreSQL.
- Three PostgreSQL shards behind a router.
- A one-customer query asking one shard.
- A cross-shard query merged in code, and a unique rule broken across shards.
- Modulo against consistent hashing when resharding.
- Every printed result asserted by a test, skipped without Docker.

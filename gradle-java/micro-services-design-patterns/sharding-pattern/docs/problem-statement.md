# Problem Statement

## The scenario

Every order is kept in one database, which takes 1,000 new orders a minute.

## The naive version

On Black Friday 2,500 orders arrive a minute and 1,500 are left waiting every
minute.

## What this project must deliver

- The overload shown on one database.
- Orders split across three shards by customer number.
- A one-customer query asking one shard.
- An all-customer query asking every shard and merging.
- The data that moves when a shard is added.
- Every printed result asserted by a test.

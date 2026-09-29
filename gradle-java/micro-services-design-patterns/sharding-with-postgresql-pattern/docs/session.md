# Session Guide — Sharding with PostgreSQL Pattern

## Learning Objectives

By the end of the session you can:

- Route queries to shards by key.
- Merge a cross-shard query in code.
- Explain why a unique constraint no longer holds across shards.
- Compare modulo and consistent hashing for resharding.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One database | 7 min |
| 0:17 | Act 2: Three shards | 7 min |
| 0:24 | Act 3: One customer, one shard | 7 min |
| 0:31 | Act 4: Everyone, every shard | 7 min |
| 0:38 | Act 5: The bill: resharding | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Open `ShardRouter`: `shardFor` is one
line; `countOver` loops over every database. End on act four's coupon and act
five's 1,874 against 630.

## Exercises

1. Enforce the one-use coupon with a separate coupons database that every shard asks.
2. Route with jump hash instead of modulo, and count the orders per shard.
3. Move the customers that change shard when a fourth database is added.

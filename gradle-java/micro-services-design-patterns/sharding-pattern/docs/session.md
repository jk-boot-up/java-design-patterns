# Session Guide — Sharding Pattern

## Learning Objectives

By the end of the session you can:

- Explain what a shard key is and how to choose one.
- Route by key to one shard.
- Answer questions that span shards.
- Explain why adding shards moves data.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One database | 7 min |
| 0:17 | Act 2: Three shards | 7 min |
| 0:24 | Act 3: One customer, one shard | 7 min |
| 0:31 | Act 4: Everyone, every shard | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 1,500 waiting with act two's three
shares. Open `ShardedOrders.shardOf`: one line decides everything. End on act
five: why would a lookup table or consistent hashing move fewer customers?

## Exercises

1. Replace `% n` with a lookup table from customer to shard, and add a fourth shard moving only new customers.
2. Shard by order number instead. What happens to "customer 17's orders"?
3. Add a customer who places 2,000 orders a minute. Which shard suffers?

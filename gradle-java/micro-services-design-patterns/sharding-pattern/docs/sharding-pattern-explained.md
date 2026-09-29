# Sharding, Explained

## The pattern in one sentence

Sharding splits one large table across several databases by a key, so each
holds and serves only its share, with a router that picks the shard from the
key.

## The 5 acts

### 1. One database

Every order goes to one database that can take 1,000 new orders a minute. On
Black Friday, 2,500 arrive each minute, and 1,500 are left waiting every
minute, so the queue keeps growing.

### 2. Three shards

`ShardedOrders` places each order on shard number customer modulo 3. The
minute's 2,500 orders split into 833, 834 and 833, each within its
database's limit. Customer 17 always lives on shard 2, customer 42 on shard
0.

### 3. One customer, one shard

Finding customer 17's orders needs only the shard key: the router asks shard
2 and no other. One shard asked.

### 4. Everyone, every shard

"Orders over £500 this minute" is about every customer, so every shard must be
asked and the three answers merged: 25 orders found, three shards asked.

### 5. The bill

Going from three shards to four with simple modulo changes the shard of 1,874
of the 2,500 customers, and all their orders must be copied across.
Consistent hashing or a lookup table reduces that. And one very busy customer
still lands entirely on one shard.

## The verdict

Shard only when one database truly cannot cope. Choose a key that spreads load
evenly and matches your most common queries, plan for cross-shard questions,
and use consistent hashing or a lookup table so adding shards moves little.

## How to recognise this in code you did not write

- A shard key or partition key in database settings.
- Code that picks a database from a key before querying.
- Scatter-gather queries across several databases.

## Where you have already met this

- MongoDB and Elasticsearch shards, and Cassandra partitions.
- Vitess and Citus, which shard MySQL and PostgreSQL.
- DynamoDB partition keys.
- Consistent hashing, which limits how much moves when shards are added.

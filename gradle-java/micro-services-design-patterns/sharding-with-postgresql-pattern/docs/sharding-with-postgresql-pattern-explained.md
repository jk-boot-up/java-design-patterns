# Sharding with PostgreSQL, Explained

## The pattern in one sentence

With PostgreSQL, sharding splits the data across separate databases by a key,
and a router in the application sends each query to the right one.

## The 5 acts

### 1. One database

All 2,500 orders go into a single PostgreSQL database. It holds them all, and
every read and write of Black Friday lands on that one server.

### 2. Three shards

Now there are three PostgreSQL databases, each in its own container. The
router puts each customer on the database numbered by customer number modulo
three. They hold 833, 834 and 833 orders. Customer 17 lives on shard 2, and
customer 42 on shard 0.

### 3. One customer, one shard

A question about one customer goes to one database only. Customer 17's
orders, ORD-17, come from shard 2; the other two databases are not asked.

### 4. Everyone, every shard

"How many orders are over £500?" must be asked of all three databases, and the
application adds the answers: 1,250. Worse, rules PostgreSQL enforces inside
one database stop at its edge. The coupon WELCOME10 is UNIQUE in every shard,
yet customer 17 on shard 2 and customer 42 on shard 0 both redeem it: each
database only knows its own rows.

### 5. The bill: resharding

Adding a fourth shard with customer modulo four puts 1,874 of the 2,500
customers on a different database, and their orders must be copied across.
Jump consistent hashing moves only 630. And no transaction spans two shards,
while one very busy customer still overloads their one shard.

## The verdict

Shard when writes outgrow one database. Choose a key most queries share,
route with consistent hashing, and keep rules that span customers in a place
every shard can see.

## How to recognise this in code you did not write

- A `shardFor(key)` method choosing a connection.
- Loops over several data sources that merge results.
- Sharding layers such as Citus or Vitess.

## Where you have already met this

- Citus, Vitess and other sharding layers for PostgreSQL and MySQL.
- MongoDB and Cassandra, which shard by a key built in.
- Consistent hashing in caches such as Memcached clients.

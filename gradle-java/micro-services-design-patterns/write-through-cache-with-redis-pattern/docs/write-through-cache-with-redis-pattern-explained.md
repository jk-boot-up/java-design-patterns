# Write-Through Cache with Redis, Explained

## The pattern in one sentence

With Redis and PostgreSQL, a write-through cache writes every change to the
database and then the shared cache before returning, and reads from the cache.

## The 5 acts

### 1. Round the cache

The kettle is £30.00, cached in Redis. The nightly job writes the new price,
£27.00, straight into PostgreSQL and forgets Redis. The product page, reading
Redis, shows £30.00; checkout, reading PostgreSQL, charges £27.00.

### 2. Write through

Now every write goes through `PriceStore.put`: PostgreSQL first, then Redis,
before it returns. The page and checkout both say £27.00, and so does a second
instance of the shop reading the same Redis, because the cache is a shared
server.

### 3. Reads from Redis

A hundred product-page views read the price from Redis. PostgreSQL is not read
at all, and Redis's own statistics count exactly a hundred cache hits.

### 4. When one of the two refuses

With PostgreSQL read-only for maintenance, the write fails first and Redis is
never touched: both still say £27.00. The other way round is the problem. The
demo freezes Redis during a write: PostgreSQL saves £25.00, Redis cannot be
written, and when it returns the page shows £27.00 against the database's
£25.00. They are two systems, and no transaction spans both; a time-to-live
on each cached price bounds how long they can disagree.

### 5. The bill

The nightly job updates a thousand prices: a thousand PostgreSQL writes and a
thousand Redis writes, every write waiting for both. And Redis now holds a
thousand more prices, though most will never be viewed.

## The verdict

Use write-through for data read far more than written, where a stale value is
costly. Write the database first, give cached values a time-to-live, and plan
for the moments when the cache cannot be written.

## How to recognise this in code you did not write

- A store whose `put` writes the database and then Redis.
- `SET key value EX seconds` after a database update.
- Product pages reading only from Redis.

## Where you have already met this

- Application-level write-through with Redis or Memcached in front of a database.
- Hazelcast and Apache Ignite, whose map stores can write through for you.
- CPU caches with a write-through policy.

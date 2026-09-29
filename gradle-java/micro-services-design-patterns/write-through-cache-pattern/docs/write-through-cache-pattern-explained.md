# Write-Through Cache, Explained

## The pattern in one sentence

A write-through cache takes every write, writes the database, then updates
itself before returning, so reads from it always match the database.

## The 5 acts

### 1. A write round the cache

`CacheAside` serves the product page from a cache. The nightly price job
writes the kettle's new price, £27.00, straight to the database and forgets
the cache. The product page still shows £30.00; checkout, reading the
database, charges £27.00.

### 2. Write-through

The job now calls `WriteThroughStore.put`, which writes the database and
then updates the cache before returning. The product page and checkout both
show £27.00.

### 3. Fast reads

A hundred product page views are all answered from the cache: zero database
reads. The cache already holds the latest price, because every write put it
there.

### 4. A refused write

The database goes read-only for maintenance. The price job tries £25.00; the
database refuses, so the store never updates its cache. Page and database both
still say £27.00: the two never disagree.

### 5. The bill

Every write waits for the database. The nightly job's 1000 price updates spend
20 seconds waiting, where write-behind would return at once. And all 1000
prices now sit in the cache, though most of those products will never be
viewed.

## The verdict

Use write-through for data that is read often and must never be stale, and
make it the only way to write that data. Accept slower writes, and limit what
the cache keeps.

## How to recognise this in code you did not write

- A store with `put` that writes the database and then the cache.
- `@CachePut` on update methods.
- Cache configuration with a `CacheWriter` or `write-through: true`.

## Where you have already met this

- Hazelcast and Ehcache `write-through` configuration with a `CacheWriter`.
- Spring's `@CachePut`, which updates the cache when a method writes.
- CPU caches, which can be configured write-through to main memory.

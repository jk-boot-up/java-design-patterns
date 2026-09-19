# Cache-Aside, Explained

## The pattern in one sentence

Cache-aside means the application looks in a cache first, and on a miss reads the source itself and puts the answer in the cache for next time.

## The six acts

### No Cache

A thousand views over ten popular products make a thousand database reads.

```
  1000 product page views over 10 popular products: 1000 database reads.
```

### Look Aside

The same thousand views now make ten database reads, ninety nine percent of them served by the cache.

```
  the same 1000 views: 10 database reads, 990 cache hits, 10 misses.
  ask the cache; on a miss, ask the database and remember the answer.
```

### Writes

If a price change forgets the cache, customers still see the old price. If it throws the cached copy away, the next read sees the new one.

```
  price changed to 1500 in the database, cache forgotten: a customer sees 1000.
  price changed to 1600, and the cached copy thrown away: a customer sees 1600.
```

### A Time Limit On Staleness

Another system changes the price behind the cache's back. Customers see the old price for the full sixty seconds, and the new one after that.

```
  another system changes the price to 2000. after 59 seconds: 1000.
  after 61 seconds: 2000.
  an expiry does not make the cache right. it makes it wrong for a bounded time.
```

### A Stampede

Fifty requests arrive together for one expired product. Every one misses, so every one reads the database: fifty reads. If the requests share a single read, there is one.

```
  50 requests arrive together for one popular product whose entry has just expired.
  every request checks the cache: 50 database reads.
  requests share one database read: 1 database read.
```

### The Bill

When the cache restarts empty, the database takes the whole load again until it warms up. And the cache is a copy, so there is a second thing to keep right.

```
  the cache is restarted, empty. the first 10 views: 10 database reads. the database takes the whole load again until it warms up.
  the cache is a copy, not the truth. there is now a second thing to keep right, to size, and to explain.
```

## The verdict

Use cache-aside for data that is read far more than it is written, where a little staleness is acceptable. Invalidate on every write you control, give every entry an expiry, and share the read when many callers miss together. Do not use it for data that must always be exact, and never treat the cache as the only copy.

## How to recognise this in code you did not write

- Code that calls `cache.get`, then the database, then `cache.put`.
- `@Cacheable` and `@CacheEvict` in Spring.
- A Redis or Memcached client beside a database client.
- A comment saying 'clear the cache when you change this'.

## Where you have already met this

Spring's `@Cacheable`, Redis in front of a database, and every browser's HTTP cache.

## When this is too much

For data that changes on every read, or that is read once, a cache is overhead. For data that must be exact, staleness is a bug, not a trade.

# Cache-Aside with Redis, Explained

## The pattern in one sentence

Cache-aside means the application asks a fast copy first, and when the copy has nothing, the application fetches the real answer itself and leaves a copy behind for the next person.

## The analogy, before any of Redis's words

Think of a busy restaurant kitchen. The recipes live in a thick book in the office down the corridor, and walking there takes time. So a whiteboard hangs by the kitchen door. A cook who needs a recipe looks at the board first. If the answer is there, good. If not, the cook walks to the office, reads the book, and writes the answer on the board on the way back. The board never walks to the office by itself. The cook does all of that.

Now three things the whiteboard makes you think about. Every cook in the kitchen reads the same board, so one cook's note saves every other cook the walk; and one cook wiping a note wipes it for everybody. Each note has a time written next to it, and a porter wipes it off when the time is up, whether or not anybody asked; but if a cook rewrites a note and forgets the time, the porter never wipes it. And when a popular note is wiped at the start of the dinner rush, twenty cooks look at the board at once, find nothing, and all walk to the office together. Those three things are this project.

## What Redis calls these things

**Redis** is the whiteboard: a separate program that keeps small pieces of data in memory and answers over the network. It runs in a container the demo starts and stops.

A **key** is the name of a note, and its **value** is what the note says. Here the key is `product:SKU-0` and the value is `1000`, a price in pence, written as text.

The time a note has left is its **time to live**. Redis shortens that to **TTL**. When the time is up, Redis removes the key by itself.

**SET** is the command that writes a key. It can carry an expiry. A SET that does not carry one writes a key that never expires, and throws away any expiry the key had before. The fourth act is about that.

**SET with NX** writes the key only if it does not already exist, and says whether it did. Exactly one caller can win, which makes it a lock that every shop process can see.

**redis-cli** is Redis's own command-line program. The demo runs it inside the container, as a second, separate reader.

**maxmemory** is the size limit Redis is given, and **eviction** is Redis throwing keys away to stay under it. Out of the box there is no limit, and nothing is ever thrown away.

## The six acts

### No Cache

Every product page reads the database. A thousand views over ten popular products cost a thousand database reads, though only ten different rows were ever read.

```
  1000 product page views over 10 popular products: 1000 database reads.
```

### Look Aside, In Redis

A Redis server is now running in a container. The shop asks Redis for the price first. On a miss it reads the database and writes the price into Redis, with a sixty-second expiry. The same thousand views now cost ten database reads: ten misses, then nine hundred and ninety hits. Redis holds ten keys.

```
  a Redis server is running in a container. the same 1000 views: 10 database reads, 990 cache hits, 10 misses.
  Redis now holds 10 keys, each written with a 60 second expiry.
```

### Another Process Can See It

This is the first act the twin could not stage. The first shop has viewed all ten products. Then a second shop starts, as a separate Java program with its own memory. Given a cache in its own memory, as the twin had, its first ten views cost ten database reads: the first shop's work is no use to it. Given the same Redis, its first ten views cost none, and all ten are hits.

Then Redis's own command-line program, a third, separate program, asks for the key for product SKU-0 and is told 1000. Finally the first shop changes that price to 1600 and deletes the key, once. No copy is left for any process, so every shop reads the new price next time.

```
  the first shop has viewed all 10 products. a second shop starts as a separate Java process.
  with its cache in its own memory, its first 10 views: 10 database reads, 0 cache hits.
  with its cache in Redis, its first 10 views: 0 database reads, 10 cache hits.
  redis-cli, a separate program in the container, asks for product:SKU-0 and is told: 1000.
  the first shop changes SKU-0 to 1600 and deletes the key once. copies left for any process: 0.
```

### Real Expiry

The price of SKU-0 is cached for two seconds. Another system changes the price in the database to 2000, and does not tell the cache, so a customer still sees 1000. Nobody deletes the key. The demo only asks Redis, again and again, whether the key is still there, until Redis has removed it on its own clock. The next customer sees 2000.

Then the headline find of this project. A price-sync job writes the price back into Redis with a plain SET, carrying no expiry. Redis now reports the key's time to live as minus one, which means never. The database changes the price to 2100. Two seconds later, as long as the first entry lived, a customer still sees 2000, and will until somebody deletes the key by hand. An expiry only limits staleness while every write keeps it.

```
  SKU-0 is cached for 2 seconds. another system changes the price to 2000. a customer sees 1000.
  nobody deletes it. Redis removes the key itself when the time is up. a customer then sees 2000.
  a price-sync job writes SKU-0 again with a plain SET. seconds to live, as Redis reports it: -1, which means never.
  the price changes to 2100. 2 seconds later a customer still sees 2000. the entry will never expire.
  an expiry only limits staleness while every write keeps it. one plain write turned it off.
```

### A Real Stampede

Fifty requests arrive at the same moment, split across two shop instances, for SKU-0, just after its entry has gone. A database read takes half a second, as it might on a busy evening. Every request asks Redis, finds nothing, and goes to the database. More than forty database reads, for one price. On the machine this was written on it was all fifty, but the exact count is up to the thread scheduler, so the demo describes it rather than counting it.

The twin's fix is to let the requests that miss together inside one program share one database read. With two instances that gives two reads, one per instance, because neither can see the other's waiting requests. The fix that works across processes is a lock kept in Redis: the first request to set a lock key, with NX, reads the database; every other request, in either instance, waits for the price to appear in Redis. One database read. The lock has its own five-second expiry, so a shop that dies holding it cannot block the others for ever.

```
  50 requests arrive together, across 2 shop instances, for SKU-0 just after its entry expired. a database read takes 500 milliseconds.
  every request checks Redis and misses. database reads: more than 40, for one price.
  requests share a read inside each instance: 2 database reads, one per instance.
  requests share a lock kept in Redis: 1 database read. the lock expires by itself after 5 seconds if its holder dies.
```

### The Bill

Redis is emptied, the way a restart with nothing saved would leave it, and the first ten views cost ten database reads again: the database takes the whole load until the cache warms up. Redis out of the box has maxmemory zero, which means no size limit, and the policy noeviction, which means it never throws anything away to make room. A cache has to be given a size and told what to discard. A price now crosses the network as text: Redis holds SKU-0 as the string 1000, and every reader has to turn it back into a number. And Redis is one more system to run, secure and watch: one container, for two shop processes.

```
  Redis is emptied, as a restart with nothing saved leaves it. the first 10 views: 10 database reads.
  Redis out of the box: maxmemory 0, which means no limit, and maxmemory-policy noeviction.
  a cache must be given a size and told what to throw away, or it grows until the machine runs out.
  and a price now crosses the network as text: Redis holds SKU-0 as the string 1000.
  and Redis is one more system to run, secure and watch: this demo needed 1 container for 2 shop processes.
```

## The verdict

Put Redis on the side when more than one process needs the same cached answers. Then say three things out loud, because Redis will not assume any of them: write every entry with an expiry, on every write, or it lives for ever; delete the entry after every change to the database, so every process rereads; and guard the refill of a popular entry with a lock that every process can see, with an expiry of its own. And give Redis a size and an eviction policy before it meets real traffic.

## How to recognise this in code you did not write

- A `get` followed, on a null, by a database query and a `set`. That is cache-aside.
- A `set` with no `ex`, `px` or `keepttl` beside it on a key that is meant to expire. That entry now lives for ever.
- A `del` after an update to the database, or its absence, which is the stale-price bug.
- A `set` with `nx` and `px` on a key named like `lock:`. That is a stampede guard, and its expiry is what keeps a crashed holder from blocking everyone.
- `maxmemory` and `maxmemory-policy` in the Redis configuration, or their absence, which means no limit.

## Where you have already met this

Product pages, prices, stock levels and sessions read from Redis or Memcached in front of a database, on any site that runs on more than one server. Spring's `@Cacheable` backed by Redis is this pattern with the lookup and the refill written for you.

## When this is too much

If the shop runs as one process, a map in its own memory is faster and costs nothing to run. If the data must be exact, staleness is a bug, not a trade. Redis earns its keep when several processes need to agree on the same cached answers.

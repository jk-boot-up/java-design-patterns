# Write-Through Cache with Redis Pattern — Video Narration Script

## 1. Write-Through Cache with Redis

Hello, and welcome. This video explains the Write-Through Cache pattern, with a real Redis and a real PostgreSQL database, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a write-through cache, every write goes to the database, and then to the cache, before it is finished. So the cache never shows something the database does not have. Redis is an open-source in-memory store, often used as a cache shared by many servers. Think of a shop's price list in the back office, and the price tags on the shelves. Whoever changes a price updates the list, then the tag, before doing anything else. In this video, the domain is an online shop's prices, shown on product pages and charged at checkout. By the end, you will hear how a forgotten cache shows the wrong price. How write-through fixes it. And why two real systems can still disagree.

## 2. The Scenario

Here is the scenario. Product pages read prices from Redis. Checkout reads the database. The nightly price job wrote new prices only to the database. Customers saw one price, and paid another.

## 3. Act One — Round the cache

First demo: a price change goes round the cache. The kettle costs thirty pounds, and that price is in Redis. The nightly job writes twenty-seven pounds, straight into the database. It forgets Redis. The product page still says thirty. Checkout charges twenty-seven.

## 4. Act Two — Write through

Second demo: write-through. Every price write now goes through one store. The database first, then Redis, before it returns. The page says twenty-seven. Checkout says twenty-seven. And a second copy of the shop, reading the same Redis, says twenty-seven too.

## 5. Act Three — Reads from Redis

Third demo: reads come from Redis. A hundred people view the product page. The database is not read at all. Redis's own counter shows a hundred cache hits.

## 6. Act Four — When one of the two refuses

Fourth demo: when one of the two refuses. The database is read-only, for maintenance. The write fails first, and Redis is never touched. They still agree. Now the other way round. Redis cannot be reached, during a write. The database saves twenty-five pounds. Redis keeps twenty-seven. Two systems. No transaction covers both. An expiry time on each cached price limits how long they can disagree.

## 7. Act Five — The bill

Fifth demo: the bill. The nightly job updates a thousand prices. A thousand database writes, and a thousand Redis writes. And Redis now holds a thousand more prices. Most will never be viewed.

## 8. The Pattern

Let's name the pattern. Every write goes to the database, then to Redis. Every read comes from Redis. And cached values get an expiry time, to limit how long they can be wrong.

## 9. Who Does What

Here is who does what. The price store writes through, and reads from the cache. The price database is PostgreSQL, the record of truth. Redis is the shared cache. And the infra class starts both in containers.

## 10. Where You Have Seen It

You have probably met this already. Redis, in front of a database, in many web shops. Hazelcast and Apache Ignite, which can write through for you. And the caches inside a processor.

## 11. When To Use It

So, when should you use it? For data read far more often than it is written, where a stale value is costly. Write the database first. Give cached values an expiry. And plan for the moment the cache cannot be written.

## 12. Thanks for Watching

That's the Write-Through Cache, with Redis. If you remember one sentence, make it this one. Write the truth, then the cache, and put a limit on how long they can disagree. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts Redis and PostgreSQL for you. Here is one exercise to try. Set a two-second expiry, and watch the page correct itself. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.

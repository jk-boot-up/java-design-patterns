# Problem Statement

## The scenario

The shop shows product pages, and every page needs a price. The prices live in the database, which is the source of truth. Ten products are popular and get most of the views, and their prices change rarely. The shop runs as more than one process, because one is never enough on a busy day, and every one of them reads the same database. Reading the same ten rows a thousand times is work the database should not have to do.

## The naive version

Every page view reads the database.

```
  1000 product page views over 10 popular products: 1000 database reads.
```

## What the twin project already did

The plain-Java Cache-Aside project in this course put a cache on the side: the shop asks the cache first, and on a miss asks the database itself and remembers the answer. A write goes to the database and then throws the cached copy away. Every entry expires after a while. It showed a stampede, and it fixed the stampede by letting requests that miss together share one database read. It is a complete teaching of the idea and nothing here replaces it.

It had three comforts, though. The cache was a map inside the shop's own program, so there was only ever one shop and one cache. Its clock was a counter the demo moved by hand, so nothing expired unless the demo said so. And its stampede had to be arranged: the demo held every database read until all fifty requests had missed.

## What this project must deliver

The same shop, the same ten products and the same prices in pence, with the cache moved into a real Redis server that the demo starts in a container and stops at the end. A second shop started as a separate Java process, finding the cache already warm. Redis's own command-line program reading the shop's entry. An entry that Redis removes on its own clock while the demo only watches, and a plain write that quietly turns that clock off. Fifty real requests across two shop instances stampeding the database with nothing arranging it, and a lock kept in Redis that brings the reads down to one. And an honest bill: an emptied cache hands the load back, Redis out of the box has no size limit, prices travel as text, and Redis is one more system to run.

Every figure printed is the program's own, and two runs back to back print the same thing.

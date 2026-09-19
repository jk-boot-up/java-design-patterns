# Problem Statement

## The scenario

Ten popular products account for almost every page view. Each view reads the product from the database.

## The naive version

No cache. Every page view is a database read, so a thousand views is a thousand reads, on the same ten rows.

```
  1000 product page views over 10 popular products: 1000 database reads.
```

## What this project must deliver

A cache with an expiry on a clock the demo controls; a service that looks aside; the read counts with and without; a write that invalidates and one that forgets; a bounded staleness; a stampede of fifty simultaneous misses and the shared read that answers them with one; the cold-cache bill; and a plain verdict.

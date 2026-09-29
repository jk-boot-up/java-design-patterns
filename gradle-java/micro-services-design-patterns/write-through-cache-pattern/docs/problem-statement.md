# Problem Statement

## The scenario

The product page reads prices from a cache; checkout reads the database; a
nightly job changes prices.

## The naive version

The job writes straight to the database and forgets the cache: the page shows
£30.00 while checkout charges £27.00.

## What this project must deliver

- The stale page shown after a write round the cache.
- A write-through store keeping cache and database equal.
- Reads served from the cache with no database reads.
- A refused database write leaving the cache untouched.
- The write cost counted.
- Every printed result asserted by a test.

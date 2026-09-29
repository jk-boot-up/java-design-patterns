# Problem Statement

## The scenario

A flash sale: 100 kettles, eight buyer threads each trying to buy fifty.

## The naive version

`UnsafeStock` reads the count and later writes back the count minus one, so
two buyers can both take the same kettle and the shop oversells.

## What this project must deliver

- Overselling shown with check-then-act.
- A locked version selling exactly 100.
- A compare-and-set retry loop selling exactly 100 with no locks.
- The same loop as one `getAndUpdate` call.
- The one-value limit shown.
- Every printed result asserted by a test.

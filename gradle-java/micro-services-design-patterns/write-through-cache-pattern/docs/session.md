# Session Guide — Write-Through Cache Pattern

## Learning Objectives

By the end of the session you can:

- Explain how writes that bypass a cache make it stale.
- Write the database first, then the cache.
- Explain why a failed write must not touch the cache.
- Choose between write-through, write-behind and cache-aside.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A write round the cache | 7 min |
| 0:17 | Act 2: Write-through | 7 min |
| 0:24 | Act 3: Fast reads | 7 min |
| 0:31 | Act 4: A refused write | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one's two prices. Open
`WriteThroughStore.put`: two lines, in that order. Ask what would happen if
they were swapped, then run act four.

## Exercises

1. Swap the two lines in `put` and write a test that fails because of it.
2. Only cache products that have been read at least once.
3. Make the price job update 1000 prices with one batched database write.

# Session Guide — Write-Through Cache with Redis Pattern

## Learning Objectives

By the end of the session you can:

- Write through to a database and a shared cache.
- Read from the cache and confirm it with Redis statistics.
- Explain why a write can leave the two disagreeing.
- Bound disagreement with a time-to-live.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Round the cache | 7 min |
| 0:17 | Act 2: Write through | 7 min |
| 0:24 | Act 3: Reads from Redis | 7 min |
| 0:31 | Act 4: When one of the two refuses | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's two prices with act
two's one. Open `PriceStore.put`: database, then cache. End on act four's
£27.00 against £25.00.

## Exercises

1. Set the time-to-live to 2 seconds and show the page correcting itself after act four.
2. When Redis cannot be written, delete the key on the next successful call.
3. Only cache prices on their first read, and compare Redis's size after act five.

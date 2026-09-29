# Session Guide — Space-Based Architecture with Hazelcast Pattern

## Learning Objectives

By the end of the session you can:

- Start an embedded Hazelcast cluster.
- Sell atomically with an entry processor.
- Explain owners and backups.
- Configure write-behind and explain its risk.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One database for everyone | 7 min |
| 0:17 | Act 2: Stock in the grid | 7 min |
| 0:24 | Act 3: One grid, not three copies | 7 min |
| 0:31 | Act 4: Write-behind | 7 min |
| 0:38 | Act 5: The last kettle, a crash, and the bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's 1.4 seconds with act two's under one.
Open `SellOne`: the whole sale. Open `Grid.config`: backups and write-behind.
End on act five's sold 1 of 2.

## Exercises

1. Set the backup count to 0 and repeat the crash in act five.
2. Sell the last kettle with get and put instead of an entry processor, and run it many times.
3. Replace the slow database with PostgreSQL through JDBC in the map store.

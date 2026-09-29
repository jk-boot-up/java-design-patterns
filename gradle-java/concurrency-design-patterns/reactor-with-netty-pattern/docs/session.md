# Session Guide — Reactor with Netty Pattern

## Learning Objectives

By the end of the session you can:

- Start a Netty server with boss and worker groups.
- Build a pipeline with a line decoder and a handler.
- Explain how connections are spread over event loops.
- Move slow work off the event loop.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One event loop | 7 min |
| 0:17 | Act 2: The pipeline | 7 min |
| 0:24 | Act 3: Everyone at once | 7 min |
| 0:31 | Act 4: Several event loops | 7 min |
| 0:38 | Act 5: The bill: never block | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ShopServer`: the bootstrap and the pipeline are a
dozen lines. Compare act five's two results: the same handler, on the loop
and on its own executor group.

## Exercises

1. Add a handler that logs every question before it is answered.
2. Limit lines to 32 characters and send a longer one.
3. Replace the blocking tills with a Netty client.

# Session Guide — Reactor Pattern

## Learning Objectives

By the end of the session you can:

- Explain why a thread per connection wastes threads.
- Describe the selector as an event demultiplexer.
- Write accept and read handlers for a reactor loop.
- Explain why handlers must never block.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A thread per connection | 7 min |
| 0:17 | Act 2: One reactor thread | 7 min |
| 0:24 | Act 3: A handler per event | 7 min |
| 0:31 | Act 4: Every till, one thread | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare the thread counts in acts one and two. Open
`Reactor.run`: the whole pattern is the loop, `select`, and the two `if`s.
End on act five and ask how the report could be run without stopping the
reactor.

## Exercises

1. Hand the report to a thread pool and write its answer back when it is ready.
2. Handle a line that arrives in two pieces.
3. Run the thread-per-connection server on virtual threads. How many platform threads does it use?

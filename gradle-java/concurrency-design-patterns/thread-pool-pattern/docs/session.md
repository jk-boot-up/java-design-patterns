# Session Guide — Thread Pool Pattern

A 60-minute session built around one question: a fixed number of workers
sounds bounded — bounded compared to what?

## Learning Objectives

By the end of the session a participant can:

1. Explain why `Executors.newFixedThreadPool` is not, by itself, the
   pattern — and name what it leaves unbounded.
2. State the difference between a bounded queue's patience window and a
   thread pool's rejection handler.
3. Explain the pool-starvation deadlock, and why it happens at every pool
   size once a task nests a submit-and-wait inside itself.
4. State, in one sentence, what virtual threads change and what they do
   not.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | Setup, and act one |
| 0:08–0:20 | Act two, and the hidden queue |
| 0:20–0:35 | The pattern, and rejection with no patience |
| 0:35–0:48 | Pool starvation |
| 0:48–0:55 | Virtual threads |
| 0:55–1:00 | Exercises, and wrap-up |

## 0:00–0:08 — Setup, And Act One

```bash
cd concurrency-design-patterns/thread-pool-pattern
./gradlew -q run
```

Read act one's output together. Ask: what does this project share with
§46's naive version? (Everything — it is the identical failure, seen from
the packing team's side.)

## 0:08–0:20 — Act Two, And The Hidden Queue

Open `naive/UnboundedPoolPacking.java`. Ask: how many worker threads does
this class ever create? (Exactly two, always.) Then ask: how many orders
can be waiting behind them? Run act two and find the backlog number.
Discuss why nothing printed that number until the demo asked for it on
purpose.

## 0:20–0:35 — The Pattern, And Rejection With No Patience

Open `pattern/BoundedPackingPool.java`. Compare its constructor against
§46's `BoundedOrderQueue` — what does this one bound that the other
project's naive fixed pool did not? Run act three and find the rejection
line. Ask: how long did this submission wait before being refused? (Zero
— `execute()`'s rejection handler runs before the call even returns.)

## 0:35–0:48 — Pool Starvation

Open `pattern/PoolStarvation.java`. Walk through what the outer task does:
submits an inner task to its own pool, then waits for it. Ask the room to
predict the outcome with a pool of one worker before running act five.
Then ask: would a bigger queue capacity fix this? (No — say why, out
loud, before revealing that the answer is no.)

## 0:48–0:55 — Virtual Threads

Run act six and compare its number directly against act one's. Ask: does
this number mean the pool from act three is no longer needed? Walk
through the downstream-connection-limit argument in
[`thread-pool-pattern-explained.md`](thread-pool-pattern-explained.md)
until the room can state, unprompted, what a pool actually bounds.

## 0:55–1:00 — Exercises, And Wrap-Up

1. **Give the pool a second worker.** Change act five's pool size to two
   and predict what happens to the starvation outcome before running it.
2. **Widen the queue in act three.** Change the capacity from 3 to 30 and
   confirm the rejection still happens eventually — only later.
3. **Make the rejection handler retry instead of count.** Write a handler
   that sleeps briefly and resubmits, and discuss why that reintroduces a
   kind of unbounded wait this project spent an entire act removing.

Close with the sentence worth remembering: a pool bounds a resource, not a
thread count — and a resource with no free slots left stays out of slots
no matter how cheap the thread asking for one was to create.

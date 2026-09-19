# Session Guide — Producer–Consumer Pattern

A 60-minute session built around one question: what happens when arrivals
outpace processing, and who decides?

## Learning Objectives

By the end of the session a participant can:

1. Explain why the inline and thread-per-order versions both fail, and how.
2. State, without hedging, why an unbounded queue is the thread-per-order
   failure again in a different shape.
3. Name the two policies a full queue can choose between, and the cost of
   each.
4. Explain the difference between a poison pill and an interrupt as a
   shutdown signal.
5. Explain, in one sentence, why none of this project's tests sleep.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | Setup, and act one |
| 0:08–0:20 | Act two, and the real cost of a thread |
| 0:20–0:32 | The bound, and the two ways to say no |
| 0:32–0:45 | Two shutdowns |
| 0:45–0:53 | Why nothing here sleeps |
| 0:53–1:00 | Exercises, and wrap-up |

## 0:00–0:08 — Setup, And Act One

```bash
cd concurrency-design-patterns/producer-consumer-pattern
./gradlew -q run
```

Read act one's output together. Ask: who is paying for the pack step
taking 50ms? (The customer, every time, in the checkout call itself.)

## 0:08–0:20 — Act Two

Read the thread-creation numbers aloud. Extrapolate together to a busier
day — 10,000 orders instead of 2,000 threads. Ask what a stack costs per
thread, and multiply.

## 0:20–0:32 — The Bound

Open `BoundedOrderQueue.java`. Ask: what happens if the constructor took
no capacity argument at all? Run act three and find the rejection line.

## 0:32–0:45 — Two Shutdowns

Read act four and act five side by side. Ask the room which one they would
reach for by default, and why that is often the wrong instinct — a raw
`interrupt()` is usually easier to write than plumbing a poison pill
through, which is exactly why it gets used by mistake.

## 0:45–0:53 — Why Nothing Here Sleeps

Open `PackerTest.interruptingThePackerLosesWhateverIsStillQueued`. Walk
through the `Gate` and `CountDownLatch` together and ask what would happen
if `Thread.sleep(50)` replaced the latch — would the test still pass most
of the time? (Yes.) Is "most of the time" acceptable? (No — and that is
this category's whole discipline.)

## 0:53–1:00 — Exercises, And Wrap-Up

1. **Change the policy.** Swap act three's rejection for a blocking `put`
   and observe checkout slow down again once the queue is full.
2. **Add a second producer.** Confirm ordering between the two producers
   is no longer guaranteed, and say why.
3. **Break determinism on purpose.** Replace the `CountDownLatch` in
   `PackerTest` with a `Thread.sleep(10)` and run the test a few dozen
   times. If it never fails, lower the sleep until it does — a fast
   demonstration of exactly what this whole project is built to avoid.

Close with the sentence worth remembering: a queue with no bound is not a
safer version of this pattern. It is the thread-per-order failure, wearing
a nicer name.
